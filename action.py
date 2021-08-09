from numpy import pi,cos,sin,tan,arctan2,sqrt ,matmul,array
from execution import univecController, whichFace
from behaviours import Univector

#% Basic Actions
def stop(robot):
    robot.simSetVel(0,0)

def sweepBall(robot,leftSide=True):
    if leftSide:
        w=-0.5*robot.vMax*robot.R/robot.L
    else:
        w=0.5*robot.vMax*robot.R/robot.L

    if robot.yPos > 65:
        robot.simSetVel(0,w)
    else:
        robot.simSetVel(0,-w)

def positionToSweep(robot,ball,leftSide=True,friend1=None,friend2=None):
    if leftSide:
        robot.target.update(ball.xPos,ball.yPos,0)
    else:
        robot.target.update(ball.xPos,ball.yPos,pi)

    if friend1 is None and friend2 is None: #? No friends to avoid
        v,w=univecController(robot,robot.target,avoidObst=False)
    else: #? Both friends to avoid
        robot.obst.update(robot,friend1,friend2)
        v,w=univecController(robot,robot.target,True,robot.obst)

    robot.simSetVel(v,w)

def avoidBound(robot,friend1=None,friend2=None):
    #% Verify if the dot product between the robot and the point (135,65) is positive
    #% It means the angle resides in ]-pi/2,pi/2[
    dotProd=(cos(robot.theta))*(135-robot.xPos)+(sin(robot.theta))*(65-robot.yPos)

    if dotProd >= 0:
        arrivalTheta=arctan2(65-robot.yPos,135-robot.xPos)
        robot.target.update(135,65,arrivalTheta)
    else:
        arrivalTheta=arctan2(65-robot.yPos,15-robot.xPos)
        robot.target.update(15,65,arrivalTheta)

    if friend1 is None and friend2 is None: #? No friends to avoid
        v,w=univecController(robot,robot.target,avoidObst=False)
    else: #? Both friends to avoid
        robot.obst.update(robot,friend1,friend2)
        v,w=univecController(robot,robot.target,True,robot.obst)

    robot.simSetVel(v,w)

def holdPosition(robot,xg,yg,desTheta,friend1=None,friend2=None):
    robot.target.update(xg,yg,desTheta)

    if friend1 is None and friend2 is None: #? No friends to avoid
        v,w=univecController(robot,robot.target,avoidObst=False,stopWhenArrive=True)
    else: #? Both friends to avoid
        robot.obst.update(robot,friend1,friend2)
        v,w=univecController(robot,robot.target,True,robot.obst,stopWhenArrive=True)

    robot.simSetVel(v,w)

#% Attacker Actions
def shoot(robot,ball,leftSide=True,friend1=None,friend2=None, enemy1=None,  enemy2=None, enemy3=None):
    if leftSide:
        arrivalTheta=arctan2(65-ball.yPos,150-ball.xPos) #? Angle between the ball and point (150,65)
    else:
        arrivalTheta=arctan2(65-ball.yPos,-ball.xPos) #? Angle between the ball and point (0,65)
    #robot.target.update(ball.xPos,ball.yPos,0)
    robot.target.update(ball.xPos,ball.yPos,arrivalTheta)

    if friend1 is None and friend2 is None: #? No friends to avoid
        v,w=univecController(robot,robot.target,avoidObst=False,n=16, d=2)
    else: #? Both friends to avoid
        robot.obst.update(robot,friend1,friend2,enemy1,enemy2,enemy3)
        v,w=univecController(robot,robot.target,True,robot.obst,n=4, d=4)

    robot.simSetVel(v,w)

#% Defender Actions
def pushBall(robot,ball,friend1=None,friend2=None):
    dSup=sqrt((75-ball.xPos)**2+(130-ball.yPos)**2) #? Distance between the ball and point (75,130)
    dInf=sqrt((75-ball.xPos)**2+(0-ball.yPos)**2)   #? Distance between the ball and point (75,0)

    if dSup<=dInf:
        arrivalTheta=arctan2(130-ball.yPos,75-ball.xPos) #? Angle between the ball and point (75,130)
    else:
        arrivalTheta=arctan2(-ball.yPos,75-ball.xPos) #? Angle between the ball and point (75,0)
    robot.target.update(ball.xPos,ball.yPos,arrivalTheta)

    if friend1 is None and friend2 is None: #? No friends to avoid
        v,w=univecController(robot,robot.target,avoidObst=False)
    else: #? Both friends to avoid
        robot.obst.update(robot,friend1,friend2)
        v,w=univecController(robot,robot.target,True,robot.obst)

    robot.simSetVel(v,w)

