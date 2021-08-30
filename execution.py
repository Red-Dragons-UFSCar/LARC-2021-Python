from numpy import cos,sin,arctan2,sqrt,sign,pi,delete,append,array,angle
from behaviours import Univector

#% Function to approximate phi_v
def approx(robot,target,avoidObst=True,obst=None,n=8,d=2, fieldIsHiperbolic=True):
    navigate=Univector()                #? Defines the navigation algorithm
    dl=0.000001                         #? Constant to approximate phi_v

    x=robot.xPos                                            #? Saving (x,y) coordinates to calculate phi_v
    y=robot.yPos
    robot.xPos=robot.xPos+dl*cos(robot.theta)               #? Incrementing robot (x,y) position
    robot.yPos=robot.yPos+dl*sin(robot.theta)

    if avoidObst:
        if fieldIsHiperbolic:
            stpTheta=navigate.univecField_H(robot,target,obst)                  #? Computing a step Theta to determine phi_v
        else:
            stpTheta=navigate.univecField_N(robot,target,obst,n,d)              #? Computing a step Theta to determine phi_v
    else:
        if fieldIsHiperbolic:
            stpTheta=navigate.hipVecField(robot,target)                         #? Computing a step Theta to determine phi_v
        else:
            stpTheta=navigate.nVecField(robot,target,n,d,haveFace=False)        #? Computing a step Theta to determine phi_v

    robot.xPos=x                        #? Returning original (x,y) coordinates
    robot.yPos=y

    return stpTheta

#% Function to control the robot with or without collision avoidance
def univecController(robot,target,avoidObst=True,obst=None,n=8,d=2,stopWhenArrive=False, doubleFace=True):
    flagCorner, corner= targetInCorner(target,robot)
    if flagCorner:
        robotLockedCorner(target, robot)
    navigate=Univector() #? Defines the navigation algorithm
    dl=0.000001          #? Constant to approximate phi_v
    k_w=1.9                #? Feedback constant (k_w=1 means no gain)
    k_p=1                #? Feedback constant (k_p=1 means no gain)
    robot_aux = deepcopy(robot)

    #% Correção de ângulo caso o robô esteja jogando com a face de trás
    if robot.face == -1:
        robot.theta = arctan2(sin(robot.theta - pi),cos(robot.theta - pi))

    #% Navigation: Go-to-Goal + Avoid Obstacle Vector Field
    if avoidObst:
        if fieldIsHiperbolic:
            desTheta=navigate.univecField_H(robot,target,obst)                  #? Desired angle w/ gtg and ao vector field
        else:
            desTheta=navigate.univecField_N(robot,target,obst,n,d)              #? Desired angle w/ gtg and ao vector field

    #% Navigation: Go-to-Goal Vector Field
    else:
        if fieldIsHiperbolic:
            desTheta=navigate.hipVecField(robot,target)                         #? Desired angle w/ gtg
        else:
            desTheta=navigate.nVecField(robot,target,n,d, haveFace=False)       #? Desired angle w/ gtg

    stpTheta=approx(robot,target,avoidObst,obst,n,d,fieldIsHiperbolic)
    phi_v=arctan2(sin(stpTheta-desTheta),cos(stpTheta-desTheta))/dl             #? Trick to mantain phi_v between [-pi,pi]
    theta_e = whichFace(robot, target, desTheta, doubleFace)
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
    robot.pastPose=delete(robot.pastPose,0,1)                                   #? Deleting the first column
    robot.pastPose=append(robot.pastPose,array([[round(robot.xPos)],[round(robot.yPos)],[round(float(robot.theta))],[round(float(v))]]),1)

    return v,w

#'''
# TODO #3 Verificar a necessidade de flagTrocaFace - travar a troca de face nos obstaculos
def whichFace(robot, target, desTheta, doubleFace):
    theta_e = arctan2(sin(desTheta-robot.theta),cos(desTheta-robot.theta))      # Calculo do erro com a face atual

    if (abs(theta_e) > pi/2 + pi/12) and (not robot.flagTrocaFace) and doubleFace:  # Se o ângulo for propício pra trocar a face
        robot.face = robot.face * (-1)                                          # Inverte a face
        robot.theta = arctan2(sin(robot.theta + pi), cos(robot.theta + pi))     # Recalcula o angulo
        theta_e = arctan2(sin(desTheta-robot.theta),cos(desTheta-robot.theta))  # Recalcula o erro

    return theta_e
