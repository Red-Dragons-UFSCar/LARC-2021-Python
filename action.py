from numpy import pi, cos, sin, tan, arctan2, sqrt, deg2rad

from execution import univec_controller


def stop(robot):
    """Input: Robot object
    Description: Stops the robot.
    Output: None"""
    robot.sim_set_vel(0, 0)


def shoot(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None):
    """Input: Robot object, ball object, side of field (True = Left, False = Right),
     other robots objects (2 friend , 3 opponents)
    Description: The robot moves to the middle of the desired goal, the orientation is based on line
                 between the position of the ball and the goal.
    Output: None"""
    arrival_theta = calculate_arrival_theta(ball, left_side)
    linear_velocity, angular_velocity = calculate_velocities(ball, enemy1, enemy2, enemy3, friend1, friend2, robot)

    robot.target.update(ball.xPos, ball.yPos, arrival_theta)
    robot.sim_set_vel(linear_velocity, angular_velocity)


# TODO dar um jeito nessas funções extraídas
def calculate_velocities(ball, enemy1, enemy2, enemy3, friend1, friend2, robot):
    """Calculates the angular and linear velocities with the univec_controller function"""
    if friend1 is None and friend2 is None:  # No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, n=16,
                                 d=2)  # Calculate linear and angular velocity

    else:  # Both friends to avoid
        robot.obst.update2(robot, ball, friend1, friend2, enemy1, enemy2, enemy3)
        v, w = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)
    return v, w


def calculate_arrival_theta(ball, left_side):
    if left_side:  # Playing in the left side of field
        arrival_theta = arctan2(65 - ball.yPos, 160 - ball.xPos)  # Angle between the ball and point (150,65)
    else:  # Playing in the right side of field
        arrival_theta = arctan2(65 - ball.yPos, 10 - ball.xPos)  # Angle between the ball and point (0,65)
    return arrival_theta


'''
Input: Robot object, ball object, side of field (True = Left, False = Right), other robots objects (2 friend , 3 opponents)
Description: The robot moves to the desired goal, the orientation is based on position of the ball and the goal.
             If the Y ball position is between 45 and 85, the arrive theta is 0, otherwise is based on line
             between the position of the ball and the edge of goal (This function is not used).
Output: None
'''


def shoot2(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None):
    """Input: Robot object, ball object, side of field (True = Left, False = Right), other robots objects
     (2 friend , 3 opponents)
    Description: The robot moves to the desired goal, the orientation is based on position of the ball and the goal.
                 If the Y ball position is between 45 and 85, the arrive theta is 0, otherwise is based on line
                 between the position of the ball and the edge of goal (This function is not used).
    Output: None"""
    arrival_theta = calculate_arrival_theta_alternate(ball, left_side)
    linear_velocity, angular_velocity = calculate_velocities(ball, enemy1, enemy2, enemy3, friend1, friend2, robot)

    robot.target.update(ball.xPos, ball.yPos, arrival_theta)
    robot.sim_set_vel(linear_velocity, angular_velocity)


def calculate_arrival_theta_alternate(ball, left_side):
    if left_side:  # Playing in the left side of field
        if (ball.yPos > 45) and (ball.yPos < 85):  # arrive with the angle 0
            arrival_theta = 0
        elif ball.yPos <= 45:
            # Y and agle target changes depending on the position of the ball, with the biggest difference
            y = 45 + (45 - ball.yPos) / (45 - 0) * 20
            # the greater the slope, in this way making a more aggressive move to the goal
            arrival_theta = arctan2(y - 45, 160 - ball.xPos)
        else:
            y = 85 - (ball.yPos - 85) / (130 - 85) * 20
            arrival_theta = arctan2(y - 85, 160 - ball.xPos)
    else:  # Playing in the right side of field
        if (ball.yPos > 45) and (ball.yPos < 85):
            arrival_theta = pi
        elif ball.yPos <= 45:
            y = 45 + (45 - ball.yPos) / (45 - 0) * 20
            arrival_theta = arctan2(y - 45, 10 - ball.xPos)
        else:
            y = 85 - (ball.yPos - 85) / (130 - 85) * 20
            arrival_theta = arctan2(y - 85, 10 - ball.xPos)
    return arrival_theta


