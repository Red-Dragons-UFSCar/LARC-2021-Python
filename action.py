from numpy import pi,cos,sin,tan,arctan2,sqrt ,matmul,array, deg2rad
from execution import univecController, whichFace
from behaviours import Univector

#% Basic Actions
def stop(robot):
    robot.simSetVel(0,0)

#% Attacker Actions
def shoot(robot,ball,leftSide=True,friends=[],enemys=[]):
    if leftSide:
        arrivalTheta=arctan2(90-ball.yPos,235-ball.xPos) #? Angle between the ball and point (150,65)
    else:
        arrivalTheta=arctan2(90-ball.yPos,15-ball.xPos) #? Angle between the ball and point (0,65)
    #robot.target.update(ball.xPos,ball.yPos,0)
    robot.target.update(ball.xPos,ball.yPos,arrivalTheta)

    if not friends: #? No friends to avoid
        v,w=univecController(robot,robot.target,avoidObst=False,n=16, d=2)
    else: #? Both friends to avoid
        #robot.obst.update(robot, obstacles)
        robot.obst.update2(robot, ball, friends[0], friends[1], enemys[0], enemys[1], enemys[2], enemys[3], enemys[4])
        v,w=univecController(robot,robot.target,True,robot.obst,n=4, d=4)

    robot.simSetVel(v,w)

def shoot_penalty(robot,ball,leftSide=True,friends=[],enemys=[]):
    if leftSide:
        arrivalTheta=arctan2(52-ball.yPos,235-ball.xPos) #? Angle between the ball and point (150,65)
    else:
        arrivalTheta=arctan2(52-ball.yPos,15-ball.xPos) #? Angle between the ball and point (0,65)
    #robot.target.update(ball.xPos,ball.yPos,0)
    robot.target.update(ball.xPos,ball.yPos,arrivalTheta)

    v,w=univecController(robot,robot.target,avoidObst=False,n=16, d=2)
    robot.simSetVel(v*5,w*5)

def defenderSpin2(robot,ball,leftSide=True,friends=[],enemys=[]):
    if leftSide:
        arrivalTheta=arctan2(90-ball.yPos,235-ball.xPos) #? Angle between the ball and point (150,65)
    else:
        arrivalTheta=arctan2(90-ball.yPos,15-ball.xPos) #? Angle between the ball and point (0,65)
    #robot.target.update(ball.xPos,ball.yPos,0)
    robot.target.update(ball.xPos,ball.yPos,arrivalTheta)

    if not friends: #? No friends to avoid
        v,w=univecController(robot,robot.target,avoidObst=False,n=16, d=2)
    else: #? Both friends to avoid
        #robot.obst.update(robot, obstacles)
        robot.obst.update2(robot, ball, friends, enemys)
        v,w=univecController(robot,robot.target,True,robot.obst,n=4, d=4)

    d = robot.dist(ball)
    if robot.spin and d < 10:
        if not robot.teamYellow:
            if robot.yPos > 90:
                v = 0
                w = -30
            else:
                v = 0
                w = 30
        else:
            if robot.yPos > 90:
                v = 0
                w = 30
            else:
                v = 0
                w = -30

    robot.simSetVel(v,w)

