from numpy import cos,sin,arctan2,sqrt,sign,pi,delete,append,array
from behaviours import Univector
from copy import deepcopy

#% Function to approximate phi_v
def approx(robot,target,avoidObst=True,obst=None,n=8,d=2):
    navigate=Univector() #? Defines the navigation algorithm
    dl=0.000001          #? Constant to approximate phi_v

    x=robot.xPos #? Saving (x,y) coordinates to calculate phi_v
    y=robot.yPos
    robot.xPos=robot.xPos+dl*cos(robot.theta) #? Incrementing robot (x,y) position
    robot.yPos=robot.yPos+dl*sin(robot.theta)

    if avoidObst:
        stpTheta=navigate.univecField_N(robot,target,obst,n,d) #? Computing a step Theta to determine phi_v
    else:
        stpTheta=navigate.nVecField(robot,target,n,d,haveFace=True) #? Computing a step Theta to determine phi_v

    robot.xPos=x #? Returning original (x,y) coordinates
    robot.yPos=y

    return stpTheta

#% Function to control the robot with or without collision avoidance
def univecController(robot,target,avoidObst=True,obst=None,n=8,d=2,stopWhenArrive=False, doubleFace=True):
    inCorner(target,robot)
    navigate=Univector() #? Defines the navigation algorithm
    dl=0.000001          #? Constant to approximate phi_v
    k_w=1                #? Feedback constant (k_w=1 means no gain)
    k_p=1                #? Feedback constant (k_p=1 means no gain)
    robot_aux = deepcopy(robot)

    if doubleFace:
        whichFace(robot, target)

    #% Navigation: Go-to-Goal + Avoid Obstacle Vector Field
    if avoidObst:
        desTheta=navigate.univecField_N(robot,target,obst,n,d) #? Desired angle w/ gtg and ao vector field
    #% Navigation: Go-to-Goal Vector Field
    else:
        desTheta=navigate.nVecField(robot,target,n,d, haveFace=False) #? Desired angle w/ gtg

    stpTheta=approx(robot,target,avoidObst,obst,n,d)
    phi_v=arctan2(sin(stpTheta-desTheta),cos(stpTheta-desTheta))/dl #? Trick to mantain phi_v between [-pi,pi]
    theta_e=arctan2(sin(desTheta-robot.theta),cos(desTheta-robot.theta)) #? Trick to mantain theta_e between [-pi,pi]
    v1=(2*robot.vMax-robot.LSimulador*k_w*sqrt(abs(theta_e)))/(2+robot.LSimulador*abs(phi_v))
    v2=(sqrt(k_w**2+4*robot.rMax*abs(phi_v))-k_w*sqrt(abs(theta_e)))/(2*abs(phi_v)+dl)

    if stopWhenArrive:
        v3=k_p*robot.dist(target)
    else:
        v3=robot.vMax

    v=min(abs(v1),abs(v2),abs(v3))
    w=v*phi_v+k_w*sign(theta_e)*sqrt(abs(theta_e))

    #% Some code to store the past position, orientation and velocity
    robot.v=v
    robot.pastPose=delete(robot.pastPose,0,1) #? Deleting the first column
    robot.pastPose=append(robot.pastPose,array([[round(robot.xPos)],[round(robot.yPos)],[round(float(robot.theta))],[round(float(v))]]),1)

    return v,w

#'''
def whichFace(robot,target): #Apenas mudar o -1 aqui funciona!
    pgVec=array([[target.xPos-robot.xPos],[target.yPos-robot.yPos]]).reshape(2,1) #? Vector between the robot and the target
    pgVec=pgVec/sqrt(pgVec[0]**2+pgVec[1]**2) #? Normalizing pgVec
    #robot.face = 1
    if robot.face == 1:
        headVec=[cos(robot.theta), sin(robot.theta)]
        dotProd=headVec[0]*pgVec[0]+headVec[1]*pgVec[1]
        if dotProd >= -0.42:
            robot.face = 1
        else:
            robot.face = -1
            robot.theta = arctan2(sin(robot.theta + pi), cos(robot.theta + pi))
    else:
        robot.theta = arctan2(sin(robot.theta + pi), cos(robot.theta + pi))
        headVec=[cos(robot.theta), sin(robot.theta)]
        dotProd=headVec[0]*pgVec[0]+headVec[1]*pgVec[1]
        if dotProd >= -0.42:
            robot.face = -1
        else:
            robot.theta = arctan2(sin(robot.theta + pi), cos(robot.theta + pi))
            robot.face = 1
#'''

def changeTargetTheta(robot, corner):

    if robot.yPos > 75:
        if corner == 1:
            target.update(theta = 90)
        elif corner == 3
            target.update(theta = -90)
        else:
            target.update(theta = 0)
    else:
        if corner == 1:
            target.update(theta = -90)
        elif corner == 3
            target.update(theta = 90)        
        else:
            target.update(theta = 0)

    return None

def inCorner(target, robot):

    flagCorner = False
    if target.xPos < 7:
        flagCorner = True
        corner = 1
        if target.xPos < 3:
            target.update(xPos = target.xPos+3)
    elif target.xPos > 143:
        flagCorner = True
        corner = 3
        if target.xPos > 147:
            target.update(xPos = target.xPos-3)
    if target.yPos < 7:
        flagCorner = True
        corner = 2
        if target.yPos < 3:
            target.update(yPos = target.yPos+3)
    elif target.yPos > 123:
        flagCorner = True
        corner = 4   
        if target.yPos > 127:
            target.update(yPos = target.yPos-3)
    if flagCorner:
        changeTargetTheta(robot, corner)

    return flagCorner, corner
