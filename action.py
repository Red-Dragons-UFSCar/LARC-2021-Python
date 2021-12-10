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
        robot.obst.update2(robot, ball, friends, enemys)
        v,w=univecController(robot,robot.target,True,robot.obst,n=4, d=4)

    robot.simSetVel(v,w)

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

def defenderSpin(robot,ball,leftSide=True,friends=[],enemys=[]):
    if leftSide:
        arrivalTheta=arctan2(90-ball.yPos,235-ball.xPos) #? Angle between the ball and point (150,65)
    else:
        arrivalTheta=arctan2(90-ball.yPos,15-ball.xPos) #? Angle between the ball and point (0,65)
    #robot.target.update(ball.xPos,ball.yPos,0)
    robot.target.update(ball.xPos,ball.yPos,arrivalTheta)

    if not friends: #? No friends to avoid
        v,w=univecController(robot,robot.target,avoidObst=False,n=16, d=2)
    else: #? Both friends to avoid
        #robot.obst.update(robot,friend1,friend2,enemy1,enemy2,enemy3)
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
    if d < 30 and ball.xPos > robot.xPos:
        if robot.teamYellow:
            dx = 15-robot.xPos
        else:
            dx = 235 - robot.xPos
        dy = tan(robot.theta)*dx + robot.yPos
        if dy > 70 and dy < 110:
            if robot.index == 2 or robot.index == 1:
                robot.simSetVel2(50*robot.face, 50*robot.face)
            else:
                robot.simSetVel(v,w)
        else:
            robot.simSetVel(v,w)
    else:
        robot.simSetVel(v,w)

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

def slave(robotSlave, robotMaster, friends, enemys, ball):

    if robotMaster.yPos > 90:
        if robotMaster.xPos > 126:
            projX = robotMaster.xPos - 15
            projY = robotMaster.yPos - 30
        else:
            projX = robotMaster.xPos + 15
            projY = robotMaster.yPos - 30
    else:
        if robotMaster.xPos > 126:
            projX = robotMaster.xPos - 15
            projY = robotMaster.yPos + 30
        else:
            projX = robotMaster.xPos + 15
            projY = robotMaster.yPos + 30

    dist = sqrt((robotSlave.xPos - projX)**2 + (robotSlave.yPos - projY)**2)
    robotSlave.target.update(projX,projY,0)

    if dist < 10:
        stop(robotSlave)
    else:
        if not friends:  #? No friends to avoid
            v,w=univecController(robotSlave,robotSlave.target,avoidObst=False,n=16, d=2)
        else: #? Both friends to avoid
            #obstacles = robots + [robotMaster]
            #robotSlave.obst.update(robotSlave, obstacles)
            friends = friends + [robotMaster]
            robotSlave.obst.update2(robotSlave,ball,friends,enemys)
            v,w=univecController(robotSlave,robotSlave.target,True,robotSlave.obst,n=4, d=4)

        robotSlave.simSetVel(v,w)


def Master_Slave(robot1, robot2, friends, enemys, ball):

    dist1 = sqrt((robot1.xPos - ball.xPos)**2 + (robot1.yPos - ball.yPos)**2)
    ang1  = arctan2(ball.yPos - robot1.yPos,ball.xPos - robot1.xPos)

    dist2 = sqrt((robot2.xPos - ball.xPos)**2 + (robot2.yPos - ball.yPos)**2)
    ang2  = arctan2(ball.yPos - robot2.yPos,ball.xPos - robot2.xPos )

    w1 = 0.20*(1-cos(ang1 - robot1.theta)) + 0.80*dist1/(dist1+dist2)
    w2 = 0.20*(1-cos(ang2 - robot2.theta)) + 0.80*dist2/(dist1+dist2)

    if dist1 > dist2:
        if not robot1.teamYellow:
            # linhas 352 e 353 condicionais para não entrar no gol, o mesmo para 365 e 366
            if ball.xPos < 40 and (ball.yPos < 130 and ball.yPos > 50):
                if robot1.xPos < 55:
                    screenOutBall(robot2, robot2, 55, leftSide=not robot2.teamYellow, upperLim=170, lowerLim=10)
                else:
                    screenOutBall(robot2, ball, 55, leftSide=not robot2.teamYellow, upperLim=170, lowerLim=10)
                slave(robot1,robot2, friends, enemys, ball)

            else:
                friends = friends + [friends[0]] #Adequando pro update2 apenas
                defenderSpin(robot2,ball,not robot2.teamYellow, friends, enemys)
                slave(robot1,robot2, friends, enemys, ball)
        else:
            if ball.xPos > 195 and (ball.yPos < 130 and ball.yPos > 50):
                if robot1.xPos > 180:
                    screenOutBall(robot2, robot2, 55, leftSide=not robot2.teamYellow, upperLim=170, lowerLim=10)
                else:
                    screenOutBall(robot2, ball, 55, leftSide=not robot2.teamYellow, upperLim=170, lowerLim=10)
                slave(robot1,robot2, friends, enemys, ball)

            else:
                friends = friends + [friends[0]] #Adequando pro update2 apenas
                defenderSpin(robot2,ball,not robot2.teamYellow, friends, enemys)
                slave(robot1,robot2, friends, enemys, ball)

    else:
        if not robot1.teamYellow:
            if ball.xPos < 40 and (ball.yPos < 130 and ball.yPos > 50):
                if robot1.xPos < 55:
                    screenOutBall(robot1, robot1, 55, leftSide=not robot1.teamYellow, upperLim=170, lowerLim=10)
                else:
                    screenOutBall(robot1, ball, 55, leftSide=not robot1.teamYellow, upperLim=170, lowerLim=10)
                slave(robot2,robot1, friends, enemys, ball)

            else:
                friends = friends + [friends[0]] #Adequando pro update2 apenas
                defenderSpin(robot1,ball,not robot1.teamYellow, friends, enemys)
                slave(robot2,robot1, friends, enemys, ball)
        else:
            if ball.xPos > 195 and (ball.yPos < 130 and ball.yPos > 50):
                if robot1.xPos > 180:
                    screenOutBall(robot1, robot1, 55, leftSide=not robot1.teamYellow, upperLim=170, lowerLim=10)
                else:
                    screenOutBall(robot1, ball, 55, leftSide=not robot1.teamYellow, upperLim=170, lowerLim=10)
                slave(robot2,robot1, friends, enemys, ball)

            else:
                friends = friends + [friends[0]] #Adequando pro update2 apenas
                defenderSpin(robot1,ball,not robot1.teamYellow, friends, enemys)
                slave(robot2,robot1, friends, enemys, ball)

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
