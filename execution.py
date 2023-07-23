from numpy import cos, sin, arctan2, sqrt, sign, pi, delete, append, array

from behaviours import Univector
from corners import handle_edge_behaviour


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
    #print("delta_d: ", delta_theta_d)
    delta_x = robot._coordinates.X - robot._coordinates.last_X
    #print("delta_x: ", delta_x)
    delta_y = robot._coordinates.Y - robot._coordinates.last_Y
    #print("delta_y: ", delta_y)
    phi_V = delta_theta_d/(delta_x+0.001) * cos(robot._coordinates.rotation) + delta_theta_d/(delta_y+0.001) * sin(robot._coordinates.rotation)
    #print("Phi_v: ", phi_V)
    return phi_V

def univec_controller(robot, target, avoid_obst=True, obst=None, n=8, d=2, stop_when_arrive=False, double_face=True,
                      field_is_hiperbolic=True):
    """Input: Robot object, Target object, Flag to activate Obstacle Avoidance, Obstacle object, Constants n and d of Univector,
       Flag to activate deceleration when approaching target, Flag to activate face swap, Flag to activate Hiperbolic Field
    Description: Function to control the robot with or without obstacle avoidance
    Output: v -> Linear Velocity (float)
        w -> Angular Velocity (float)"""
    handle_edge_behaviour(robot)  # Checks if the robot is in some corner
    #double_face=False

    navigate = Univector()  # Defines the navigation algorithm
    dl = 0.000001  # Constant to approximate phi_v
    k_w = 1.7  # Feedback constant for angle error (k_w=1 means no gain)
    k_p = 1  # Proporcional constant for stopping when arrive in target (k_p=1 means no gain)

    # Target angle estimation

    # Angle correction if robot face is inverted
    if robot.face == -1:
        robot._coordinates.rotation = arctan2(sin(robot._coordinates.rotation - pi), cos(robot._coordinates.rotation - pi))

    # Navigation: Go-to-Goal + Avoid Obstacle Vector Field
    robot.last_univector_angle = robot.univector_angle
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
    phi_v = arctan2(sin(stp_theta - des_theta),     # Difference between the prediction and current angle
                    cos(stp_theta - des_theta)) / dl
    #phi_v = calculate_phi_v(robot, target)
    phi_v = 0
    theta_e = which_face(robot, target, des_theta, double_face) # Angle error

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

    #v, w = pid(robot, des_theta)
    # Some code to store the past position, orientation and velocity

    #robot.v=v
    robot.pastPose = delete(robot.pastPose, 0, 1)  # Deleting the first column
    robot.pastPose = append(robot.pastPose, array(
        [[round(robot._coordinates.X)], [round(robot._coordinates.Y)], [round(float(robot._coordinates.rotation))], [round(float(v))]]), 1)

    #print("v1: ", v1)
    #print("v2: ", v2)
    #print("v3: ", v3)
    return v, w


# TODO #3 Check the need for flagTrocaFace - lock the face swap in obstacle avoidance
def which_face(robot, target, des_theta, double_face):
    """Input: Robot object, Target object, Desired angle, Flag to activate face swap
    Description: Defines de better face to robot movement and estimate angle error
    Output: theta_e -> Angle error (float)"""
    robot_coordinates = robot.get_coordinates()
    theta_e = arctan2(sin(des_theta - robot_coordinates.rotation), cos(des_theta - robot_coordinates.rotation))  # Error estimation with current face

    if (abs(theta_e) > pi / 2 + pi / 12) and (
            not robot.flagTrocaFace) and double_face:  # If the angle is convenient for face swap
        robot.face = robot.face * (-1)  # Swaps face
        robot_coordinates.rotation = arctan2(sin(robot_coordinates.rotation + pi), cos(robot_coordinates.rotation + pi))  # Angle re-estimate
        theta_e = arctan2(sin(des_theta - robot_coordinates.rotation), cos(des_theta - robot_coordinates.rotation))  # Error angle re-estimate

    return theta_e

def pid(robot, des_theta):
    robot_coordinates = robot.get_coordinates()
    #target_coordinates = target.get_coordinates()
    #des_theta = target_coordinates.rotation
    theta_e = arctan2(sin(des_theta - robot_coordinates.rotation), cos(des_theta - robot_coordinates.rotation))  # Error estimation with current face
    de = (theta_e- robot.last_theta)/(1/60)
    robot.theta_e = theta_e
    robot.int_theta_e += robot.theta_e

    #print("Erro: ", theta_e*180/pi)
    Kp = 1
    Ki = 0
    Kd = 0.000
    saturacao = 6
    w = Kp*theta_e + Ki*robot.int_theta_e + Kd*de
    if w > saturacao:
        w = saturacao
    elif w < -saturacao:
        w = -saturacao
    print("w: ", w)
    w = w#*robot.face
    v = 20#*robot.face
    robot.last_theta = theta_e
    return v, w


