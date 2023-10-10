from numpy import pi, cos, sin, tan, arctan2, sqrt, deg2rad

import simClasses
import strategy
from execution import univec_controller, pid
import json


def stop(robot: simClasses.Robot):
    """Input: Robot object
    Description: Stops the robot.
    Output: None"""
    robot.sim_set_vel(0, 0)


def shoot(robot: simClasses.Robot, ball: simClasses.Ball, left_side=True):
    """Input: Robot object, ball object, side of field (True = Left, False = Right),
     other robots objects (2 friend , 3 opponents)
    Description: The robot moves to the middle of the desired goal, the orientation is based on a line
                 between the position of the ball and the goal.
    Output: None"""
    arrival_angle = calculate_arrival_angle(ball, left_side)
    arrival_angle = 0
    linear_velocity, angular_velocity = calculate_velocities(ball, robot)

    robot.target.set_coordinates(ball._coordinates.X, ball._coordinates.Y, arrival_angle)
    robot.sim_set_vel(linear_velocity, angular_velocity)


# TODO dar um jeito nessas funções extraídas
def calculate_velocities(ball: simClasses.Ball, robot: simClasses.Robot, double_face=True):
    #friends = [None, None]
    friends = robot.get_friends()
    """Calculates the angular and linear velocities with the univec_controller function"""
    if friends[0] is None and friends[1] is None:  # No friends to avoid
        linear_velocity, angular_velocity = univec_controller(robot, robot.target, avoid_obst=False, n=16,
                                                              d=2, double_face=double_face)  # Calculate linear and angular velocity
    else:  # Both friends to avoid
        #robot.obst.update2(ball, robot.get_friends(), robot.get_enemies())
        robot.obst.update2(ball)
        linear_velocity, angular_velocity = univec_controller(robot, robot.target, avoid_obst=True, obst=robot.obst, n=4, d=4, double_face=True)
        #print("X: ", robot.obst._coordinates.X, end=' ')
        #print("Y: ", robot.obst._coordinates.Y)
    return linear_velocity, angular_velocity


def calculate_arrival_angle(ball: simClasses.Ball, left_side):
    ball_coordinates = ball.get_coordinates()
    if left_side:  # Playing on the left side of field
        arrival_angle = arctan2(65 - ball_coordinates.Y,
                                160 - ball_coordinates.X)  # Angle between the ball and point (150,65)
    else:  # Playing on the right side of field
        arrival_angle = arctan2(65 - ball_coordinates.Y,
                                10 - ball_coordinates.X)  # Angle between the ball and point (0,65)
    return arrival_angle


def shoot2(robot: simClasses.Robot, ball: simClasses.Ball, left_side=True):
    """Input: Robot object, ball object, side of field (True = Left, False = Right), other robots objects
     (2 friend , 3 opponents)
    Description: The robot moves to the desired goal, the orientation is based on position of the ball and the goal.
                 If the Y ball position is between 45 and 85, the arrive angle is 0, otherwise is based on line
                 between the position of the ball and the edge of goal (This function is not used).
    Output: None"""
    ball_coordinates = ball.get_coordinates()
    arrival_angle = calculate_arrival_angle_alternate(ball, left_side)
    linear_velocity, angular_velocity = calculate_velocities(ball, robot)

    robot.target.set_coordinates(ball_coordinates.X, ball_coordinates.Y, arrival_angle)
    robot.sim_set_vel(linear_velocity, angular_velocity)


def calculate_arrival_angle_alternate(ball: simClasses.Ball, left_side):
    ball_coordinates = ball.get_coordinates()
    if left_side:  # Playing in the left side of field
        if (ball_coordinates.Y > 45) and (ball_coordinates.Y < 85):  # arrive with the angle 0
            arrival_angle = 0
        elif ball_coordinates.Y <= 45:
            # Y and angle target changes depending on the position of the ball, with the biggest difference
            y = 45 + (45 - ball_coordinates.Y) / (45 - 0) * 20
            # the greater the slope, in this way making a more aggressive move to the goal
            arrival_angle = arctan2(y - 45, 160 - ball_coordinates.X)
        else:
            y = 85 - (ball._coordinates.Y - 85) / (130 - 85) * 20
            arrival_angle = arctan2(y - 85, 160 - ball_coordinates.X)
    else:  # Playing in the right side of field
        if (ball_coordinates.Y > 45) and (ball_coordinates.Y < 85):
            arrival_angle = pi
        elif ball_coordinates.Y <= 45:
            y = 45 + (45 - ball_coordinates.Y) / (45 - 0) * 20
            arrival_angle = arctan2(y - 45, 10 - ball._coordinates.X)
        else:
            y = 85 - (ball._coordinates.Y - 85) / (130 - 85) * 20
            arrival_angle = arctan2(y - 85, 10 - ball._coordinates.X)
    return arrival_angle


