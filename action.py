from numpy import pi,cos,sin,tan,arctan2,sqrt ,matmul,array, deg2rad, rad2deg
import math
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
        v, w = univecController(robot, robot.target, avoidObst=False, n=16, d=2) # Calculate linear and angular velocity
    else:  # Both friends to avoid
        robot.obst.update2(robot, ball, friend1, friend2, enemy1, enemy2, enemy3, enemy4, enemy5)
        v, w = univecController(robot, robot.target, True, robot.obst, n=4, d=4, doubleFace=True)

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
            v, w = univecController(robot_follower, robot_follower.target, avoidObst=False, n=16, d=2)
        else:  # Both friends to avoid
            robot_follower.obst.update2(robot_follower, ball, robot0, robot_leader, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
            v, w = univecController(robot_follower, robot_follower.target, True, robot_follower.obst, n=4, d=4)

        robot_follower.simSetVel(v, w)

def mirror_follower(robot_follower, robot_leader, ball, robot0=None, robot_enemy_0=None, robot_enemy_1=None, robot_enemy_2=None, robot_enemy_3=None, robot_enemy_4=None):

    '''
    Defines the position of the follower based on the leader position, the position is a mirror position based on the leader
    '''
    if robot_leader.yPos > 90:
        if robot_leader.xPos > 126:
            proj_x = robot_leader.xPos - 15
            proj_y = 90 - (180 - robot_leader.yPos)
        else:
            proj_x = robot_leader.xPos + 15
            proj_y = 90 - (180 - robot_leader.yPos)
    else:
        if robot_leader.xPos > 126:
            proj_x = robot_leader.xPos - 15
            proj_y = 90 + robot_leader.yPos
        else:
            proj_x = robot_leader.xPos + 15
            proj_y = 90 + robot_leader.yPos
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
            v, w = univecController(robot_follower, robot_follower.target, avoidObst=False, n=16, d=2)
        else:  # Both friends to avoid
            robot_follower.obst.update2(robot_follower, ball, robot0, robot_leader, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
            v, w = univecController(robot_follower, robot_follower.target, True, robot_follower.obst, n=4, d=4)

        robot_follower.simSetVel(v, w)

'''
Input: Robot object (All team members), ball object, other robots objects (3 opponents)
Description: Defines the strategy of 2 attackers, who is the leader and what each robot need to do in each situation.
Output: None
'''

def angulo_Bola(robot, ball):
    if robot.teamYellow:
        y = 90 - ball.yPos
        x = ball.xPos - 15
    else:
        y = 90 - ball.yPos
        x = 250 - (ball.xPos + 15)

    theta = arctan2(y, x)
    
    if robot.teamYellow and ball.yPos < 90:
        theta = pi - theta
    if robot.teamYellow and ball.yPos > 90:
        theta = -pi - theta

    return theta


def new_leaderSelector(robot1, robot2, ball):

    '''
    Calculate the distan of both robots to the ball
    '''
    dist1 = sqrt((robot1.xPos - ball.xPos) ** 2 + (robot1.yPos - ball.yPos) ** 2)
    dist2 = sqrt((robot2.xPos - ball.xPos) ** 2 + (robot2.yPos - ball.yPos) ** 2)
    
    ballTheta = angulo_Bola(robot1, ball)
    angDiff1 = abs(abs(ballTheta) - abs(robot1.theta))
    angDiff2 = abs(abs(ballTheta) - abs(robot2.theta))
    #distDiff = abs(dist1 - dist2)

    #calculando heuristicas através da multiplicação do angulo e da distância
    heur1 = dist1 * angDiff1
    heur2 = dist2 * angDiff2    

    if heur2 < heur1:
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

#triple_leaederSelector
def triple_leaderSelector(robot1, robot2, robot3, ball):
    dist1 = sqrt((robot1.xPos - ball.xPos) ** 2 + (robot1.yPos - ball.yPos) ** 2)
    dist2 = sqrt((robot2.xPos - ball.xPos) ** 2 + (robot2.yPos - ball.yPos) ** 2)
    dist3 = sqrt((robot3.xPos - ball.xPos) ** 2 + (robot3.yPos - ball.yPos) ** 2)

    if dist1 < dist2 and dist1 < dist3: # Strategy if robot 2 is closer to the ball
        if robot1.isLeader is None and robot2.isLeader is None and robot3.isLeader is None:
            robot1.isLeader = True
            robot2.isLeader = False
            robot3.isLeader = False
            robot1.holdLeader += 1

        else:
            if robot1.isLeader:
                robot1.holdLeader += 1
            else:
                if robot2.holdLeader > 60 or robot3.holdLeader > 60:
                    robot1.isLeader = True
                    robot2.isLeader = False
                    robot3.isLeader = False
                    robot1.holdLeader += 1
                    robot2.holdLeader = 0
                    robot3.holdLeader = 0
                elif robot2.holdLeader > 0:
                    robot2.holdLeader += 1
                elif robot3.holdLeader > 0:
                    robot3.holdLeader += 1

    if dist2 < dist1 and dist2 < dist3: # Strategy if robot 2 is closer to the ball
        if robot1.isLeader is None and robot2.isLeader is None and robot3.isLeader is None:
            robot1.isLeader = False
            robot2.isLeader = True
            robot3.isLeader = False
            robot2.holdLeader += 1

        else:
            if robot2.isLeader:
                robot2.holdLeader += 1
            else:
                if robot1.holdLeader > 60 or robot3.holdLeader > 60:
                    robot2.isLeader = True
                    robot1.isLeader = False
                    robot3.isLeader = False
                    robot1.holdLeader = 0
                    robot3.holdLeader = 0
                    robot2.holdLeader += 1
                elif robot1.holdLeader > 0:
                    robot1.holdLeader += 1
                elif robot3.holdLeader > 0:
                    robot3.holdLeader += 1

    if dist3 < dist2 and dist3 < dist1: # Strategy if robot 2 is closer to the ball
        if robot1.isLeader is None and robot2.isLeader is None and robot3.isLeader is None:
            robot1.isLeader = False
            robot2.isLeader = False
            robot3.isLeader = True
            robot3.holdLeader += 1

        else:
            if robot3.isLeader:
                robot3.holdLeader += 1
            else:
                if robot1.holdLeader > 60 or robot2.holdLeader > 60:
                    robot1.isLeader = False
                    robot2.isLeader = False
                    robot3.isLeader = True
                    robot1.holdLeader = 0
                    robot2.holdLeader = 0
                    robot3.holdLeader += 1
                elif robot1.holdLeader > 0:
                    robot1.holdLeader += 1
                elif robot2.holdLeader > 0:
                    robot2.holdLeader += 1

def followLeader(robot0, robot1, robot2, ball, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4):

    leaderSelector(robot1, robot2, ball)

    if robot2.isLeader:
        if not robot1.teamYellow:
            if ball.xPos < 40 and (130 > ball.yPos > 50): # If ball is in defence side the robot 2 do the screen out, and the robot 1 follow his moves
                #print('hmmmm')
                if robot1.xPos < 30:
                    screenOutBall(robot2, robot2, 55, leftSide=not robot2.teamYellow, upperLim=120, lowerLim=10)
                else:
                    screenOutBall(robot2, ball, 55, leftSide=not robot2.teamYellow, upperLim=120, lowerLim=10)
                follower(robot1, robot2, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)

            else:  # If ball is in attack side the robot 2 do the defender spin, and the robot 1 follow his moves
                #print('ataque azul')
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
                    screenOutBall(robot2, robot2, 55, leftSide=not robot2.teamYellow, upperLim=120, lowerLim=10)
                else:
                    screenOutBall(robot2, ball, 55, leftSide=not robot2.teamYellow, upperLim=120, lowerLim=10)
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
                    screenOutBall(robot1, robot1, 55, leftSide=not robot1.teamYellow, upperLim=120, lowerLim=10)
                else:
                    screenOutBall(robot1, ball, 55, leftSide=not robot1.teamYellow, upperLim=120, lowerLim=10)
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
                    screenOutBall(robot1, robot1, 55, leftSide=not robot1.teamYellow, upperLim=120, lowerLim=10)
                else:
                    screenOutBall(robot1, ball, 55, leftSide=not robot1.teamYellow, upperLim=120, lowerLim=10)
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

def atacante_lider(robot, ball, friend=None, enemy1=None, enemy2=None, enemy3=None, enemy4=None, enemy5=None):
    ballXPos = ball.xPos
    ballYPos = ball.yPos

    theta = 0
    xPos = 0
    yPos = 0

    if robot.teamYellow:
        xPos = ballXPos
        yPos = ballYPos
        theta = math.atan2(90 - ball.yPos, ball.xPos - 15)
        theta = math.pi - theta
        stop = False

    if not robot.teamYellow:
        xPos = ballXPos
        yPos = ballYPos
        theta = math.atan2(90 - ball.yPos, 235 - ball.xPos)
        stop = False

    robot.target.update(xPos, yPos, theta)
    
    if enemy1 is None:
        v, w = univecController(robot, robot.target, avoidObst=False, stopWhenArrive=stop)
    else:    
        obst = [friend, enemy1, enemy2, enemy3, enemy4, enemy5]
        robot.obst.update(robot, obst)
        v, w = univecController(robot, robot.target, avoidObst=True, obst=robot.obst, stopWhenArrive=stop)
    
    robot.simSetVel(v, w)

def atacante_secundario1(robot_leader, robot):
    if robot.teamYellow:
        xPos = robot_leader.xPos/2
        yPos = robot_leader.yPos
        theta = robot_leader.theta
    if not robot.teamYellow:
        xPos = (220 - robot_leader.xPos)/2
        yPos = robot_leader.yPos
        theta = robot_leader.theta

    robot.target.update(xPos, yPos, theta)
    v, w = univecController(robot, robot.target, avoidObst=False, stopWhenArrive=True)
    robot.simSetVel(v, w)

def atacante_secundario(robot_leader, robot):
    if robot.teamYellow:
        xPos = robot_leader.xPos + 20
        if robot_leader.yPos > 90:
            yPos = robot_leader.yPos - 10
        else:
            yPos = robot_leader.yPos + 10
        theta = robot_leader.theta
    if not robot.teamYellow:
        xPos = robot_leader.xPos - 20
        if robot_leader.yPos > 90:
            yPos = robot_leader.yPos - 10
        else:
            yPos = robot_leader.yPos + 10
        theta = robot_leader.theta

    robot.target.update(xPos, yPos, theta)
    v, w = univecController(robot, robot.target, avoidObst=False, stopWhenArrive=True)
    robot.simSetVel(v, w)

def atacante_idle(robot, up, move=False, ball=None):

    if robot.teamYellow:
        xPos = 180

    if not robot.teamYellow:
        xPos = 70

    if not move:
        if up:
            yPos = 160
            theta = deg2rad(-90)

        if not up:
            yPos = 20
            theta = deg2rad(90)
    else:
        if up:
            yPos = calculaPosIdle(ball, up)
            theta = deg2rad(-90)
            
        if not up:
            yPos = calculaPosIdle(ball, up)
            theta = deg2rad(90)
            
    robot.target.update(xPos, yPos, theta)
    v, w = univecController(robot, robot.target, avoidObst=False, stopWhenArrive=True, doubleFace=True)
    robot.simSetVel(v, w)


def calculaPosIdle(ball, up):
    if up:
        if ball.yPos < 90:
            yPos = 100
        elif ball.yPos <= 160:
            yPos = ball.yPos + 10
        else:
            yPos = 160
    if not up:
        if ball.yPos > 90:
            yPos = 80
        elif ball.yPos >= 20:
            yPos = ball.yPos - 10
        else:
            yPos = 20
    
    return yPos

def idle(robot1, robot2):
    atacante_idle(robot1, True)
    atacante_idle(robot2, False)



def defesa_atacantes(ball, robot0, robot1, robot2, robot3, robot4, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4):
    
    #verifica_area(robot3, True)
    #verifica_area(robot3, False)

    if robot3.yPos > robot4.yPos:
        up = True
    else:
        up = False

    if robot0.teamYellow and ball.xPos > 180 and ball.yPos > 50 and ball.yPos < 130:
        atacante_idle(robot3, up, True, ball)
        atacante_idle(robot4, not up, True, ball)
    
    if (not robot0.teamYellow) and ball.xPos < 70 and ball.yPos > 50 and ball.yPos < 130:
        atacante_idle(robot3, up, True, ball)
        atacante_idle(robot4, not up, True, ball)
    
    if robot0.teamYellow and (ball.xPos < 180 or ball.yPos < 50 or ball.yPos > 130):
        leaderSelector(robot3, robot4, ball)

        if robot3.isLeader:
            defenderSpin(robot3, ball, not robot3.teamYellow, robot1, robot2, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
            atacante_idle(robot4, not up, True, ball)
            #follower(robot4, robot3, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
        if robot4.isLeader:
            defenderSpin(robot4, ball, not robot3.teamYellow, robot1, robot2, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
            atacante_idle(robot3, up, True, ball)
            #follower(robot3, robot4, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
    
    if (not robot0.teamYellow) and (ball.xPos > 70 or ball.yPos < 50 or ball.yPos > 130):
        leaderSelector(robot3, robot4, ball)

        if robot3.isLeader:
            defenderSpin(robot3, ball, not robot3.teamYellow, robot1, robot2, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
            atacante_idle(robot4, not up, True, ball)
            #follower(robot4, robot3, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
        if robot4.isLeader:
            defenderSpin(robot4, ball, not robot3.teamYellow, robot1, robot2, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
            atacante_idle(robot3, up, True, ball)
            #follower(robot3, robot4, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)

def defesa_atacante_solo(ball, robot0, robot1, robot2, robot3, robot4, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4):
    if ball.yPos > 90:
        up = True
    else:
        up = False

    if robot0.teamYellow and ball.xPos > 180 and ball.yPos > 50 and ball.yPos < 130:
        atacante_idle(robot3, up, True, ball)
    
    if (not robot0.teamYellow) and ball.xPos < 70 and ball.yPos > 50 and ball.yPos < 130:
        atacante_idle(robot3, up, True, ball)
    
    if robot0.teamYellow and (ball.xPos < 180 or ball.yPos < 50 or ball.yPos > 130):
        defenderSpin(robot3, ball, not robot3.teamYellow, robot1, robot2, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
    
    if (not robot0.teamYellow) and (ball.xPos > 70 or ball.yPos < 50 or ball.yPos > 130):
        defenderSpin(robot3, ball, not robot3.teamYellow, robot1, robot2, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)


def ataque(ball, robot1, robot2, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4):

    if (not robot1.teamYellow) and ball.xPos < 150 and ball.yPos > 50 and ball.yPos < 130:
        defenderSpin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot2, friend2=robot2, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
        defenderSpin(robot2, ball, left_side=not robot1.teamYellow, friend1=robot1, friend2=robot1, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
        
    elif robot1.teamYellow and ball.xPos < 70 and ball.yPos > 50 and ball.yPos < 130:
        defenderSpin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot2, friend2=robot2, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
        defenderSpin(robot2, ball, left_side=not robot1.teamYellow, friend1=robot1, friend2=robot1, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
    else:
        leaderSelector(robot1, robot2, ball)

        if robot1.isLeader:
            defenderSpin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot2, friend2=robot2, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
            mirror_follower(robot2, robot1, ball)
        if robot2.isLeader:
            defenderSpin(robot2, ball, left_side=not robot1.teamYellow, friend1=robot1, friend2=robot1, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
            mirror_follower(robot1, robot2, ball)

def triple_ataque(ball, robot1, robot2, robot3, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4):

    if (not robot1.teamYellow) and ball.xPos < 150 and ball.yPos > 50 and ball.yPos < 130:
        defenderSpin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot3, friend2=robot2, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
        defenderSpin(robot2, ball, left_side=not robot1.teamYellow, friend1=robot1, friend2=robot3, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
        defenderSpin(robot3, ball, left_side=not robot1.teamYellow, friend1=robot2, friend2=robot1, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
        
    elif robot1.teamYellow and ball.xPos < 70 and ball.yPos > 50 and ball.yPos < 130:
        defenderSpin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot2, friend2=robot3, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
        defenderSpin(robot2, ball, left_side=not robot1.teamYellow, friend1=robot1, friend2=robot3, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
        defenderSpin(robot3, ball, left_side=not robot1.teamYellow, friend1=robot2, friend2=robot1, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
    else:
        triple_leaderSelector(robot1, robot2, robot3, ball)

        if robot1.isLeader:
            defenderSpin(robot1, ball, left_side=not robot1.teamYellow, friend1=robot2, friend2=robot3, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
            mirror_follower(robot2, robot1, ball)
            robot3_idle(robot3, robot1, robot2, ball)
        if robot2.isLeader:
            defenderSpin(robot2, ball, left_side=not robot1.teamYellow, friend1=robot1, friend2=robot3, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
            mirror_follower(robot1, robot2, ball)
            robot3_idle(robot3, robot1, robot2, ball)
        if robot3.isLeader:
            defenderSpin(robot3, ball, left_side=not robot1.teamYellow, friend1=robot1, friend2=robot2, 
                    enemy1=robot_enemy_0, enemy2=robot_enemy_1, enemy3=robot_enemy_2, enemy4=robot_enemy_3, enemy5=robot_enemy_4)
            idle_ataque(robot2, ball)
            mirror_follower(robot1, robot2, ball)

def robot3_idle(robot, robot1, robot2, ball):
    
    if robot.teamYellow:
        xPos = robot1.xPos + 25
    else:
        xPos = robot1.xPos - 25

    yPos = (robot1.yPos + robot2.yPos)/2

    dist = sqrt((robot.xPos - xPos) ** 2 + (robot.yPos - yPos) ** 2)
    arrival_theta = arctan2(ball.yPos - robot.yPos, ball.xPos - robot.xPos)
    robot.target.update(xPos, yPos, arrival_theta)

    if dist<10:
        stop(robot)
    else:
        v, w = univecController(robot, robot.target, avoidObst=False, n=16, d=2)
        robot.simSetVel(v, w)


def idle_ataque(robot, ball, robot0=None, robot_enemy_0=None, robot_enemy_1=None, robot_enemy_2=None, robot_enemy_3=None, robot_enemy_4=None):

    '''
    Defines the position of the follower based on the leader position, the position is a mirror position based on the leader
    '''

    if robot.teamYellow:
        proj_x = ball.xPos - 15
    else:
        proj_x = ball.xPos + 15

    if proj_x >= 220:
        proj_x = 220
    
    if proj_x <= 30:
        proj_x = 30

    proj_y = 45

    '''
    Calculate distante between the follower and the projected point
    '''
    dist = sqrt((robot.xPos - proj_x) ** 2 + (robot.yPos - proj_y) ** 2)
    arrival_theta = arctan2(ball.yPos - robot.yPos, ball.xPos - robot.xPos)
    robot.target.update(proj_x, proj_y, arrival_theta)

    if dist < 10: # Check if the robot is close to the projected point and stops the robot
        stop(robot)
    else:
        # No friends to avoid
        if robot0 is None and robot_enemy_0 is None and robot_enemy_1 is None and robot_enemy_2 is None:
            v, w = univecController(robot, robot.target, avoidObst=False, n=16, d=2)
        else:  # Both friends to avoid
            robot.obst.update2(robot, ball, robot0, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
            v, w = univecController(robot, robot.target, True, robot.obst, n=4, d=4)

        robot.simSetVel(v, w)

def ataque2(ball, robot1, robot2, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4):

    if (not robot1.teamYellow) and ball.xPos < 150 and ball.yPos > 50 and ball.yPos < 130:
        atacante_lider(robot1, ball, robot2, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
        atacante_lider(robot2, ball, robot1, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
        
    elif robot1.teamYellow and ball.xPos < 70 and ball.yPos > 50 and ball.yPos < 130:
        atacante_lider(robot1, ball, robot2, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
        atacante_lider(robot2, ball, robot1, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)

    else:
        leaderSelector(robot1, robot2, ball)

        if robot1.isLeader:
            atacante_lider(robot1, ball, robot2, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
            follower(robot2, robot1, ball)
        if robot2.isLeader:
            atacante_lider(robot2, ball, robot1, robot_enemy_0, robot_enemy_1, robot_enemy_2, robot_enemy_3, robot_enemy_4)
            follower(robot1, robot2, ball)

def circumferencePointProjectionSolo(ballTheta,r,xgoal, ygoal):
    #print("robotTheta1 = %.2f" %robotTheta1 +" robotTheta2 = %.2f" %robotTheta2)

    # Calcula a projeção usando a fórmula
    xtarget = xgoal + r * cos(ballTheta)
    ytarget = ygoal + r * sin(ballTheta)

    # Retorna as coordenadas da projeção
    return xtarget, ytarget

def circumferencePointProjection(robotTheta1, robotTheta2, ballTheta,r,xgoal, ygoal):
    #Verifica qual melhor formação para os dois robôs
    if robotTheta1 > robotTheta2:
        ballTheta1 = ballTheta + 8*pi/180 # + 10 graus
        ballTheta2 = ballTheta - 8*pi/180 # - 10 graus
    else:
        ballTheta1 = ballTheta - 8*pi/180 # + 10 graus
        ballTheta2 = ballTheta + 8*pi/180 # - 10 graus

    #print("robotTheta1 = %.2f" %robotTheta1 +" robotTheta2 = %.2f" %robotTheta2)

    # Calcula a projeção usando a fórmula
    xtarget1 = xgoal + r * cos(ballTheta1)
    ytarget1 = ygoal + r * sin(ballTheta1)
    xtarget2 = xgoal + r * cos(ballTheta2)
    ytarget2 = ygoal + r * sin(ballTheta2)

    # Retorna as coordenadas da projeção
    return xtarget1, ytarget1, xtarget2, ytarget2

def adjustArrivalThetaWall(ballTheta, leftSide, robotTheta):
    if (ballTheta < robotTheta):  
        arrivalTheta = ballTheta - pi/2 
    else:
        arrivalTheta = ballTheta + pi/2


    return arrivalTheta

def defenderWall(robot1, robot2, ball,leftSide=True):
    xgoal = 15 if leftSide else 235
    raio = 30

    ballTheta=arctan2(ball.yPos-90,ball.xPos-xgoal)
    robotTheta1=arctan2(robot1.yPos-90,robot1.xPos-xgoal)
    robotTheta2=arctan2(robot2.yPos-90,robot2.xPos-xgoal)

    if not leftSide:
        if ballTheta < 0:
            ballTheta += 2*pi
        if robotTheta1 < 0:
            robotTheta1 += 2*pi        
        if robotTheta2 < 0:
            robotTheta2 += 2*pi

    xtarget1, ytarget1, xtarget2, ytarget2 = circumferencePointProjection(robotTheta1, robotTheta2, ballTheta, raio, xgoal, 90)

    arrivalTheta1 = adjustArrivalThetaWall(ballTheta, ball, robotTheta1)
    arrivalTheta2 = adjustArrivalThetaWall(ballTheta, ball, robotTheta2)

    #print("POS = %.2f" %xtarget2 +" / %.2f" %ytarget2 + "   ANG = %.2f" %arrivalTheta2)

    robot1.target.update(xtarget1, ytarget1, arrivalTheta1)
    v,w=univecController(robot1,robot1.target,avoidObst=False, doubleFace=True, stopWhenArrive = True)
    robot1.simSetVel(v*1.2,w*1.2)
    robot2.target.update(xtarget2, ytarget2, arrivalTheta2)
    v,w=univecController(robot2,robot2.target,avoidObst=False, doubleFace=True, stopWhenArrive = True)
    robot2.simSetVel(v*1.2,w*1.2)

def defenderWallSolo(robot, ball,leftSide=True):
    xgoal = 15 if leftSide else 235

    ballTheta=arctan2(ball.yPos-90,ball.xPos-xgoal)
    robotTheta=arctan2(robot.yPos-90,robot.xPos-xgoal)

    if not leftSide:
        if ballTheta < 0:
            ballTheta += 2*pi
        if robotTheta < 0:
            robotTheta += 2*pi        


    xtarget, ytarget = circumferencePointProjectionSolo(ballTheta, 40, xgoal, 90)

    arrivalTheta = adjustArrivalThetaWall(ballTheta, ball, robotTheta)

    #print("POS = %.2f" %xtarget2 +" / %.2f" %ytarget2 + "   ANG = %.2f" %arrivalTheta2)

    robot.target.update(xtarget, ytarget, arrivalTheta)
    v,w=univecController(robot,robot.target,avoidObst=False, doubleFace=True, stopWhenArrive = True)
    robot.simSetVel(v*1.2,w*1.2)


def cruzamento(ball, robot2, robot3, alvo):

    alvo = 0 if alvo == 1 and ball.yPos < 90 and ball.xPos > 125 else alvo 
    alvo = 0 if alvo == 2 and ball.yPos < 90 and ball.xPos < 125 else alvo 
    alvo = 0 if alvo == 3 and ball.yPos > 90 and ball.xPos < 125 else alvo 
    alvo = 0 if alvo == 4 and ball.yPos > 90 and ball.xPos > 125 else alvo 

    xPos = 0
    yPos = 0
    theta = 0

    if alvo == 2 or alvo == 3:
        xPos = ball.xPos
        yPos = ball.yPos
        theta = math.atan2(90 - ball.yPos, ball.xPos - 95)
        theta = math.pi - theta

    if alvo == 1 or alvo == 4:
        xPos = ball.xPos
        yPos = ball.yPos
        theta = math.atan2(90 - ball.yPos, 155 - ball.xPos)

    robot2.target.update(xPos, yPos, theta)
    robot3.target.update(xPos, yPos, theta)
    v,w=univecController(robot2,robot2.target,avoidObst=False, doubleFace=True, stopWhenArrive = True)
    robot2.simSetVel(v,w)
    v,w=univecController(robot3,robot3.target,avoidObst=False, doubleFace=True, stopWhenArrive = True)
    robot3.simSetVel(v,w)


def breakWall(robot, ball, quadrant, friend1=None, friend2=None, enemy1=None, enemy2=None, enemy3=None, enemy4=None, enemy5=None, leftSide=True):
    r = 32
    xgoal = 235 if leftSide else 15
    side = 1 if leftSide else 0
    xtarget = xgoal + r * cos(pi*side)
    ytarget = 90 + r * sin(pi*side)      
    arrivalTheta = 90
    robot.obst.update2(robot, ball, friend1, friend2, enemy1, enemy2, enemy3, enemy4, enemy5)
        
    robot.target.update(xtarget, ytarget, arrivalTheta)
    v,w=univecController(robot,robot.target,True, robot.obst, doubleFace=True, stopWhenArrive = True)
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
    #friends = robot.get_friends()
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
        if robot.yPos> 65:
            arrival_angle = -deg2rad(15)
        else:
            arrival_angle = deg2rad(15)
    else:
        if robot.yPos> 65:
            arrival_angle = -deg2rad(165)
        else:
            arrival_angle = deg2rad(165)
    return arrival_angle