def defender_spin(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None):
    """Input: Robot object, ball object, side of field (True = Left, False = Right), other robots objects (2 friend,
     3 opponents)
    Description: The robot moves to the ball at an angle to move it away from the friendly goal,
     and try to carry the the for the anemys goal (This is used as a main move strategy for the robots)
    Output: None"""
    if left_side: # Playing in the left side of field
        arrival_theta = arctan2(65 - ball.yPos,  160 - ball.xPos)  # Angle between the ball and point (150,65)
    else: # Playing in the right side of field
        arrival_theta = arctan2(65 - ball.yPos, 10 - ball.xPos)  # Angle between the ball and point (0,65)
    robot.target.update(ball.xPos, ball.yPos, arrival_theta)

    if friend1 is None and friend2 is None:  # No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, n=16, d=2) # Calculate linear and angular velocity
    else:  # Both friends to avoid
        robot.obst.update2(robot, ball, friend1, friend2, enemy1, enemy2, enemy3)
        v, w = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)

    d = robot.dist(ball) # Calculate distance between ball and robot
    if robot.spin and d < 10: # Check if the flag spin is true and if distance is lower than a threshold
        if not robot.teamYellow:
            '''
            Define the direction of rotation, the direction changes based on northern
            and southern hemisphere, in the North hemisphere the direction is clockwise
            and the South hemisphere is anti-clockwise.
            '''
            if robot.yPos > 65:
                v = 0
                w = -30
            else:
                v = 0
                w = 30
        else:
            if robot.yPos > 65:
                v = 0
                w = 30
            else:
                v = 0
                w = -30


    #TODO: CHECK IF THIS IS RIGHT - MAKE IT WORK FOR BOUTH SIDES
    if d < 30 and ball.xPos > robot.xPos: # Check if the distance is lower than a threshold and

                                          # if the ball is on the right of robot
        if robot.teamYellow:
            dx = 15 - robot.xPos
        else:
            dx = 160 - robot.xPos
        dy = tan(robot.theta)*dx + robot.yPos # Calculate the height of the goal arrival
        if dy > 45 and dy < 85:
            if robot.index == 2 or robot.index == 1:
                robot.sim_set_vel2(50*robot.face, 50*robot.face) # Send the velocity of right and left wheel
            else:
                robot.sim_set_vel(v,w) # Calculate linear and angular velocity
        else:
            robot.sim_set_vel(v,w)
    else:
        robot.sim_set_vel(v,w)


def screen_out_ball(robot, ball, static_point, left_side=True, upper_lim=200, lower_lim=0, friend1=None, friend2=None):
    """Input: Robot object, ball object, point to project the ball, side of field (True = Left, False = Right), moviment limits(upper and lower), other robots objects (2 friend)
    Description: Project ball Y position to the selected X point.
    Output: None"""
    xPos = ball.xPos + ball.vx*100*22/60 # Predict ball position multiples frames ahead (Possible conflit with other ball prediction)
    yPos = ball.yPos + ball.vy*100*22/60

    if yPos >= upper_lim: # If ball position is out of limits of Y axis, set the value to the limits
        y_point = upper_lim

    elif yPos <= lower_lim:
        y_point = lower_lim

    else: # Project Y position of the ball to the selected point
        y_point = yPos
    # Check the field side
    if left_side:
        if robot.yPos <= yPos: # Define the arrive angle based on the side of the field
            arrival_theta = pi / 2
        else:
            arrival_theta = -pi / 2
        robot.target.update(static_point, y_point, arrival_theta)
    else:
        if robot.yPos <= yPos:
            arrival_theta = pi / 2
        else:
            arrival_theta = -pi / 2
        robot.target.update(170 - static_point, y_point, arrival_theta)

    if robot.contStopped > 60: # Check if the robot is locked on the corner, and try to free him
        if robot.teamYellow:
            if abs(robot.theta) < 10:
                v = -30
                w = 5
            else:
                v = 30
                w = -5
        else:
            if abs(robot.theta) < 10:
                v = -30
                w = 0
            else:
                v = 30
                w = 0
    else:
        if friend1 is None and friend2 is None:  # No friends to avoid
            v, w = univec_controller(robot, robot.target, avoid_obst=False, stop_when_arrive=True) # Calculate linear and angular velocity
        else:  # Both friends to avoid
            robot.obst.update(robot, friend1, friend2)
            v, w = univec_controller(robot, robot.target, True, robot.obst, stop_when_arrive=True)

    robot.sim_set_vel(v, w)