def defender_spin(robot: simClasses.Robot, ball: simClasses.Ball, left_side=True):
    """Input: Robot object, ball object, side of field (True = Left, False = Right), other robots objects (2 friend ,
     3 opponents)
    Description: The robot moves to the ball at an angle to move it away from the friendly goal, and try to carry the
     for the anemys goal(This is used as a main move strategy for the robots)
    Output: None"""
    ball_coordinates = ball.get_coordinates()
    #arrival_angle = calculate_arrival_angle_defender_spin(ball, left_side)
    arrival_angle = calculate_arrival_angle_alternate(ball, left_side)

    # Teste para cantos
    if left_side:
        if ball_coordinates.Y > 120:
            arrival_angle = 45*pi/180
        elif ball_coordinates.Y < 10:
            arrival_angle = -45*pi/180
    else:
        if ball_coordinates.Y > 120:
            arrival_angle = 135*pi/180
        elif ball_coordinates.Y < 10:
            arrival_angle = -135*pi/180
    
    #arrival_angle=0
    robot.target.set_coordinates(ball_coordinates.X, ball_coordinates.Y, arrival_angle)

    linear_velocity, angular_velocity = calculate_velocities(ball, robot)

    distance_ball_robot = robot.calculate_distance(ball)  # Calculate distance between ball and robot
    linear_velocity, angular_velocity = try_corner_spin_defender_spin(ball, robot, distance_ball_robot,
                                                                      linear_velocity, angular_velocity)

    # Check if the distance is lower than a threshold and if the ball is on the right of robot
    if not check_forward_advance_possible(ball, distance_ball_robot, robot):
        robot.sim_set_vel(linear_velocity, angular_velocity)
        #robot.sim_set_vel(0, 0)
        return
    robot.sim_set_vel2(80 * robot.face, 80 * robot.face)  # Send the velocity of right and left wheel
    #robot.sim_set_vel(linear_velocity, angular_velocity)


def check_forward_advance_possible(ball: simClasses.Ball, distance_ball_robot, robot: simClasses.Robot):
    robot_coordinates = robot.get_coordinates()
    ball_coordinates = ball.get_coordinates()
    if distance_ball_robot < 20:
        #print("Distancia OK")

        if check_flag_velocity(ball, robot):
            #print("Check OK")
            x_goal_projection = calculate_x_goal_projection(ball, robot)
            y_goal_projection = calculate_y_goal_projection(robot, x_goal_projection)
            if robot.face == 1:
                theta = robot_coordinates.rotation
            else:
                theta = arctan2(sin(robot_coordinates.rotation + pi),
                        cos(robot_coordinates.rotation + pi))  # Angle between the ball and point (0,65)
            if 45 < y_goal_projection < 85:
                #print("Projecao OK")
                x_projection = robot_coordinates.X + distance_ball_robot * cos(theta)
                y_projection = robot_coordinates.Y + distance_ball_robot * sin(theta)
                distance_ball_projection = sqrt(
                    (ball_coordinates.X - x_projection) ** 2 + (ball_coordinates.Y - y_projection) ** 2)
                #print("Distancia: ", distance_ball_projection)
                if (robot.index == 2 or robot.index == 1) and (distance_ball_projection < 4):
                    print("ZUUUUUUUUUUUUUM")
                    return True

    return False


def calculate_y_goal_projection(robot: simClasses.Robot, x_goal_projection):
    robot_coordinates = robot.get_coordinates()
    if robot.face == 1:
        theta = robot_coordinates.rotation
    else:
        theta = arctan2(sin(robot_coordinates.rotation + pi),
                        cos(robot_coordinates.rotation + pi))
    y_goal_projection = tan(theta) * x_goal_projection + robot_coordinates.Y
    return y_goal_projection


def check_flag_velocity(ball: simClasses.Ball, robot: simClasses.Robot):
    ball_coordinates = ball.get_coordinates()
    robot_coordinates = robot.get_coordinates()
    if robot.teamYellow and ball_coordinates.X < robot_coordinates.X:
        return True
    elif not robot.teamYellow and ball_coordinates.X > robot_coordinates.X:
        return True
    return False


def calculate_x_goal_projection(ball: simClasses.Ball, robot: simClasses.Robot):
    ball_coordinates = ball.get_coordinates()
    robot_coordinates = robot.get_coordinates()
    if robot.teamYellow and ball_coordinates.X < robot_coordinates.X:
        x_goal_projection = 15 - robot_coordinates.X
        return x_goal_projection
    if not robot.teamYellow and ball_coordinates.X > robot_coordinates.X:
        x_goal_projection = 160 - robot_coordinates.X
        return x_goal_projection


def try_corner_spin_defender_spin(ball: simClasses.Ball, robot: simClasses.Robot, distance_ball_robot, linear_velocity,
                                  angular_velocity):
    # TODO arrumar isso urgente
    # Check if the flag spin is true and if distance is lower than a threshold
    robot_coordinates = robot.get_coordinates()
    w = 16
    if robot.spin and distance_ball_robot < 10:
        if not robot.teamYellow:
            '''
            Define the direction of rotation, the direction changes based on northern
            and southern hemisphere, in the North hemisphere the direction is clockwise
            and the South hemisphere is anti-clockwise.
            '''
            if robot._coordinates.X < ball._coordinates.X:
                if robot_coordinates.Y > 65:
                    linear_velocity = 0
                    angular_velocity = -w
                else:
                    linear_velocity = 0
                    angular_velocity = w
        elif robot._coordinates.X < ball._coordinates.X:
            if robot_coordinates.Y > 65:
                linear_velocity = 0
                angular_velocity = w
            else:
                linear_velocity = 0
                angular_velocity = -w
    return linear_velocity, angular_velocity


