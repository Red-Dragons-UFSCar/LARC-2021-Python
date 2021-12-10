from numpy import cos,sin,arctan2,sqrt,sign,pi,delete,append,array,angle, deg2rad
from behaviours import Univector
from corners import targetInCorner, robotLockedCorner

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
def univecController(robot,target,avoidObst=True,obst=None,n=8,d=2,stopWhenArrive=False, doubleFace=True, fieldIsHiperbolic=True):
    flagCorner, corner= targetInCorner(target,robot)
    #if flagCorner:
        #robotLockedCorner(target, robot)
    navigate=Univector() #? Defines the navigation algorithm
    dl=0.000001          #? Constant to approximate phi_v
    k_w=1.8                #? Feedback constant (k_w=1 means no gain)
    k_p=1                #? Feedback constant (k_p=1 means no gain)

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

    if stopWhenArrive and robot.arrive():
        v = 0
        w = 0
    else:
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