def goal_keeper_defender(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None,
                         enemy3=None):
    """Input: Robot object, ball object, side of field (True = Left, False = Right), other robots objects (2 friends, 3 opponents)
    Description: The robot pushes the ball away from the goal and make him spin.
    Output: None"""
    if left_side:
        arrival_theta = arctan2(ball.yPos - 65, ball.xPos - 10)  # Angle between the ball and point (150,65)
    else:
        arrival_theta = arctan2(ball.yPos - 65, ball.xPos - 160)  # Angle between the ball and point (0,65)
    robot.target.update(ball.xPos, ball.yPos, arrival_theta)

    if friend1 is None and friend2 is None:  # No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, n=16, d=2)
    else:  # Both friends to avoid
        robot.obst.update(robot, friend1, friend2, enemy1, enemy2, enemy3)
        v, w = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)

    if robot.dist(ball) < 10: # Check if the distance is lower than a threshold
        '''
        Define the direction of rotation, the direction changes based on northern
        and southern hemisphere, in the North hemisphere the direction is clockwise
        and the South hemisphere is anti-clockwise.
        '''
        if not robot.teamYellow:
            if robot.yPos > 65:
                v = 0
                w = -30
            else:
                v = 0
                w = 30
        else:
            if robot.yPos > 65:
                v = 0
                w = 30
            else:
                v = 0
                w = -30

    robot.sim_set_vel(v, w)


def protect_goal(robot, ball, r, left_side=True, friend1=None, friend2=None):
    """Input: Robot object, ball object, radius of circumference, side of field (True = Left, False = Right), other robots objects (2 friend)
    Description: The robot make a semi-circunference around the goal.
    Output: None"""
    if left_side:
        theta = arctan2((ball.yPos - 65), (ball.xPos - 15)) # Calculate angle of vector goal and ball

        if pi / 2 >= theta >= (-pi / 2): # project the ball into the circumference

            proj_x = r * cos(theta) + 15
            proj_y = r * sin(theta) + 65

        else:

            proj_x = -r * cos(theta) + 15
            proj_y = r * sin(theta) + 65

        '''
        Defines the arrival angle, the angle changes based on the ball's relative
        position in relation to the robot, it is necessary to choose the arrival angle
        that generates the smoothest movement to make the semi-circle movement
        '''
        if robot.yPos > 100:
            if robot.xPos < ball.xPos:
                arrival_theta = -(pi / 2 - theta)

            if robot.xPos >= ball.xPos:
                arrival_theta = (pi / 2 + theta)

        if 100 >= robot.yPos > 65:
            if robot.yPos < ball.yPos:
                arrival_theta = (pi / 2 + theta)
            if robot.yPos >= ball.yPos:
                arrival_theta = -(pi / 2 - theta)

        if 65 >= robot.yPos > 30:
            if robot.yPos < ball.yPos:
                arrival_theta = pi / 2 + theta
            if robot.yPos >= ball.yPos:
                arrival_theta = -(pi / 2 - theta)

        if robot.yPos <= 30:
            if robot.xPos < ball.xPos:
                arrival_theta = pi / 2 + theta

            if robot.xPos >= ball.xPos:
                arrival_theta = -(pi / 2 - theta)

    arrival_theta = arctan2(sin(arrival_theta), cos(arrival_theta))
    robot.target.update(proj_x, proj_y, arrival_theta)

    if friend1 is None and friend2 is None:  # No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, stop_when_arrive=True)
    else:  # Both friends to avoid
        robot.obst.update(robot, friend1, friend2)
        v, w = univec_controller(robot, robot.target, True, robot.obst, stop_when_arrive=True)

    robot.sim_set_vel(v, w)