def calculate_arrival_angle_defender_spin(ball: simClasses.Ball, left_side):
    ball_coordinates = ball.get_coordinates()
    if left_side:  # Playing on the left side of field
        arrival_angle = arctan2(65 - ball_coordinates.Y,
                                160 - ball_coordinates.X)  # Angle between the ball and point (150,65)
    else:  # Playing on the right side of field
        arrival_angle = arctan2(65 - ball_coordinates.Y,
                                10 - ball_coordinates.X)  # Angle between the ball and point (0,65)
    return arrival_angle


def screen_out_ball(robot: simClasses.Robot, ball: simClasses.KinematicBody, static_point, left_side=True, upper_lim=200,
                    lower_lim=0):
    """Input: Robot object, ball object, point to project the ball, side of field (True = Left, False = Right), moviment limits(upper and lower), other robots objects (2 friend)
    Description: Project ball Y position to the selected X point.
    Output: None"""
    ball_coordinates = ball.get_coordinates()
    ball_velocities = ball.get_velocities()
    # Predict ball position multiples frames ahead (Possible conflit with other ball prediction)
    # If ball position is out of limits of Y axis, set the value to the limits
    ball_y_prediction = ball_coordinates.Y + ball._velocities.Y * 100 * 22 / 60
    ball_y_target = min(ball_y_prediction, upper_lim)
    ball_y_target = max(ball_y_target, lower_lim)

    arrival_angle = calculate_arrival_angle_screenout(ball_y_prediction, left_side, robot)
    if left_side:
        robot.target.set_coordinates(static_point, ball_y_target, arrival_angle)
    else:
        robot.target.set_coordinates(170 - static_point, ball_y_target, arrival_angle)

    if robot.contStopped > 60:  # Check if the robot is locked on the corner, and try to free him
        linear_velocity, angular_velocity = escape_from_corner_lock(robot)
    else:
        linear_velocity, angular_velocity = calculate_velocities_screenout(robot)

    if robot.calculate_distance(robot.target) < 5:
        linear_velocity = 0

    robot.sim_set_vel(linear_velocity, angular_velocity)


def calculate_velocities_screenout(robot: simClasses.Robot):
    friends = robot.get_friends()
    #friends=[None, None]
    if friends[0] is None and friends[1] is None:  # No friends to avoid
        linear_velocity, angular_velocity = univec_controller(robot, robot.target, avoid_obst=False,
                                                              stop_when_arrive=True, screen_out=True)  # Calculate linear and angular velocity
    else:  # Both friends to avoid
        robot.obst.update()
        if robot.calculate_distance(robot.target) > 15:
            avoid_obst = True
        else:
            avoid_obst = False
        linear_velocity, angular_velocity = univec_controller(robot, robot.target, avoid_obst, robot.obst,
                                                              stop_when_arrive=True, screen_out=True)
    return linear_velocity, angular_velocity


def escape_from_corner_lock(robot: simClasses.Robot):
    robot_coordinates = robot.get_coordinates()
    if robot.teamYellow:
        if abs(robot_coordinates.rotation) < 10:
            linear_velocity = -30
            angular_velocity = 5
        else:
            linear_velocity = 30
            angular_velocity = -5
    else:
        if abs(robot_coordinates.rotation) < 10:
            linear_velocity = -30
            angular_velocity = 0
        else:
            linear_velocity = 30
            angular_velocity = 0

    return linear_velocity, angular_velocity


def calculate_arrival_angle_screenout(ball_y_prediction, left_side, robot: simClasses.Robot):
    robot_coordinates = robot.get_coordinates()
    if left_side:
        if robot_coordinates.Y <= ball_y_prediction:  # Define the arrival angle based on the side of the field
            arrival_angle = pi / 2
        else:
            arrival_angle = -pi / 2

    else:
        if robot_coordinates.Y <= ball_y_prediction:
            arrival_angle = pi / 2
        else:
            arrival_angle = -pi / 2
    return arrival_angle


def goal_keeper_defender(robot: simClasses.Robot, ball: simClasses.Robot, left_side=True):
    """Input: Robot object, ball object, side of field (True = Left, False = Right), other robots objects (2 friends, 3 opponents)
    Description: The robot pushes the ball away from the goal and make him spin.
    Output: None"""
    ball_coordinates = ball.get_coordinates()
    arrival_angle = calculate_arrival_angle_defence(ball, left_side)
    robot.target.set_coordinates(ball_coordinates.X, ball_coordinates.Y, arrival_angle)

    linear_velocity, angular_velocity = calculate_velocities_defence(robot)

    if robot.calculate_distance(ball) < 10:  # Check if the distance is lower than a threshold

        angular_velocity, linear_velocity = spin_goalkeeper(angular_velocity, linear_velocity, robot)

    robot.sim_set_vel(linear_velocity, angular_velocity)


def spin_goalkeeper(angular_velocity, linear_velocity, robot: simClasses.Robot):
    """Define the direction of rotation, the direction changes based on northern
    and southern hemisphere, in the North hemisphere the direction is clockwise
    and the South hemisphere is anticlockwise."""
    if not robot.teamYellow:
        if robot._coordinates.Y > 65:
            linear_velocity = 0
            angular_velocity = -30
        else:
            linear_velocity = 0
            angular_velocity = 30
    else:
        if robot._coordinates.Y > 65:
            linear_velocity = 0
            angular_velocity = 30
        else:
            linear_velocity = 0
            angular_velocity = -30
    return angular_velocity, linear_velocity


