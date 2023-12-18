from numpy import cos, sin, arctan2, sqrt, sign, pi, delete, append, array, exp, arccos

from behaviours import Univector
from corners import handle_edge_behaviour

from face_selector import sideDecider_goalkeeper

import action

def approx(robot, target, avoid_obst=True, obst=None, n=8, d=2, field_is_hiperbolic=True):
    """Input: Robot object, Target object, Flag to activate Obstacle Avoidance, Obstacle object,
       Constants n and d of Univector, Flag to activate Hiperbolic Field
    Description: Estimate of robot desired angle in projection ( x + dl, y + dl )
    Output: stp_theta -> Angle referring to robot projection (float)"""
    navigate = Univector()  # Defines the navigation algorithm
    dl = 0.000001  # Constant to approximate phi_v

    x = robot._coordinates.X  # Saving (x,y) coordinates to calculate phi_v
    y = robot._coordinates.Y
    robot._coordinates.X = robot._coordinates.X + dl * cos(robot._coordinates.rotation)  # Incrementing robot (x,y) position
    robot._coordinates.Y = robot._coordinates.Y + dl * sin(robot._coordinates.rotation)

    if avoid_obst:                                                          # If obstacle avoidance is activated
        if field_is_hiperbolic:                                             # Use of the Hyperbolic field
            stp_theta = navigate.univec_field_h(robot, target, obst)        # Computing a step Theta to determine phi_v
        else:                                                               # Use of the old field
            stp_theta = navigate.univec_field_n(robot, target, obst, n, d)  # Computing a step Theta to determine phi_v
    else:
        if field_is_hiperbolic:                                             # Use of the Hyperbolic field
            stp_theta = navigate.hip_vec_field(robot, target)               # Computing a step Theta to determine phi_v
        else:                                                               # Use of the old field
            stp_theta = navigate.n_vec_field(robot, target, n, d, have_face=False) # Computing a step Theta to determine phi_v

    robot._coordinates.X = x  # Returning original (x,y) coordinates
    robot._coordinates.Y = y

    return stp_theta

def calculate_phi_v(robot, target):
    delta_theta_d = robot.univector_angle - robot.last_univector_angle
    delta_x = robot._coordinates.X - robot._coordinates.last_X
    delta_y = robot._coordinates.Y - robot._coordinates.last_Y
    phi_V = delta_theta_d/(delta_x+0.001) * cos(robot._coordinates.rotation) + delta_theta_d/(delta_y+0.001) * sin(robot._coordinates.rotation)
    return phi_V