def girar(robot, v1, v2):
    """Input: Robot object, ball object, Velocity of Right and Left wheel
    Description: The robot spin around it's own axis
    Output: None"""
    robot.sim_set_vel2(v1, v2)

def defender_penalty(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None):
    """Input: Robot object, ball object, side of field (True = Left, False = Right), other robots objects (2 friend, 3 opponents)
    Description: Makes the goalkepper go straight to the ball to defend the penalty
    Output: None"""

    if left_side:
        arrival_theta = arctan2(ball.yPos - 65, ball.xPos - 10)  # Angle between the ball and point (150,65)
    else:
        arrival_theta = arctan2(ball.yPos - 65, ball.xPos - 160)  # Angle between the ball and point (0,65)
    robot.target.update(ball.xPos, ball.yPos, arrival_theta)

    if friend1 is None and friend2 is None:  # No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, n=16, d=2)
    else:  # Both friends to avoid
        robot.obst.update(robot, friend1, friend2, enemy1, enemy2, enemy3)
        v, w = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)

    robot.sim_set_vel(v, w)


def defender_penalty_spin(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None):

    list_enemy = [enemy1, enemy2, enemy3]
    distance = 200
    index_enemy = 0

    for enemy in list_enemy:
        d = sqrt((enemy.xPos - ball.xPos)**2 + (enemy.yPos - ball.yPos)**2)
        if d < distance:
            distance = d
            index_enemy = enemy.index
    kicker = list_enemy[index_enemy]

    theta = arctan2(ball.yPos - kicker.yPos, ball.xPos - kicker.xPos)
    phi = pi - theta

    if left_side:
        dx = kicker.xPos - 14
        dy = dx*tan(phi)

        proj_y = kicker.yPos + dy
        proj_x = 14
        if proj_y > 80:
            proj_y = 80
        elif proj_y < 50:
            proj_y = 50
        if proj_y > robot.yPos:
            arrival_theta = pi/2
        else:
            arrival_theta = -pi/2

    else:
        dx = 156 - kicker.xPos
        dy = dx*tan(theta)

        proj_y = kicker.yPos + dy
        proj_x = 156
        if proj_y > 80:
            proj_y = 80
        elif proj_y < 50:
            proj_y = 50
        if proj_y > robot.yPos:
            arrival_theta = pi/2
        else:
            arrival_theta = -pi/2

    robot.target.update(proj_x, proj_y, arrival_theta)

    if friend1 is None and friend2 is None:  # No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, n=16, d=2)
    else:  # Both friends to avoid
        robot.obst.update(robot, friend1, friend2, enemy1, enemy2, enemy3)
        v, w = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)

    if robot.dist(robot.target) < 6:
        if left_side:
        #if robot.arrive():
            v = 0
            if robot.yPos > 65:
                w = 30
            else:
                w = -30
        else:
            v = 0
            if robot.yPos > 65:
                w = -30
            else:
                w = 30

    robot.sim_set_vel(v, w)

def attacker_penalty_spin(robot, ball):
    if not robot.dist(ball) < 9: # If the attacker is not closer to the ball
        girar(robot, 100, 100) # Moving forward
    else:
        if robot.teamYellow: # Team verification
            if robot.yPos < 65:
                girar(robot, 0, 100) # Shoots the ball spinning up
            else:
                girar(robot, 100, 0) # Shoots the ball spinning down
        else:
            if robot.yPos > 65:
                girar(robot, 0, 100) # Shoots the ball spinning down
            else:
                girar(robot, 100, 0) # Shoots the ball spinning up

def attacker_penalty_direct(robot):
    if robot.teamYellow:
        girar(robot,-10,-10)
    else:
        girar(robot,-10,-10)

'''
Input: Robot object, ball object, side of field (True = Left, False = Right), other robots objects (2 friend, 3 opponents)
Description: Positions the robot to take the penalty, it is positioned and moves to go towards the corners of the goal.
Output: None
'''