def calculate_velocities_defence(robot: simClasses.Robot):
    friends = robot.get_friends()
    if friends[0] is None and friends[1] is None:  # No friends to avoid
        linear_velocity, angular_velocity = univec_controller(robot, robot.target, avoid_obst=False, n=16, d=2)
    else:  # Both friends to avoid
        robot.obst.update()
        linear_velocity, angular_velocity = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)
    return linear_velocity, angular_velocity


def calculate_arrival_angle_defence(ball, left_side):
    if left_side:
        arrival_angle = arctan2(ball._coordinates.Y - 65,
                                ball._coordinates.X - 10)  # Angle between the ball and point (150,65)
    else:
        arrival_angle = arctan2(ball._coordinates.Y - 65,
                                ball._coordinates.X - 160)  # Angle between the ball and point (0,65)
    return arrival_angle


def protect_goal(robot: simClasses.Robot, ball: simClasses.Ball, r, left_side=True):
    """Input: Robot object, ball object, radius of circumference, side of field (True = Left, False = Right),
     other robots objects (2 friend)
    Description: The robot does a semi-circumference around the goal.
    Output: None"""
    ball_coordinates = ball.get_coordinates()
    robot_coordinates = robot.get_coordinates()
    friends = robot.get_friends()
    if left_side:
        angle = arctan2((ball_coordinates.Y - 65), (ball_coordinates.X - 15))  # Calculate angle of vector goal and ball

        if pi / 2 >= angle >= (-pi / 2):  # project the ball into the circumference

            proj_x = r * cos(angle) + 15
            proj_y = r * sin(angle) + 65

        else:

            proj_x = -r * cos(angle) + 15
            proj_y = r * sin(angle) + 65

        '''
        Defines the arrival angle, the angle changes based on the ball's relative
        position in relation to the robot, it is necessary to choose the arrival angle
        that generates the smoothest movement to make the semi-circle movement
        '''
        if robot_coordinates.Y > 100:
            if robot_coordinates.X < ball_coordinates.X:
                arrival_angle = -(pi / 2 - angle)

            if robot_coordinates.X >= ball_coordinates.X:
                arrival_angle = (pi / 2 + angle)

        if 100 >= robot_coordinates.Y > 65:
            if robot_coordinates.Y < ball_coordinates.Y:
                arrival_angle = (pi / 2 + angle)
            if robot_coordinates.Y >= ball_coordinates.Y:
                arrival_angle = -(pi / 2 - angle)

        if 65 >= robot_coordinates.Y > 30:
            if robot_coordinates.Y < ball._coordinates.Y:
                arrival_angle = pi / 2 + angle
            if robot._coordinates.Y >= ball._coordinates.Y:
                arrival_angle = -(pi / 2 - angle)

        if robot._coordinates.Y <= 30:
            if robot._coordinates.X < ball._coordinates.X:
                arrival_angle = pi / 2 + angle

            if robot._coordinates.X >= ball._coordinates.X:
                arrival_angle = -(pi / 2 - angle)

    arrival_angle = arctan2(sin(arrival_angle), cos(arrival_angle))
    robot.target._coordinates.update()

    if friends[0] is None and friends[1] is None:  # No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, stop_when_arrive=True)
    else:  # Both friends to avoid
        robot.obst.update()
        v, w = univec_controller(robot, robot.target, True, robot.obst, stop_when_arrive=True)

    robot.sim_set_vel(v, w)


def girar(robot: simClasses.Robot, v1, v2):
    """Input: Robot object, ball object, Velocity of Right and Left wheel
    Description: The robot spins around it's own axis
    Output: None"""
    robot.sim_set_vel2(v1, v2)


def defender_penalty(robot: simClasses.Robot, ball: simClasses.Ball, left_side=True):
    """Input: Robot object, ball object, side of field (True = Left, False = Right), other robots objects (2 friend, 3 opponents)
    Description: Makes the goalkepper go straight to the ball to defend the penalty
    Output: None"""

    arrival_angle = calculate_arrival_angle_defence(ball, left_side)
    ball_coordinates = ball.get_coordinates()
    robot.target.set_coordinates(ball_coordinates.X, ball_coordinates.Y, arrival_angle)

    linear_velocity, angular_velocity = calculate_velocities_defence(robot)

    robot.sim_set_vel(linear_velocity, angular_velocity)


def defender_penalty_spin(robot: simClasses.Robot, ball: simClasses.Ball, left_side=True):
    enemies = robot.get_enemies()

    kicker = determine_enemy_kicker(ball, enemies)

    arrival_angle, proj_x, proj_y = calculate_arrival_theta_defender_spin(ball, kicker, left_side, robot)

    robot.target.set_coordinates(proj_x, proj_y, arrival_angle)

    angular_velocity, linear_velocity = calculate_velocities_defender(robot)

    if robot.calculate_distance(robot.target) < 6:
        if left_side:
            # if robot.arrive():
            linear_velocity = 0
            if robot._coordinates.Y > 65:
                angular_velocity = -30
            else:
                angular_velocity = 30
        else:
            linear_velocity = 0
            if robot._coordinates.Y > 65:
                angular_velocity = 30
            else:
                angular_velocity = -30

    robot.sim_set_vel(linear_velocity, angular_velocity)