def defenderSpin(robot, ball, left_side=True, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None, enemy4=None, enemy5=None):
    if left_side: # Playing in the left side of field
        arrival_theta = arctan2(90 - ball.yPos,  235- ball.xPos)  # Angle between the ball and point (150,65)
    else: # Playing in the right side of field
        arrival_theta = arctan2(90 - ball.yPos, 15 - ball.xPos)  # Angle between the ball and point (0,65)
    robot.target.update(ball.xPos, ball.yPos, arrival_theta)

    if friend1 is None and friend2 is None:  # No friends to avoid
        v, w = univecController(robot, robot.target, avoid_obst=False, n=16, d=2) # Calculate linear and angular velocity
    else:  # Both friends to avoid
        robot.obst.update2(robot, ball, friend1, friend2, enemy1, enemy2, enemy3, enemy4, enemy5)
        v, w = univecController(robot, robot.target, True, robot.obst, n=4, d=4)

    d = robot.dist(ball) # Calculate distance between ball and robot
    if robot.spin and d < 10: # Check if the flag spin is true and if distance is lower than a threshold
        if not robot.teamYellow:
            '''
            Define the direction of rotation, the direction changes based on northern
            and southern hemisphere, in the North hemisphere the direction is clockwise
            and the South hemisphere is anti-clockwise.
            '''
            if robot.yPos > 90:
                v = 0
                w = -30
            else:
                v = 0
                w = 30
        else:
            if robot.yPos > 90:
                v = 0
                w = 30
            else:
                v = 0
                w = -30

    #TODO: CHECK IF THIS IS RIGHT - MAKE IT WORK FOR BOUTH SIDES
    flagVelocity = False
    if d < 30 :                           # Check if the distance is lower than a threshold and # if the ball is on the right of robot
        if robot.teamYellow:
            if ball.xPos < robot.xPos:
                dx = 15 - robot.xPos
                flagVelocity = True
        else:
            if ball.xPos > robot.xPos:
                dx = 235 - robot.xPos
                flagVelocity = True
        if flagVelocity:
            dy = tan(robot.theta)*dx + robot.yPos # Calculate the height of the goal arrival
            if dy > 70 and dy < 110:
                if robot.index == 2 or robot.index == 1:
                    robot.simSetVel2(50*robot.face, 50*robot.face) # Send the velocity of right and left wheel
                    #print("zuuum + ", robot.theta)
                else:
                    robot.simSetVel(v,w) # Calculate linear and angular velocity
            else:
                robot.simSetVel(v,w)
        else:
            robot.simSetVel(v,w)
    else:
        robot.simSetVel(v,w)

# def defenderSpin(robot,ball,leftSide=True,friends=[],enemys=[]):
#     if leftSide:
#         arrivalTheta=arctan2(90-ball.yPos,235-ball.xPos) #? Angle between the ball and point (150,65)
#     else:
#         arrivalTheta=arctan2(90-ball.yPos,15-ball.xPos) #? Angle between the ball and point (0,65)
#     #robot.target.update(ball.xPos,ball.yPos,0)
#     robot.target.update(ball.xPos,ball.yPos,arrivalTheta)
#
#     if not friends: #? No friends to avoid
#         v,w=univecController(robot,robot.target,avoidObst=False,n=16, d=2)
#     else: #? Both friends to avoid
#         #robot.obst.update(robot,friend1,friend2,enemy1,enemy2,enemy3)
#         robot.obst.update2(robot, ball, friends, enemys)
#         v,w=univecController(robot,robot.target,True,robot.obst,n=4, d=4)
#
#     d = robot.dist(ball)
#     if robot.spin and d < 10:
#         if not robot.teamYellow:
#             if robot.yPos > 90:
#                 v = 0
#                 w = -30
#             else:
#                 v = 0
#                 w = 30
#         else:
#             if robot.yPos > 90:
#                 v = 0
#                 w = 30
#             else:
#                 v = 0
#                 w = -30
#     if d < 30 and ball.xPos > robot.xPos:
#         if robot.teamYellow:
#             dx = 15-robot.xPos
#         else:
#             dx = 235 - robot.xPos
#         dy = tan(robot.theta)*dx + robot.yPos
#         if dy > 70 and dy < 110:
#             if robot.index == 2 or robot.index == 1:
#                 robot.simSetVel2(50*robot.face, 50*robot.face)
#             else:
#                 robot.simSetVel(v,w)
#         else:
#             robot.simSetVel(v,w)
#     else:
#         robot.simSetVel(v,w)