#TODO #2 Need more speed to reach the ball faster than our enemy
def screenOutBall(robot,ball,staticPoint,leftSide=True,upperLim=200,lowerLim=0,friend1=None,friend2=None):
    #Check if ball is inside the limits
    if ball.yPos >= upperLim:
        yPoint = upperLim

    elif ball.yPos <= lowerLim:
        yPoint = lowerLim

    else:
        yPoint = ball.yPos
    #Check the field side
    if leftSide:
        if robot.yPos <= ball.yPos:
            arrivalTheta=pi/2
        else:
            arrivalTheta=-pi/2
        robot.target.update(staticPoint,yPoint,arrivalTheta)
    else:
        if robot.yPos <= ball.yPos:
            arrivalTheta=pi/2
        else:
            arrivalTheta=-pi/2
        robot.target.update(150 - staticPoint,yPoint,arrivalTheta)

    if friend1 is None and friend2 is None: #? No friends to avoid
        v,w=univecController(robot,robot.target,avoidObst=False,stopWhenArrive=True)
    else: #? Both friends to avoid
        robot.obst.update(robot,friend1,friend2)
        v,w=univecController(robot,robot.target,True,robot.obst,stopWhenArrive=True)

    robot.simSetVel(v,w)

#% Goalkeeper Actions
#TODO #1 More effective way to predict the ball position
def blockBall(robot,ball,leftSide=True):
    ballVec=(ball.pastPose[:,1]-ball.pastPose[:,0]).reshape(2,1) #? Building a vector between current and past position of the ball
    if leftSide:
        alpha=(9-ball.xPos)/(ballVec[0]+0.000000001)
        desY=ball.yPos+alpha*ballVec[1]
        if desY <= 82 and desY >= 48: #? If the projection of the ball is inside of our goal, we manage the goalkeeper to the
            if robot.yPos <= desY:   #? point (9,y_projected)
                arrivalTheta=pi/2
            else:
                arrivalTheta=-pi/2
            robot.target.update(9,float(desY),arrivalTheta)
        else:                       #? Else we manage the goalkeeper to the center of the goal, at point (9,65)
            if robot.yPos <= 65:
                arrivalTheta=pi/2
            else:
                arrivalTheta=-pi/2
            robot.target.update(9,65,arrivalTheta)
        v,w=univecController(robot,robot.target,None,False,stopWhenArrive=True)
        robot.simSetVel(v,w)
    else:
        alpha=(141-ball.xPos)/(ballVec[0]+0.000000001)
        desY=ball.yPos+alpha*ballVec[1]
        if desY <= 82 and desY >= 48: #? If the projection of the ball is inside of our goal, we manage the goalkeeper to the
            if robot.yPos <= desY:   #? point (141,y_projected)
                arrivalTheta=pi/2
            else:
                arrivalTheta=-pi/2
            robot.target.update(141,float(desY),arrivalTheta)
        else:                       #? Else we manage the goalkeeper to the center of the goal, at point (141,65)
            if robot.yPos <= 65:
                arrivalTheta=pi/2
            else:
                arrivalTheta=-pi/2
            robot.target.update(141,65,arrivalTheta)
        v,w=univecController(robot,robot.target,None,False,stopWhenArrive=True)
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

        if (robot.yPos < 100 and robot.yPos > 65):
            if robot.yPos < ball.yPos:
                arrivalTheta = (pi/2 + theta)
            if robot.yPos > ball.yPos:
                arrivalTheta = -(pi/2 - theta)

        if (robot.yPos < 65 and robot.yPos > 30):
            if robot.yPos < ball.yPos:
                arrivalTheta = pi/2 + theta
            if robot.yPos > ball.yPos:
                arrivalTheta = -(pi/2 - theta)

        if robot.yPos < 30:
            if robot.xPos < ball.xPos:
                arrivalTheta = pi/2 + theta

            if robot.xPos >= ball.xPos:
                arrivalTheta = -(pi/2 - theta)

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