def calculate_velocities_defender(robot):
    friends = robot.get_friends()
    print("Defender Spin")
    if friends[0] is None and friends[1] is None:  # No friends to avoid
        linear_velocity, angular_velocity = univec_controller(robot, robot.target, avoid_obst=False, n=16, d=2)
    else:  # Both friends to avoid
        robot.obst.update()
        linear_velocity, angular_velocity = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)
    return angular_velocity, linear_velocity


def calculate_arrival_theta_defender_spin(ball, kicker, left_side, robot):
    angle = arctan2(ball._coordinates.Y - kicker._coordinates.Y, ball._coordinates.X - kicker._coordinates.X)
    phi = pi - angle
    if left_side:
        dx = kicker._coordinates.X - 14
        dy = dx * tan(phi)

        proj_y = kicker._coordinates.Y + dy
        proj_x = 14
        if proj_y > 80:
            proj_y = 80
        elif proj_y < 50:
            proj_y = 50
        if proj_y > robot._coordinates.Y:
            arrival_angle = pi / 2
        else:
            arrival_angle = -pi / 2
        return arrival_angle, proj_x, proj_y

    dx = 156 - kicker._coordinates.X
    dy = dx * tan(angle)

    proj_y = kicker._coordinates.Y + dy
    proj_x = 156
    if proj_y > 80:
        proj_y = 80
    elif proj_y < 50:
        proj_y = 50
    if proj_y > robot._coordinates.Y:
        arrival_angle = pi / 2
    else:
        arrival_angle = -pi / 2
    return arrival_angle, proj_x, proj_y


def determine_enemy_kicker(ball, enemies):
    distance = 200
    index_enemy = 0
    for index, enemy in enumerate(enemies):
        distance_enemy_ball = enemy.calculate_distance(ball)
        if distance_enemy_ball < distance:
            distance = distance_enemy_ball
            index_enemy = index
    kicker = enemies[index_enemy]
    return kicker


def attacker_penalty_spin(robot: simClasses.Robot, ball: simClasses.Robot):
    if not robot.calculate_distance(ball) < 9:  # If the attacker is not closer to the ball
        girar(robot, 100, 100)  # Moving forward
    else:
        if robot.teamYellow:  # Team verification
            if robot.get_coordinates().Y < 65:
                girar(robot, 0, 100)  # Shoots the ball spinning up
            else:
                girar(robot, 100, 0)  # Shoots the ball spinning down
        else:
            if robot.get_coordinates().Y > 65:
                girar(robot, 0, 100)  # Shoots the ball spinning down
            else:
                girar(robot, 100, 0)  # Shoots the ball spinning up


def attack_penalty(robot):
    if robot.teamYellow:
        girar(robot, -10, -10)
    else:
        girar(robot, -10, -10)

def attacker_penalty_switch(robot):
    girar(robot, -10, -10)


def attacker_penalty_direct(robot, ball, left_side=True):
    """Input: Robot object, ball object, side of field (True = Left, False = Right), other robots objects (2 friend, 3 opponents)
    Description: Positions the robot to take the penalty, it is positioned and moves to go towards the corners of the goal.
    Output: None"""
    friends = robot.get_friends()
    arrival_angle = calculate_arrival_angle_attack_penalty(left_side, robot)

    #robot.target.set_coordinates(ball._coordinates.X, ball._coordinates.Y, arrival_angle)
    #linear_velocity, angular_velocity = calculate_velocities_defender(robot)

    if robot.teamYellow:
        girar(robot,40,30)
    else:
        girar(robot,40,30)

    #robot.sim_set_vel(linear_velocity, angular_velocity)


def calculate_arrival_angle_attack_penalty(left_side, robot):
    if left_side:
        # The arrival angle changes based on the position, and the position has 2 random possibilities
        if robot._coordinates.Y > 65:
            arrival_angle = -deg2rad(15)
        else:
            arrival_angle = deg2rad(15)
    else:
        if robot._coordinates.Y > 65:
            arrival_angle = -deg2rad(165)
        else:
            arrival_angle = deg2rad(165)
    return arrival_angle


def defender_penalty_spin_proj_vel(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None):

    if abs(ball._velocities.X) < 0.01:
        v = 0
        w = 0

    else:

        theta = arctan2(ball._velocities.Y, ball._velocities.X)
        phi = pi - theta

        if left_side:
            dx = ball._coordinates.X - 14
            dy = dx*tan(phi)

            proj_y = ball._coordinates.Y + dy
            proj_x = 14
            if proj_y > 80:
                proj_y = 80
            elif proj_y < 50:
                proj_y = 50
            if proj_y > robot._coordinates.Y:
                arrival_theta = pi/2
            else:
                arrival_theta = -pi/2

        else:
            dx = 156 - ball._coordinates.X
            dy = dx*tan(theta)

            proj_y = ball._coordinates.Y + dy
            proj_x = 156
            if proj_y > 80:
                proj_y = 80
            elif proj_y < 50:
                proj_y = 50
            if proj_y > robot._coordinates.Y:
                arrival_theta = pi/2
            else:
                arrival_theta = -pi/2

        robot.target.set_coordinates(proj_x, proj_y, arrival_theta)

        v, w = calculate_velocities_defender(robot)

        if robot.calculate_distance(robot.target) < 7:
            if left_side:
                v = 0
                if robot._coordinates.Y > 65:
                    w = 30
                else:
                    w = -30
            else:
                v = 0
                if robot._coordinates.Y > 65:
                    w = -30
                else:
                    w = 30

    robot.sim_set_vel(v, w)