def univec_controller(robot, target, avoid_obst=True, obst=None, n=8, d=2, stop_when_arrive=False, double_face=True,
                      field_is_hiperbolic=True, screen_out=False, pos_auto=False):
    """Input: Robot object, Target object, Flag to activate Obstacle Avoidance, Obstacle object, Constants n and d of Univector,
       Flag to activate deceleration when approaching target, Flag to activate face swap, Flag to activate Hiperbolic Field
    Description: Function to control the robot with or without obstacle avoidance
    Output: v -> Linear Velocity (float)
            w -> Angular Velocity (float)"""
    
    handle_edge_behaviour(robot)  # Checks if the robot is in some corner
    navigate = Univector()  # Defines the navigation algorithM

    # Adequate univector constantes if robot is in screen_out
    if screen_out or robot.index == 0:
        navigate.k_r = 3
        navigate.d_e = 5
    
    dl = 0.000001  # Constant to approximate phi_v
    k_w = 1.7  # Feedback constant for angle error (k_w=1 means no gain)
    k_p = 1  # Proporcional constant for stopping when arrive in target (k_p=1 means no gain)

    # Angle correction if robot face is inverted
    # TODO: Verify if uncomment this lines all of operations with angle and face can be eliminated
    #if robot.face == -1:
        #robot._coordinates.rotation = arctan2(sin(robot._coordinates.rotation - pi), cos(robot._coordinates.rotation - pi))

    # Navigation: Go-to-Goal + Avoid Obstacle Vector Field
    robot.last_univector_angle = robot.univector_angle
    robot.set_wall_obstacle()
    obst = robot.obst
    if avoid_obst: # If obstacle avoidance is activated
        if field_is_hiperbolic:                                             # Use of the Hyperbolic field
            des_theta = navigate.univec_field_h(robot, target, obst)        # Desired angle w/ go-to-goal and avoid obstacle vector field
        else:                                                               # Use of the old field
            des_theta = navigate.univec_field_n(robot, target, obst, n, d)  # Desired angle w/ go-to-goal and avoid obstacle vector field
    # Navigation: Go-to-Goal Vector Field
    else:
        if field_is_hiperbolic:                                                     # Use of the Hyperbolic field
            des_theta = navigate.hip_vec_field(robot, target)                       # Desired angle w/ go-to-goal
        else:                                                                       # Use of the old field
            des_theta = navigate.n_vec_field(robot, target, n, d, have_face=False)  # Desired angle w/ go-to-goal   
    robot.univector_angle = des_theta

    # Controller estimation
    stp_theta = approx(robot, target, avoid_obst, obst, n, d, field_is_hiperbolic) # Desired angle prediction
    #phi_v = calculate_phi_v(robot, target)
    phi_v = 0
    theta_e = which_face(robot, target, des_theta, double_face, screen_out=screen_out) # Angle error

    # Controller velocities v1, v2, v3 estimation
    v1 = (2 * robot.vMax - robot.LSimulador * k_w * sqrt(abs(theta_e))) / (2 + robot.LSimulador * abs(phi_v))
    
    if phi_v == 0:
        v2 = robot.vMax
    else:
        v2 = (sqrt(k_w ** 2 + 4 * robot.rMax * abs(phi_v)) - k_w * sqrt(abs(theta_e))) / (2 * abs(phi_v))

    if stop_when_arrive:
        v3 = k_p * robot.calculate_distance(target)
    else:
        v3 = robot.vMax

    if stop_when_arrive and robot.arrive(): # If robot needs stop when arrive target
        v = 0
        w = 0
    else:
        v = min(abs(v1), abs(v2), abs(v3))  # Controller velocities v and w
        w = v * phi_v + k_w * sign(theta_e) * sqrt(abs(theta_e))

    v, w = pid(robot, des_theta, screen_out, pos_auto)
    # Some code to store the past position, orientation and velocity

    #robot.v=v
    robot.pastPose = delete(robot.pastPose, 0, 1)  # Deleting the first column
    robot.pastPose = append(robot.pastPose, array(
        [[round(robot._coordinates.X)], [round(robot._coordinates.Y)], [round(float(robot._coordinates.rotation))], [round(float(v))]]), 1)
    return v, w


# TODO #3 Check the need for flagTrocaFace - lock the face swap in obstacle avoidance
def which_face(robot, target, des_theta, double_face, screen_out=False):
    """Input: Robot object, Target object, Desired angle, Flag to activate face swap
    Description: Defines de better face to robot movement and estimate angle error
    Output: theta_e -> Angle error (float)"""

    # If you want to test without double_face, uncomment next line
    #double_face=False
    
    robot_coordinates = robot.get_coordinates()
    
    if robot.face == 1:
        theta_e = arctan2(sin(des_theta - robot_coordinates.rotation), cos(des_theta - robot_coordinates.rotation))  # Error estimation with current face
    else:
        theta_e = arctan2(sin(des_theta - robot_coordinates.rotation + pi), cos(des_theta - robot_coordinates.rotation + pi))  # Error estimation with current face

    '''
    Conditions to switch face:
    1- Angle error (theta_e) has a high value
    2- CornerAvoid detect robot in some border
    3- All permitions of switch face bellow this
    '''
    if ( (abs(theta_e) > pi / 2 + pi / 12) or action.CornerAvoid(robot)) and (not robot.flagTrocaFace) and double_face:  # If the angle is convenient for face swap
        if robot.flagKeepFace:  # If robot not switched face recently
            robot.face = robot.face * (-1)  # Face switch
            robot_coordinates.rotation = arctan2(sin(robot_coordinates.rotation + pi), cos(robot_coordinates.rotation + pi))  # Angle re-estimate
            theta_e = arctan2(sin(des_theta - robot_coordinates.rotation), cos(des_theta - robot_coordinates.rotation))  # Error angle re-estimate
            robot.flagKeepFace = False
            robot.contKeepFace = 0
        else:
            if robot.contKeepFace > 60:  # Counter to next face switch
                robot.flagKeepFace = True
            else:
                robot.contKeepFace += 1
    return theta_e