def ballCrossing(robotAtacker, ball, arraySideCrossing, leftSide = True,robotDefender = None,robotGoalkeeper=None):
    if( arraySideCrossing[0] or (robotAtacker.flagCruzamento and robotAtacker.yPos < 65)): #For left-down side
        arrivalTheta = arctan2(115-ball.yPos,75-ball.xPos)
        robotAtacker.target.update(ball.xPos, ball.yPos, arrivalTheta)
        robotDefender.target.update(85, 85, arrivalTheta-pi)
        robotAtacker.flagCruzamento = True
    elif( arraySideCrossing[1] or (robotAtacker.flagCruzamento and robotAtacker.yPos > 65)): #For left-up side
        arrivalTheta = -pi + arctan2(ball.yPos-25,ball.xPos-75)
        robotAtacker.target.update(ball.xPos, ball.yPos, arrivalTheta)
        robotDefender.target.update(85, 45, arrivalTheta+pi)
        robotAtacker.flagCruzamento = True

    if robotGoalkeeper is None: # Setting velocity for robots
        va,wa=univecController(robotAtacker,robotAtacker.target,avoidObst=False)
        vd,wd=univecController(robotDefender,robotDefender.target,avoidObst=False)
    else: #? Both friends to avoid
        robotAtacker.obst.update(robotAtacker,robotDefender,robotGoalkeeper)
        va,wa=univecController(robotAtacker,robotAtacker.target,True,robotAtacker.obst)
        robotAtacker.obst.update(robotDefender,robotAtacker,robotGoalkeeper)
        if(robotDefender.dist(robotDefender.target) < 5):#Code for stop robot when he arrive in the target
            stop(robotDefender)
        else:
            vd,wd=univecController(robotDefender,robotDefender.target,True,robotDefender.obst)
            robotDefender.simSetVel(vd,wd)
    robotAtacker.simSetVel(va,wa)


def verifyCrossing(robotAtacker, ball, leftSide = True,robotDefender = None,robotGoalkeeper=None):
    x_t = (150 - 40/tan(pi/6))
    arraySideCrossing = [False, False] #[Left-Down, Left-Up]
    flagCrossing = False
    #Ball in corners - Triangular Area
    if(robotAtacker.xPos > (150 - x_t) and (robotAtacker.yPos < (robotAtacker.xPos - x_t)*tan(pi/6))): #For left-down side
        arraySideCrossing[0] = True
        flagCrossing = True
    elif(robotAtacker.xPos > (150 - x_t) and (robotAtacker.yPos > 130 - (robotAtacker.xPos - x_t)*tan(pi/6))): #For left-up side
        arraySideCrossing[1] = True
        flagCrossing = True
    elif(robotAtacker.flagCruzamento):
        flagCrossing = True
    return arraySideCrossing, flagCrossing

def positionChange(arrayFunctions, ball, arraySideCrossing, leftSide = True):
    if(arrayFunctions[2].flagCruzamento and (not arraySideCrossing[0]) and (not arraySideCrossing[1])):
        if( (ball.yPos >  30 and ball.yPos <  100) and (ball.xPos >  92.5 and ball.xPos <  132.5)):
            arrayFunctions[1], arrayFunctions[2] = arrayFunctions[2], arrayFunctions[1]#Switching positions
            arrayFunctions[2].flagCruzamento = False
        elif(arrayFunctions[2].dist(ball) > 30):
            arrayFunctions[2].flagCruzamento = False
        elif((ball.yPos >  45 and ball.yPos <  85) and (ball.xPos >  132.5 and ball.xPos <  150)):
            arrayFunctions[2].flagCruzamento = False
        elif((ball.yPos >  105) and (ball.xPos >  75 and ball.xPos <  112.5)):
            arrayFunctions[2].flagCruzamento = False
        elif((ball.yPos <  25) and (ball.xPos >  75 and ball.xPos <  112.5)):
            arrayFunctions[2].flagCruzamento = False
    return arrayFunctions

def girar(robot):
    robot.simSetVel(0,0)