def play_follower(robot_follower: simClasses.Robot, robot_leader: simClasses.Robot, ball: simClasses.Ball,
             robot0: simClasses.Robot = None):
    """Input: Robot object (All team members), ball object, other robots objects (3 opponents)
    Description: Defines the position of follower robot based on the leader position.
    Output: None"""

    proj_x, proj_y = project_coordinates(robot_leader)

    # Calculate distance between the follower and the projected point

    dist = sqrt((robot_follower._coordinates.X - proj_x) ** 2 + (robot_follower._coordinates.Y - proj_y) ** 2)
    arrival_angle = arctan2(ball._coordinates.Y - robot_follower._coordinates.Y,
                            ball._coordinates.X - robot_follower._coordinates.X)
    robot_follower.target.set_coordinates(proj_x, proj_y, arrival_angle)

    if dist < 10:  # Check if the robot is close to the projected point and stops the robot
        stop(robot_follower)
        return

    # No friends to avoid
    linear_velocity, angular_velocity = calculate_follower_velocities(robot0, robot_follower, robot_leader)

    robot_follower.sim_set_vel(linear_velocity, angular_velocity)


def calculate_follower_velocities(robot0: simClasses.Robot, robot_follower: simClasses.Robot, robot_leader: simClasses.Robot):
    enemies = robot_follower.get_enemies()
    if robot0 is None and enemies[0] is None and enemies[1] is None and enemies[2] is None:
        linear_velocity, angular_velocity = univec_controller(robot_follower, robot_follower.target, avoid_obst=False, n=16, d=2)
    else:  # Both friends to avoid
        robot_follower.obst.update()
        linear_velocity, angular_velocity = univec_controller(robot_follower, robot_follower.target, True,
                                                              robot_follower.obst, n=4, d=4)
    return linear_velocity, angular_velocity


def project_coordinates(robot_leader):
    """Input: Robot object
    Description: Calculates the projected coordinates of the robot.
    Output: Projected coordinates"""
    robot_leader_coordinates = robot_leader.get_coordinates()
    if robot_leader_coordinates.Y > 65:
        if robot_leader_coordinates.X > 75:
            proj_x = robot_leader_coordinates.X - (15)
            proj_y = robot_leader_coordinates.Y - (30+10)
        else:
            proj_x = robot_leader_coordinates.X + (15)
            proj_y = robot_leader_coordinates.Y - (15+10)
    else:
        if robot_leader_coordinates.X > 75:
            proj_x = robot_leader_coordinates.X - (15)
            proj_y = robot_leader_coordinates.Y + (30+10)
        else:
            proj_x = robot_leader_coordinates.X + (15)
            proj_y = robot_leader_coordinates.Y + (15+10)
    return proj_x, proj_y


def follow_leader(robot1: simClasses.Robot, robot2: simClasses.Robot, ball: simClasses.Ball,
                  strategy_controller):
    """Input: Robot object (All team members), ball object, other robots objects (3 opponents)
    Description: Defines the strategy of 2 attackers, the leader and what each robot needs to do in each situation.
    Output: None"""
    ball_coordinates = ball.get_coordinates()
    leader, follower = select_leader(robot1, robot2, ball, strategy_controller)

    leader_coordinates = leader.get_coordinates()
    follower_coordinates = follower.get_coordinates()

    if not follower.teamYellow:
        # If ball is on the defence side the leader does the screen out, and the follower follows his moves.
        if (ball_coordinates.X < 30) and (110 > ball_coordinates.Y > 30):
            if follower_coordinates.X < 30:
                screen_out_ball(leader, leader, 55, left_side=not leader.teamYellow, upper_lim=120, lower_lim=10)
            else:
                screen_out_ball(leader, ball, 55, left_side=not leader.teamYellow, upper_lim=120, lower_lim=10)
            play_follower(follower, leader, ball)

        else:  # If ball is on the attack side the leader does the defender spin, and the follower follows his moves.
            defender_spin(leader, ball, left_side=not leader.teamYellow)
            # If the follower is close enough to the ball, it starts to do the defender spin.
            if follower.calculate_distance(ball) < 20 and \
                    not ((leader_coordinates.X > 140) and (100 > leader_coordinates.Y > 40)):
                defender_spin(follower, ball, left_side=not follower.teamYellow)
                return

            play_follower(follower, leader, ball)
        return
    # Same Idea but for the other side of de field
    if follower.teamYellow:
        if (ball_coordinates.X > 130) and (110 > ball_coordinates.Y > 30):
            if follower_coordinates.X > 130:
                screen_out_ball(leader, leader, 55, left_side=not leader.teamYellow, upper_lim=120, lower_lim=10)
            else:
                screen_out_ball(leader, ball, 55, left_side=not leader.teamYellow, upper_lim=120, lower_lim=10)
            play_follower(follower, leader, ball)

        else:
            defender_spin(leader, ball, left_side=not leader.teamYellow)
            if follower.calculate_distance(ball) < 20 and \
                    not ((leader_coordinates.X < 35) and (100 > leader_coordinates.Y > 40)):
                defender_spin(follower, ball, left_side=not follower.teamYellow)
                return

            play_follower(follower, leader, ball)