#TODO #2 Need more speed to reach the ball faster than our enemy
def screenOutBall(robot,ball,staticPoint,leftSide=True,upperLim=200,lowerLim=0,friend1=None,friend2=None):
    xPos = ball.xPos + ball.vx*100*22/60 # Só mudei isso
    yPos = ball.yPos + ball.vy*100*22/60
    #Check if ball is inside the limits
    if yPos >= upperLim:
        yPoint = upperLim

    elif yPos <= lowerLim:
        yPoint = lowerLim

    else:
        yPoint = yPos
    #Check the field side
    if leftSide:
        if robot.yPos <= yPos:
            arrivalTheta=pi/2
        else:
            arrivalTheta=-pi/2
        robot.target.update(staticPoint,yPoint,arrivalTheta)
    else:
        if robot.yPos <= yPos:
            arrivalTheta=pi/2
        else:
            arrivalTheta=-pi/2
        robot.target.update(250 - staticPoint,yPoint,arrivalTheta)

    if robot.contStopped > 60:
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
        if friend1 is None and friend2 is None: #? No friends to avoid
            v,w=univecController(robot,robot.target,avoidObst=False,stopWhenArrive=True)
        else: #? Both friends to avoid
            robot.obst.update(robot,friend1,friend2)
            v,w=univecController(robot,robot.target,True,robot.obst,stopWhenArrive=True)

    robot.simSetVel(v,w)

def protectGoal(robot,ball,r,leftSide=True,friend1=None,friend2=None):

    if leftSide:
        theta = arctan2((ball.yPos-65),(ball.xPos-15))

        if (theta <= pi/2 and theta >= (-pi/2)):

            projX = r*cos(theta) + 15
            projY = r*sin(theta) + 65

        else:

            projX = -r*cos(theta) + 15
            projY = r*sin(theta) + 65

        if robot.yPos > 100:
            if robot.xPos < ball.xPos:
                arrivalTheta = -(pi/2 - theta)

            if robot.xPos >= ball.xPos:
                arrivalTheta = (pi/2 + theta)

        if (robot.yPos <= 100 and robot.yPos > 65):
            if robot.yPos < ball.yPos:
                arrivalTheta = (pi/2 + theta)
            if robot.yPos >= ball.yPos:
                arrivalTheta = -(pi/2 - theta)

        if (robot.yPos <= 65 and robot.yPos > 30):
            if robot.yPos < ball.yPos:
                arrivalTheta = pi/2 + theta
            if robot.yPos >= ball.yPos:
                arrivalTheta = -(pi/2 - theta)

        if robot.yPos <= 30:
            if robot.xPos < ball.xPos:
                arrivalTheta = pi/2 + theta

            if robot.xPos >= ball.xPos:
                arrivalTheta = -(pi/2 - theta)

    arrivalTheta = arctan2(sin(arrivalTheta), cos(arrivalTheta))
    robot.target.update(projX,projY,arrivalTheta)

    if friend1 is None and friend2 is None: #? No friends to avoid
        v,w=univecController(robot,robot.target,avoidObst=False,stopWhenArrive=True)
    else: #? Both friends to avoid
        robot.obst.update(robot,friend1,friend2)
        v,w=univecController(robot,robot.target,True,robot.obst,stopWhenArrive=True)

    robot.simSetVel(v,w)

#%Crossing functions
def directGoal(robot, ball, leftSide = True,friend1=None,friend2=None, enemy1=None, enemy2=None, enemy3=None):
    if(robot.flagDirectGoal):
        if(robot.dist(ball) < 10):
            robot.target.update(150,65, 0)
        else:
            robot.flagDirectGoal = False
    else:
        arrivalTheta = arctan2(65-ball.yPos,150-ball.xPos)
        robot.target.update(ball.xPos, ball.yPos, arrivalTheta)
        if(robot.dist(ball) < 10 and (robot.theta < (arrivalTheta+pi/18) and (robot.theta > arrivalTheta - pi/18))):
            robot.flagDirectGoal = True

    if friend1 is None and friend2 is None: #? No friends to avoid
        v,w=univecController(robot,robot.target,avoidObst=False)
    else: #? Both friends to avoid
        robot.obst.update(robot,friend1,friend2, enemy1, enemy2, enemy3)
        v,w=univecController(robot,robot.target,True,robot.obst)
    robot.simSetVel(v,w)