#'''
# Estas funções são utilizadas para alterar a execução das estratégias do jogador nos cantos
# Afim de impedir que ele fique travado

def targetInCorner(target, robot):

    corner = 0
    flagCorner = False
    if target.xPos < 20:

        flagCorner = True
        corner = 1
        if target.xPos < 5:
            target.update(target.xPos+3, target.yPos, target.theta)
        else:
            target.update(target.xPos+1.5, target.yPos, target.theta)
    elif target.xPos > 140:

        flagCorner = True
        corner = 3
        if target.xPos > 145:
            target.update(target.xPos-3, target.yPos, target.theta)
        else:
            target.update(target.xPos-1.5, target.yPos, target.theta)
    if target.yPos < 10:

        flagCorner = True
        corner = 2
        if target.yPos < 5:
            target.update(target.xPos,target.yPos+3, target.theta)
        else:
            target.update(target.xPos,target.yPos+1.5, target.theta)
    elif target.yPos > 120:

        flagCorner = True
        corner = 4
        if target.yPos > 125:
            target.update(target.xPos,target.yPos-3, target.theta)
        else:
            target.update(target.xPos,target.yPos-1.5, target.theta)

    if flagCorner:
        changeTargetTheta(robot, target,corner)

    return flagCorner, corner

def changeTargetTheta(robot, target,corner):

    dist = sqrt((robot.xPos- target.xPos)**2 + (robot.yPos- target.yPos)**2)

    if (corner == 2 or corner == 4):
        if dist < 6:
            if robot.yPos < 75:
                thetaGol = angle([150- robot.xPos],75)

            else:
                thetaGol = angle([150- robot.xPos],-75)
            target.update(target.xPos,target.yPos,thetaGol)
        else:
            target.update(target.xPos,target.yPos,0)

    elif robot.yPos > 110:
        if corner == 1:
            target.update(target.xPos,target.yPos,pi/2)
        elif corner == 3:
            target.update(target.xPos,target.yPos,-pi/2)
    elif robot.yPos < 40:
        if corner == 1:
            target.update(target.xPos,target.yPos,-pi/2)
        elif corner == 3:
            target.update(target.xPos,target.yPos,pi/2)

    return None

def robotLockedCorner(target, robot):

    corner = 0
    flagLocked = False
    if (robot.xPos < 3 and (robot.yPos > 110 or robot.yPos < 40)):
        if (abs(robot.theta) < 0.35 or abs(robot.theta - pi) < 0.35):
            flagLocked = True
            corner = 1
    elif (robot.xPos > 147 and (robot.yPos > 110 or robot.yPos < 40)):
        if (abs(robot.theta) < 0.35 or abs(robot.theta - pi) < 0.35):
            flagLocked = True
            corner = 3
    if robot.yPos < 5:
        if ((abs(robot.theta) < ((pi/2)+0.35)) and (abs(robot.theta) > ((pi/2)-0.35))):
            flagLocked = True
            corner = 2
    elif robot.yPos > 125:
        if ((abs(robot.theta) < ((pi/2)+0.35)) and (abs(robot.theta) < ((pi/2)-0.35))):
            flagLocked = True
            corner = 4

    if flagLocked:
        changeTargetPos(robot, target,corner)

    return flagLocked, corner

def changeTargetPos(robot, target,corner):

    if corner == 1:
        target.update(robot.xPos+10,robot.yPos,0)
    if corner == 2:
        target.update(robot.xPos,robot.yPos+10,pi/2)
    if corner == 3:
        target.update(robot.xPos-10,robot.yPos,0)
    if corner == 4:
        target.update(robot.xPos,robot.yPos-10,-pi/2)
    return None