def select_leader(robot1: simClasses.Robot, robot2: simClasses.Robot, ball: simClasses.Ball, strategy_controller):
    """Input: Distance of the robots to the ball, robot objects
    Description: Defines which robot is the leader and who is the follower
    Output: None"""
    leader = strategy_controller.get_leader()
    follower = strategy_controller.get_follower()
    leader_time = strategy_controller.get_leader_time()
    distance1_to_ball = robot1.calculate_distance(ball)
    distance2_to_ball = robot2.calculate_distance(ball)

    if distance2_to_ball < distance1_to_ball:  # Strategy if robot 2 is closer to the ball
        if leader is None and follower is None:
            leader = robot2
            follower = robot1

        else:
            if leader_time > 60 and leader is robot1:
                leader = robot2
                follower = robot1
                leader_time = 0

        leader_time += 1

    # Same idea, but robot 1 is closer to the ball
    else:
        if leader is None and follower is None:
            leader = robot1
            follower = robot2

        else:
            if leader_time > 60 and leader is robot2:
                leader = robot1
                follower = robot2
                leader_time = 0

        leader_time += 1

    strategy_controller.set_leader(leader)
    strategy_controller.set_follower(follower)
    strategy_controller.set_leader_time(leader_time)
    return leader, follower

def rectangle(robot: simClasses.Robot, double_face=False):
    '''
        4          3

        1          2
    '''
    #posicoes_x = [47.5, 122.5, 122.5, 47.5]
    #posicoes_y = [25, 25, 105, 105]
    #posicoes_angulo = [-90*pi/180, 0, 90*pi/180, 180*pi/180]

    '''
        1             5
               2/6       4
        7             3
    '''
    #posicoes_x = [47.5, 85, 122.5, 142, 122.5, 85, 47.5]
    #posicoes_y = [105, 65, 25, 65, 105, 65, 25]
    #posicoes_angulo = [90*pi/180, -45*pi/180, 0, 90*pi/180, 180*pi/180, -135*pi/180, -135*pi/180]

    '''
        2             3/6
                    
        1/4             5
    '''
    posicoes_x = [47.5, 47.5, 122.5, 47.5, 122.5, 122.5]
    posicoes_y = [25, 105, 105, 25, 25, 105]
    posicoes_angulo = [-135*pi/180, 90*pi/180, 0, -135*pi/180, 0*pi/180, 90*pi/180]

    n_points = len(posicoes_x)

    robot.target.set_coordinates(posicoes_x[robot.stateRetangle%n_points], 
                                 posicoes_y[robot.stateRetangle%n_points], 
                                 posicoes_angulo[robot.stateRetangle%n_points])
    
    if robot.calculate_distance(robot.target) < 5:
        robot.stateRetangle += 1
    
    #print("Indice alvo: ", robot.stateRetangle%4)

    linear_velocity, angular_velocity = calculate_velocities(robot.target, robot, double_face)

    coordinates = robot.get_coordinates()

    #print(coordinates.rotation )
    if coordinates.Y < 7.5 and -pi/2 -pi/12 < coordinates.rotation < -pi/2 +pi/12:
        print("[PRESO] Baixo")
        linear_velocity = -30*robot.face
        angular_velocity = 0
    elif coordinates.Y > 122 and pi/2 -pi/15 < coordinates.rotation < pi/2 +pi/15:
        print("[PRESO] Cima")
        linear_velocity = -30*robot.face
        angular_velocity = 0
    elif coordinates.X > 150 and -pi/15 < coordinates.rotation < +pi/15:
        print("[PRESO] Esquerda")
        linear_velocity = -30*robot.face
        angular_velocity = 0
    elif coordinates.X < 20 and (pi-pi/15 < coordinates.rotation or coordinates.rotation > -pi+pi/15):
        print("[PRESO] Direita")
        linear_velocity = -30*robot.face
        angular_velocity = 0

    robot.sim_set_vel(linear_velocity, angular_velocity)


def CornerAvoid(robot:simClasses.Robot):
    xUperLimit = 145
    xLowerLimit = 25

    yUperLimit = 110
    yLowerLimit = 20

    if robot.face == 1:
        robotAngle = robot._coordinates.rotation# Radianos
    else:
        robotAngle = arctan2(sin(robot._coordinates.rotation + pi), 
                             cos(robot._coordinates.rotation + pi))
    robotPos = (robot._coordinates.X,robot._coordinates.Y) # X, Y
    
    border = False

    # Condicao para estar preso na parede do lado esquerdo
    if robotPos[0]<=xLowerLimit and ((robotAngle> deg2rad(180-30)) or (robotAngle< deg2rad(-180+30))):
        #print("Preso no lado esquerdo")
        border = True

    # Condicao para estar preso na parede do lado direito
    elif robotPos[0]>=xUperLimit and (robotAngle>deg2rad(-30) and robotAngle<deg2rad(30)):
        #print("Preso no lado Direito")
        border = True

    # Condicao para estar preso na parede de baixo
    elif robotPos[1]<=yLowerLimit and (robotAngle<deg2rad(-90+30) and robotAngle>deg2rad(-90-30)):
        #print("Preso na parede de Baixo")
        border = True

    # Condicao para estar preso na parede de cima
    elif robotPos[1]>=yUperLimit and (robotAngle>deg2rad(90-30) and robotAngle<deg2rad(+90+30)):
        #print("Preso na parede de Cima")
        border = True
    
    if border:
        #print("Entrei")
        if robot.contWall > 15:
            #print("TROQUE IMEDIATAMENTE")
            return True
        else:
            #print("Contei")
            robot.contWall+=1
            
    else:
        robot.contWall=0
        return False



    return