def attack_penalty(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None):
    """Input: Robot object, ball object, side of field (True = Left, False = Right), other robots objects (2 friend, 3 opponents)
    Description: Positions the robot to take the penalty, it is positioned and moves to go towards the corners of the goal.
    Output: None"""
    if left_side:
        '''
        The arrive angle changes based on the position, and the position have 2 random possibilities
        '''
        if robot.yPos > 65:
            arrival_theta = -deg2rad(15)
        else:
            arrival_theta = deg2rad(15)
    else:
        if robot.yPos > 65:
            arrival_theta = -deg2rad(165)
        else:
            arrival_theta = deg2rad(165)

    robot.target.update(ball.xPos, ball.yPos, arrival_theta)

    if friend1 is None and friend2 is None:  # No friends to avoid
        v, w = univec_controller(robot, robot.target, avoid_obst=False, n=16, d=2)
    else:  # Both friends to avoid
        robot.obst.update(robot, friend1, friend2, enemy1, enemy2, enemy3)
        v, w = univec_controller(robot, robot.target, True, robot.obst, n=4, d=4)

    robot.sim_set_vel(v, w)


def follower(robot_follower, robot_leader, ball, robot0=None, robot_enemy_0=None, robot_enemy_1=None, robot_enemy_2=None):

    """Input: Robot object (All team members), ball object, other robots objects (3 opponents)
    Description: Defines the position of follower robot based on the leader position.
    Output: None"""

    if robot_leader.yPos > 65:
        if robot_leader.xPos > 75:
            proj_x = robot_leader.xPos - 15
            proj_y = robot_leader.yPos - 30
        else:
            proj_x = robot_leader.xPos + 15
            proj_y = robot_leader.yPos - 15
    else:
        if robot_leader.xPos > 75:
            proj_x = robot_leader.xPos - 15
            proj_y = robot_leader.yPos + 30
        else:
            proj_x = robot_leader.xPos + 15
            proj_y = robot_leader.yPos + 15
    '''
    Calculate distante between the follower and the projected point
    '''
    dist = sqrt((robot_follower.xPos - proj_x) ** 2 + (robot_follower.yPos - proj_y) ** 2)
    arrival_theta = arctan2(ball.yPos - robot_follower.yPos, ball.xPos - robot_follower.xPos)
    robot_follower.target.update(proj_x, proj_y, arrival_theta)

    if dist < 10: # Check if the robot is close to the projected point and stops the robot
        stop(robot_follower)
    else:
        # No friends to avoid
        if robot0 is None and robot_enemy_0 is None and robot_enemy_1 is None and robot_enemy_2 is None:
            v, w = univec_controller(robot_follower, robot_follower.target, avoid_obst=False, n=16, d=2)
        else:  # Both friends to avoid
            robot_follower.obst.update(robot_follower, robot0, robot_leader, robot_enemy_0, robot_enemy_1, robot_enemy_2)
            v, w = univec_controller(robot_follower, robot_follower.target, True, robot_follower.obst, n=4, d=4)

        robot_follower.sim_set_vel(v, w)