def girar(robot, v1, v2):
    robot.simSetVel2(v1,v2)

def follower(robot_follower, robot_leader, ball, robot0=None, robot_enemy_0=None, robot_enemy_1=None, robot_enemy_2=None, robot_enemy_3=None, robot_enemy_4=None):

    '''
    Defines the position of the follower based on the leader position, the position is a diagonal
    projection of leader position.
    '''
    if robot_leader.yPos > 90:
        if robot_leader.xPos > 126:
            proj_x = robot_leader.xPos - 15
            proj_y = robot_leader.yPos - 30
        else:
            proj_x = robot_leader.xPos + 15
            proj_y = robot_leader.yPos - 15
    else:
        if robot_leader.xPos > 126:
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
            v, w = univecController(robot_follower, robot_follower.target, avoid_obst=False, n=16, d=2)
        else:  # Both friends to avoid
            robot_follower.obst.update2(robot_follower, ball, robot0, robot_leader, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
            v, w = univecController(robot_follower, robot_follower.target, True, robot_follower.obst, n=4, d=4)

        robot_follower.simSetVel(v, w)

'''
Input: Robot object (All team members), ball object, other robots objects (3 opponents)
Description: Defines the strategy of 2 attackers, who is the leader and what each robot need to do in each situation.
Output: None
'''

def leaderSelector(robot1, robot2, ball):

    '''
    Calculate the distan of both robots to the ball
    '''
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

def followLeader(robot0, robot1, robot2, ball, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4):

    leaderSelector(robot1, robot2, ball)

    if robot2.isLeader:
        if not robot1.teamYellow:
            if ball.xPos < 40 and (130 > ball.yPos > 50): # If ball is in defence side the robot 2 do the screen out, and the robot 1 follow his moves
                if robot1.xPos < 30:
                    screenOutBall(robot2, robot2, 55, leftSide=not robot2.teamYellow, upper_lim=120, lower_lim=10)
                else:
                    screenOutBall(robot2, ball, 55, leftSide=not robot2.teamYellow, upper_lim=120, lower_lim=10)
                follower(robot1, robot2, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)

            else:  # If ball is in attack side the robot 2 do the defender spin, and the robot 1 follow his moves
                defenderSpin(robot2, ball, left_side=not robot2.teamYellow, friend1=robot0, friend2=robot0,
                              enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
                '''
                If is the robot 1 is close enough to the tha ball, starts to do the defender spin
                '''
                if robot1.dist(ball) < 40:
                    if robot2.xPos > 195 and (100 > robot2.yPos > 40):
                        follower(robot1, robot2, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
                    else:
                        defenderSpin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot0, friend2=robot2,
                                      enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
                else:
                    follower(robot1, robot2, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)

        #Same Idea but for the other side of de field
        else:
            if ball.xPos > 195 and (120 > ball.yPos > 50):
                if robot1.xPos > 180:
                    screenOutBall(robot2, robot2, 55, leftSide=not robot2.teamYellow, upper_lim=120, lower_lim=10)
                else:
                    screenOutBall(robot2, ball, 55, leftSide=not robot2.teamYellow, upper_lim=120, lower_lim=10)
                follower(robot1, robot2, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)

            else:
                defenderSpin(robot2, ball, left_side=not robot2.teamYellow, friend1=robot0, friend2=robot0,
                  enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
                if robot1.dist(ball) < 40:
                    if robot2.xPos < 35 and (100 > robot2.yPos > 40):
                        follower(robot1, robot2, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3,robot_enemy_4)
                    else:
                        defenderSpin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot0, friend2=robot2,
                                      enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
                else:
                    follower(robot1, robot2, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)

    elif robot1.isLeader:
        if not robot1.teamYellow:
            if ball.xPos < 35 and (120 > ball.yPos > 50):
                if robot1.xPos < 35:
                    screenOutBall(robot1, robot1, 55, leftSide=not robot1.teamYellow, upper_lim=120, lower_lim=10)
                else:
                    screenOutBall(robot1, ball, 55, leftSide=not robot1.teamYellow, upper_lim=120, lower_lim=10)
                follower(robot2, robot1, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)

            else:
                defenderSpin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot0, friend2=robot0,
                              enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
                if robot2.dist(ball) < 40:
                    if robot1.xPos > 195 and (100 > robot1.yPos > 40):
                        follower(robot2, robot1, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
                    else:
                        defenderSpin(robot2, ball, left_side=not robot2.teamYellow, friend1=robot0, friend2=robot1,
                                      enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
                else:
                    follower(robot2, robot1, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
        else:
            if ball.xPos > 195 and (130 > ball.yPos > 50):
                if robot1.xPos > 130:
                    screenOutBall(robot1, robot1, 55, leftSide=not robot1.teamYellow, upper_lim=120, lower_lim=10)
                else:
                    screenOutBall(robot1, ball, 55, leftSide=not robot1.teamYellow, upper_lim=120, lower_lim=10)
                follower(robot2, robot1, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)

            else:
                defenderSpin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot0, friend2=robot0,
                              enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
                if robot2.dist(ball) < 40:
                    if robot1.xPos < 35 and (100 > robot1.yPos > 40):
                        follower(robot2, robot1, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
                    else:
                        defenderSpin(robot2, ball, left_side=not robot2.teamYellow, friend1=robot0, friend2=robot1,
                                      enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
                else:
                    follower(robot2, robot1, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)

def defenderPenalty(robot,ball,leftSide=True,friend1=None,friend2=None, enemy1=None,  enemy2=None, enemy3=None):
    if leftSide:
        arrivalTheta=arctan2(ball.yPos-90,ball.xPos-15) #? Angle between the ball and point (150,65)
    else:
        arrivalTheta=arctan2(ball.yPos-90,ball.xPos-235) #? Angle between the ball and point (0,65)
    #robot.target.update(ball.xPos,ball.yPos,0)
    robot.target.update(ball.xPos,ball.yPos,arrivalTheta)

    if friend1 is None and friend2 is None: #? No friends to avoid
        v,w=univecController(robot,robot.target,avoidObst=False,n=16, d=2)
    else: #? Both friends to avoid
        robot.obst.update(robot,friend1,friend2,enemy1,enemy2,enemy3)
        v,w=univecController(robot,robot.target,True,robot.obst,n=4, d=4)

    robot.simSetVel(v,w)

def attackPenalty(robot,ball,leftSide=True,friend1=None,friend2=None, enemy1=None,  enemy2=None, enemy3=None):
    if leftSide:
        if robot.yPos > 65:
            arrivalTheta = -deg2rad(15)
        else:
            arrivalTheta = deg2rad(15)
    else:
        if robot.yPos > 65:
            arrivalTheta = -deg2rad(165)
        else:
            arrivalTheta = deg2rad(165)

    robot.target.update(ball.xPos, ball.yPos, arrivalTheta)

    if friend1 is None and friend2 is None: #? No friends to avoid
        v,w=univecController(robot,robot.target,avoidObst=False,n=16, d=2)
    else: #? Both friends to avoid
        robot.obst.update(robot,friend1,friend2,enemy1,enemy2,enemy3)
        v,w=univecController(robot,robot.target,True,robot.obst,n=4, d=4)

    robot.simSetVel(v,w)