def go_to_point(robot:simClasses.Robot, x:float, y:float, theta:float):
    robot.target.set_coordinates(x,y,theta)
    linear_velocity, angular_velocity = calculate_velocities(robot.target, robot)

    if robot.arrive():
        stop(robot)
    else:
        robot.sim_set_vel(linear_velocity, angular_velocity)

def SendRobotPosition(mray, ref_data, number_robot, file, if_else = None):
    """
    FREE_KICK = 0
    PENALTY_KICK = 1
    GOAL_KICK = 2
    FREE_BALL = 3
    KICKOFF = 4 
    STOP = 5
    GAME_ON = 6
    HALT = 7    
    """
    file_name = "fouls_foulder/positions/" + file + '.json'
    
    with open(file_name) as f:
        data = json.load(f)

    side = ''
    offensive_defensive_quadrant = ''
    list_robot = ['robot0', 'robot1', 'robot2', 'robot3', 'robot4']

    if mray == True:
        side = 'yellow'
    else:
        side = 'blue'

    teamYellow = (ref_data["teamcolor"] == 1)

    #Setting the game current foul
    if ref_data["foul"] == 1:
        current_foul = "penalty_kick"
    elif ref_data["foul"] == 2:
        current_foul = "goal_kick"
    elif ref_data["foul"] == 3:
        current_foul = "free_ball"
    elif ref_data["foul"] == 4:
        current_foul = "kickoff"
    #current_foul = str(ref_data["foul"])

    #Setting Offensive or Defensive strategy
    if ref_data["foulQuadrant"] == 0:
        if not mray and teamYellow:
            offensive_defensive_quadrant = 'defensive'
        elif not mray and not teamYellow:
            offensive_defensive_quadrant = 'offensive'
        if mray and teamYellow:
            offensive_defensive_quadrant = 'offensive'
        elif mray and not teamYellow:
            offensive_defensive_quadrant = 'defensive'

    #Setting the quadrant
    elif ref_data["foulQuadrant"] == 1:
        offensive_defensive_quadrant = 'quad1'
    elif ref_data["foulQuadrant"] == 2:
        offensive_defensive_quadrant = 'quad2'
    elif ref_data["foulQuadrant"] == 3:
        offensive_defensive_quadrant = 'quad3'
    else:
        offensive_defensive_quadrant = 'quad4'

    #Setting the goal kick strategy. strategy = if or else
    """
    if current_foul == '1' and if_else != None:
        if if_else == 'if':
            strategy = 'if'
        elif if_else == 'else':
            strategy = 'else'
    
    """

    #if current_foul == '1' and if_else != None:
    #    return data[side][current_foul][offensive_defensive_quadrant][if_else][list_robot[number_robot]]

    return data[side][current_foul][offensive_defensive_quadrant][list_robot[number_robot]]

def Robot2Position(robot, ball, friend1, friend2, enemy0, enemy1, enemy2, list_r0, list_r1, list_r2):
    #Recebendo as informações corretamente
    robot.target.set_coordinates(list_r0[0], list_r0[1], deg2rad(list_r0[2])) #xpos, ypos, theta
    friend1.target.set_coordinates(list_r1[0], list_r1[1], deg2rad(list_r1[2])) #xpos, ypos, theta
    friend2.target.set_coordinates(list_r2[0], list_r2[1], deg2rad(list_r2[2])) #xpos, ypos, theta

    #Robot, friend1 e friend2 funcionando corretamente
    if not robot.arrive():
        robot.vMax = 20
        #v, w = univecController(robot, robot.target, avoid_obst=False) # Calculate linear and angular velocity
        #robot.obst.update2(robot, ball, friend3, friend4, enemy0, enemy1, enemy2, enemy3, enemy4)
        robot.obst.update2(ball)
        v, w = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4, pos_auto=True)
        robot.sim_set_vel(v, w)
    else:
        robot.vMax = 50
        robot.sim_set_vel(0, 0)
        #print("Robo 1 chegou")

    if not friend1.arrive():
        friend1.vMax = 20
        #friend1.obst.update2(friend1, ball, friend3, friend4, enemy0, enemy1, enemy2, enemy3, enemy4)
        friend1.obst.update2(ball)
        v, w = univec_controller(friend1, friend1.target, True, friend1.obst, n=4, d=4, pos_auto=True)
        friend1.sim_set_vel(v, w)
    else:
        friend1.vMax = 50
        friend1.sim_set_vel(0, 0)
        #print("Robo 2 chegou")

    if not friend2.arrive():
        friend2.vMax = 20
        #friend2.obst.update2(friend2, ball, friend3, friend4, enemy0, enemy1, enemy2, enemy3, enemy4)
        friend2.obst.update2(ball)
        v, w = univec_controller(friend2, friend2.target, True, friend2.obst, n=4, d=4, pos_auto=True)
        friend2.sim_set_vel(v, w)
    else:
        friend2.vMax = 50
        friend2.sim_set_vel(0, 0)
        #print("Robo 3 chegou")

    #Tentativa 1, para os dois novos robos.
    
    return True

angulo = deg2rad(-160)