def followLeader(robot0, robot1, robot2, ball, robot_enemy_0, robot_enemy_1, robot_enemy_2):
    """Input: Robot object (All team members), ball object, other robots objects (3 opponents)
    Description: Defines the strategy of 2 attackers, who is the leader and what each robot need to do in each situation.
    Output: None"""
    dist1 = sqrt((robot1.xPos - ball.xPos) ** 2 + (robot1.yPos - ball.yPos) ** 2)
    dist2 = sqrt((robot2.xPos - ball.xPos) ** 2 + (robot2.yPos - ball.yPos) ** 2)

    if dist2 < dist1: # Strategy if robot 2 is closer to the ball
        if robot1.isLeader is None and robot2.isLeader is None:
            robot2.isLeader = True
            robot1.isLeader = False
            robot2.holdLeader += 1

        else:
            if robot2.isLeader:
                robot2.holdLeader += 1
            else:
                if robot1.holdLeader > 60:
                    robot2.isLeader = True
                    robot1.isLeader = False
                    robot1.holdLeader = 0
                    robot2.holdLeader += 1
                else:
                    robot1.holdLeader += 1

    # Same idea, but robot 1 is closer to the ball
    else:
        if robot1.isLeader is None and robot2.isLeader is None:
            robot1.isLeader = True
            robot2.isLeader = False
            robot1.holdLeader += 1
        else:
            if robot1.isLeader:
                robot1.holdLeader += 1
            else:
                if robot2.holdLeader > 60:
                    robot1.isLeader = True
                    robot2.isLeader = False
                    robot1.holdLeader += 1
                    robot2.holdLeader = 0
                else:
                    robot2.holdLeader += 1

    if robot2.isLeader:
        if not robot1.teamYellow:
            if ball.xPos < 30 and (110 > ball.yPos > 30): # If ball is in defence side the robot 2 do the screen out, and the robot 1 follow his moves
                if robot1.xPos < 30:
                    screen_out_ball(robot2, robot2, 55, left_side=not robot2.teamYellow, upper_lim=120, lower_lim=10)
                else:
                    screen_out_ball(robot2, ball, 55, left_side=not robot2.teamYellow, upper_lim=120, lower_lim=10)
                follower(robot1, robot2, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)

            else:  # If ball is in attack side the robot 2 do the defender spin, and the robot 1 follow his moves
                defender_spin(robot2, ball, left_side=not robot2.teamYellow, friend1=robot0, friend2=robot0,
                              enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                '''
                If is the robot 1 is close enough to the tha ball, starts to do the defender spin
                '''
                if robot1.dist(ball) < 20:
                    if robot2.xPos > 140 and (100 > robot2.yPos > 40):
                        follower(robot1, robot2, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)
                    else:
                        defender_spin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot0, friend2=robot2,
                                      enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                else:
                    follower(robot1, robot2, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)

        #Same Idea but for the other side of de field
        else:
            if ball.xPos > 130 and (110 > ball.yPos > 30):
                if robot1.xPos > 130:
                    screen_out_ball(robot2, robot2, 55, left_side=not robot2.teamYellow, upper_lim=120, lower_lim=10)
                else:
                    screen_out_ball(robot2, ball, 55, left_side=not robot2.teamYellow, upper_lim=120, lower_lim=10)
                follower(robot1, robot2, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)

            else:
                defender_spin(robot2, ball, left_side=not robot2.teamYellow, friend1=robot0, friend2=robot0,
                              enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                if robot1.dist(ball) < 20:
                    if robot2.xPos < 35 and (100 > robot2.yPos > 40):
                        follower(robot1, robot2, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)
                    else:
                        defender_spin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot0, friend2=robot2,
                                      enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                else:
                    follower(robot1, robot2, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)

    elif robot1.isLeader:
        if not robot1.teamYellow:
            if ball.xPos < 35 and (110 > ball.yPos > 30):
                if robot1.xPos < 35:
                    screen_out_ball(robot1, robot1, 55, left_side=not robot1.teamYellow, upper_lim=120, lower_lim=10)
                else:
                    screen_out_ball(robot1, ball, 55, left_side=not robot1.teamYellow, upper_lim=120, lower_lim=10)
                follower(robot2, robot1, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)

            else:
                defender_spin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot0, friend2=robot0,
                              enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                if robot2.dist(ball) < 20:
                    if robot1.xPos > 140 and (100 > robot1.yPos > 40):
                        follower(robot2, robot1, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)
                    else:
                        defender_spin(robot2, ball, left_side=not robot2.teamYellow, friend1=robot0, friend2=robot1,
                                      enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                else:
                    follower(robot2, robot1, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)
        else:
            if ball.xPos > 130 and (110 > ball.yPos > 30):
                if robot1.xPos > 130:
                    screen_out_ball(robot1, robot1, 55, left_side=not robot1.teamYellow, upper_lim=120, lower_lim=10)
                else:
                    screen_out_ball(robot1, ball, 55, left_side=not robot1.teamYellow, upper_lim=120, lower_lim=10)
                follower(robot2, robot1, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)

            else:
                defender_spin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot0, friend2=robot0,
                              enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                if robot2.dist(ball) < 20:
                    if robot1.xPos < 35 and (100 > robot1.yPos > 40):
                        follower(robot2, robot1, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)
                    else:
                        defender_spin(robot2, ball, left_side=not robot2.teamYellow, friend1=robot0, friend2=robot1,
                                      enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2)
                else:
                    follower(robot2, robot1, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2)