def pid(robot, des_theta, screen_out, pos_auto):
    # Discrete Control Constants adjustables
    Kp = 4
    Kd = 0.02
    Ki = 0.0
    T0 = 1/60

    # Discrete equations constants
    q0 = Kp + Kd/T0 + Ki*T0
    q1 = -Kp -2*Kd/T0
    q2 = Kd/T0

    # Calculate the error angle theta_e
    robot_coordinates = robot.get_coordinates()
    if robot.face==1:
        theta_e = arctan2(sin(des_theta - robot_coordinates.rotation), cos(des_theta - robot_coordinates.rotation))  # Error estimation with current face
    else:
        theta_e = arctan2(sin(des_theta - robot_coordinates.rotation+pi), cos(des_theta - robot_coordinates.rotation+pi))  # Error estimation with current face

    # Discrete control law
    uk = robot.u_k1 + q0*theta_e + q1*robot.e_k1 + q2*robot.e_k2
    w = uk

    # Saturating control action - limited robot response
    saturacao = 20
    if w > saturacao:
        w = saturacao
    elif w < -saturacao:
        w = -saturacao

    # Updating control variables
    robot.e_k2 = robot.e_k1
    robot.e_k1 = theta_e
    robot.u_k1 = uk

    # Using sigmoid function to scale linear velocity during robot movimentation
    # Depreciated, but keep here for documentation
    '''
    def sigmoid(x):
        return 1/(1+exp(-x))
    
    if robot.calculate_distance(robot.target) < 10:
        limiar = 0.05*saturacao
    else:
        limiar = 0.2*saturacao

    if robot.calculate_distance(robot.target) < 20:
        fator = (max((1-abs(w)/(saturacao/2)), 0))
        fator = sigmoid(fator*12-6)
    elif robot.calculate_distance(robot.target) < 40:
        fator = (max((1-abs(w)/(saturacao/1.5)), 0))
        fator = sigmoid(fator*12-6)
    else:
        fator = 1
    fator=1

    if w > limiar:
        v = 30*robot.face*fator
    else:
        v = 30*robot.face*fator
    #'''

    # Setting limit velocities
    if screen_out:
        vmin = 40
    else:
        vmin = 30
    vmax = 60
    # Setting limit distances
    dmin = 10
    dmax = 60

    # Dot product with robot angle and vector between robot and ball
    vector_ball = [robot.target._coordinates.X-robot_coordinates.X, robot.target._coordinates.Y-robot_coordinates.Y]
    abs_vector_ball = sqrt(vector_ball[0]**2 + vector_ball[1]**2)
    vector_ball = vector_ball/abs_vector_ball

    if robot.face == 1:
        rotation = robot_coordinates.rotation
    else:
        rotation = arctan2(sin(robot_coordinates.rotation+pi), cos(robot_coordinates.rotation+pi))  # Error estimation with current face
    
    vector_robot = [cos(rotation), sin(rotation)]

    dot_product = vector_ball[0]*vector_robot[0] + vector_ball[1]*vector_robot[1]

    # Angle of this dot product
    theta_ball = arccos(dot_product)

    # If robot is alling with ball in a some time counter, it can accelerate
    if theta_ball < 30:
        if robot.contador_velocidade > 120:
            flag_acelera = True
        else:
            robot.contador_velocidade = robot.contador_velocidade + 1
            flag_acelera = False
    else:
        flag_acelera = False

    if robot.calculate_distance(robot.target) < dmin:  # Verify minimum distance to map minimum velocity
        if flag_acelera and not screen_out:
            v = 45*robot.face
        else:
            v = vmin*robot.face

    elif robot.calculate_distance(robot.target) > dmax:  # Verify max distance to map max velocity
        v = vmax*robot.face
    else:  # Linear regretion of interval [dmin, dmax] -> [vmin, vmax]
        v = vmin*robot.face + (robot.calculate_distance(robot.target)-dmin)/(dmax-dmin) *(vmax-vmin)*robot.face
    
    # If robot is in automatic positioning, it velocity is limited
    if pos_auto: v = 30
    
    return v, w

