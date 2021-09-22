from numpy import arctan2,pi,sqrt,cos,sin,array,matmul,amin,where,take,zeros,delete,append,int32,argmin
from scipy.spatial import distance

#! Units: cm, rad, s

#% Class to set the targets of each robot in game
class Target:
    def __init__(self):
        self.xPos=0         #? Desired x position
        self.yPos=0         #? Desired y position
        self.theta=0        #? Orientation at the desired point (x,y)

    #% Setter
    def update(self,x,y,theta):
        self.xPos=x
        self.yPos=y
        self.theta=theta

    #% This method print a little log on console
    def showInfo(self):
        print('xPos: {:.2f} | yPos: {:.2f} | theta: {:.2f}'.format(self.xPos,self.yPos,float(self.theta)))

#% Class to set the obstacle of each robot
class Obstacle:
    def __init__(self):
        self.xPos=0         #? Obstacle x position
        self.yPos=0         #? Obstacle y position
        self.v=0            #? Obstacle velocity (cm/s)
        self.theta=0        #? Obstacle orientation

    #% Setter
    def setObst(self,x,y,v,theta):
        self.xPos=x
        self.yPos=y
        self.v=v
        self.theta=theta

    #% This method verify which is the closest obstacle and sets it as the current obstacle to avoid
    def update(self,robot,friend1,friend2,enemy1=None,enemy2=None,enemy3=None):
        if (enemy1 is None) and (enemy2 is None) and (enemy3 is None):
            d=array([[robot.dist(friend1)],
                     [robot.dist(friend2)]])
        elif (enemy2 is None) and (enemy3 is None):
            d=array([[robot.dist(friend1)],
                     [robot.dist(friend2)],
                     [robot.dist(enemy1) ]])
        elif (enemy3 is None):
            d=array([[robot.dist(friend1)],
                     [robot.dist(friend2)],
                     [robot.dist(enemy1) ],
                     [robot.dist(enemy2) ]])
        else:
            d=array([[robot.dist(friend1)],
                     [robot.dist(friend2)],
                     [robot.dist(enemy1) ],
                     [robot.dist(enemy2) ],
                     [robot.dist(enemy3) ]])

        index=where(d==amin(d))
        if index[0][0]==0:
            self.setObst(friend1.xPos,friend1.yPos,friend1.v,friend1.theta)
        elif index[0][0]==1:
            self.setObst(friend2.xPos,friend2.yPos,friend2.v,friend2.theta)
        elif index[0][0]==2:
            self.setObst(enemy1.xPos,enemy1.yPos,0,0)
        elif index[0][0]==3:
            self.setObst(enemy2.xPos,enemy2.yPos,0,0)
        else:
            self.setObst(enemy3.xPos,enemy3.yPos,0,0)

    #% This method print a little log on console
    def showInfo(self):
        print('xPos: {:.2f} | yPos: {:.2f} | theta: {:.2f} | velocity: {:.2f}'.format(self.xPos,self.yPos,float(self.theta),self.v))

#% Class to create the ball in game
class Ball:
    def __init__(self):
        self.xPos=0
        self.yPos=0
        self.vx=0
        self.vy=0
        self.pastPose=zeros(4).reshape(2,2) #? Stores the last 3 positions (x,y) => updated on self.simGetPose()

    #% This method gets position of the ball in FIRASim
    def simGetPose(self, data_ball):
        self.xPos = data_ball.x
        self.yPos = data_ball.y
        self.vx = data_ball.vx
        self.vy = data_ball.vy


    #% This method print a little log on console
    def showInfo(self):
        print('xPos: {:.2f} | yPos: {:.2f}'.format(self.xPos,self.yPos))

#% Class to create the robots in game
class Robot:
    def __init__(self, index, actuator, mray):
        self.flagDirectGoal=False
        self.flagCruzamento=False
        self.flagTrocaFace=False
        self.teamYellow=mray
        self.index=int32(index)
        self.actuator=actuator
        self.face=1                          #? Defines the current face of the robot
        self.xPos=0                          #? X position
        self.yPos=0                          #? Y position
        self.theta=0                         #? Orientation
        self.rightMotor=0                    #? Right motor handle
        self.leftMotor=0                     #? Left motor handle
        self.v=0                             #? Velocity (cm/s) => updated on execution.py
        self.vx=0
        self.vy=0
        self.vTheta=0
        self.vL=0                            #? Left wheel velocity (cm/s) => updated on simClasses.py -> simSetVel()
        self.vR=0                            #? Right wheel velocity (cm/s) =>  updated on simClasses.py -> simSetVel()
        self.vMax=35                             #! Robot max velocity (cm/s)
        self.rMax=3*self.vMax                #! Robot max rotation velocity (rad*cm/s)
        self.L=7.5                           #? Base length of the robot (cm)
        self.LSimulador=6.11                 #? Base length of the robot on coppelia (cm)
        self.R=3.4                           #? Wheel radius (cm)
        self.obst=Obstacle()                 #? Defines the robot obstacle
        self.target=Target()                 #? Defines the robot target
        self.pastPose=zeros(12).reshape(4,3) #? Stores the last 3 positions (x,y) and orientation => updated on execution.py



    #% This method calculates the distance between the robot and an object
    def dist(self,obj):
        return sqrt((self.xPos-obj.xPos)**2+(self.yPos-obj.yPos)**2)

    #% This method returns True if the distance between the target and the robot is less than 5cm - False otherwise
    def arrive(self):
        if self.dist(self.target)<=5:
            return True
        else:
            return False

    #% This method gets both position and orientation of the robot in FIRASim
    def simGetPose(self, data_robot):
        self.xPos = data_robot.x
        self.yPos = data_robot.y
        self.vx = data_robot.vx
        self.vy = data_robot.vy
        self.theta = data_robot.a
        self.vTheta = data_robot.va

    def simSetVel(self,v,w):
        if self.face==1:
            self.vR=v+0.5*self.L*w
            self.vL=v-0.5*self.L*w
        else:
            self.vL=-v-0.5*self.L*w
            self.vR=-v+0.5*self.L*w
        self.actuator.send(self.index, self.vL, self.vR)

    #% This method print a little log on console
    def showInfo(self):
        print('xPos: {:.2f} | yPos: {:.2f} | theta: {:.2f} | velocity: {:.2f}'.format(self.xPos,self.yPos,float(self.theta),float(self.v)))

class Grid:
    def __init__(self):
        
        # criando um grid 5x6
        self.gridv = array([[17.5, 13],[42.5, 13], [67.5, 13],[92.5, 13], [117.5, 13],[142.5, 13],
                      [17.5, 39],[42.5, 39], [67.5, 39],[92.5, 39], [117.5, 39],[142.5, 39]
                      [17.5, 65],[42.5, 65], [67.5, 65],[92.5, 65], [117.5, 65],[142.5, 65]
                      [17.5, 91],[42.5, 91], [67.5, 91],[92.5, 91], [117.5, 91],[142.5, 91]
                      [17.5, 117],[42.5, 117], [67.5, 117],[92.5, 117], [117.5, 117],[142.5, 117] ])
        
        # definindo os angulos de cada grid
        self.AttitudeGrid = array([-pi/2, 0.47282204, 0.56910571, 0.70991061, 0.9279823, 1.27818735,
                             -pi/2, 0.29463669, 0.35945951, 0.46006287, 0.63557154, 1.0038244,
                             0.06148337, 0.07225452, 0.08759046, 0.11115443, 0.15188589, 0.23793116,
                             pi/2, -0.29463669, -0.35945951, -0.46006287, -0.63557154, -1.0038244,
                             pi/2,  -0.47282204, -0.56910571, -0.70991061, -0.9279823, -1.27818735])
        self.robotGridPos = zeros(3)
        self.ballGridPos = 0

    def update(self, robot0, robot1, robot2, ball):
        
        # encontrando o indice em que cada robo e a bola se encontra
        index0 = argmin(distance.cdist(self.gridv, [robot0.xPos, robot0.yPos], 'euclidian'))
        index1 = argmin(distance.cdist(self.gridv, [robot1.xPos, robot1.yPos], 'euclidian'))
        index2 = argmin(distance.cdist(self.gridv, [robot2.xPos, robot2.yPos], 'euclidian'))
        indexb = argmin(distance.cdist(self.gridv, [ball.xPos, ball.yPos], 'euclidian'))

        # Atualizando os valores
        self.robotGridPos = array([index0, index1, index2])
        self.ballGridPos = indexb

    def bestGridMov():

        # Posição dos robôs
        pos0 = self.gridv[index[0]]
        pos1 = self.gridv[index[1]]
        pos2 = self.gridv[index[2]]

        # Lista dos grids mais próximos de cada robô 
        listAux0 = distance.cdist(self.gridv, self.gridv[pos0], 'euclidian') # calcula a distancia
        listId0 = where(list0Aux == list0Aux.min()) # encontra o indice dos valores min
        list0 = take(self.gridv, listId0) # salva a posição dos valores min
        
        listAux1 = distance.cdist(self.gridv, self.gridv[pos1], 'euclidian')
        listId1 = where(listAux1 == listAux1.min())
        list1 = take(self.gridv, listId1)
        
        listAux2 = distance.cdist(self.gridv, self.gridv[pos2], 'euclidian')
        listId2 = where(listAux2 == listAux2.min())
        list2 = take(self.gridv, listId2)

        #Verifica se a posição que ele vai se mover já tem algum robô
        
        if self.robotGridPos[1] in listId0:
            listId0 = delete(listId0, where(listId0 == self.robotGridPos[1]))
            list0 = delete(list0, where(listId0 == self.robotGridPos[1]))
        if self.robotGridPos[2] in listId0:
            listId0 = delete(listId0, where(listId0 == self.robotGridPos[2]))
            list0 = delete(list0, where(listId0 == self.robotGridPos[2]))
       
        if self.robotGridPos[0] in listId1:
            listId1 = delete(listId1, where(listId1 == self.robotGridPos[0]))
            list1 = delete(list1, where(listId1 == self.robotGridPos[0]))
        if self.robotGridPos[2] in listId1:
            listId1 = delete(listId1, where(listId1 == self.robotGridPos[2]))
            list1 = delete(list1, where(listId1 == self.robotGridPos[2]))

        if self.robotGridPos[0] in listId2:
            listId2 = delete(listId2, where(listId2 == self.robotGridPos[0]))
            list2 = delete(list2, where(listId2 == self.robotGridPos[0]))
        if self.robotGridPos[1] in listId2:
            listId2 = delete(listId2, where(listId2 == self.robotGridPos[1]))
            list2 = delete(list2, where(listId2 == self.robotGridPos[1]))

        # Encontrando qual grid é o mais próximo da bola
        targetId0 = argmin(distance.cdist(list0, self.gridv[indexb], 'euclidian'))
        target0 = self.gridv[listId0[targetId0]]

        targetId1 = argmin(distance.cdist(list1, self.gridv[indexb], 'euclidian'))
        target1 = self.gridv[listId0[targetId1]]

        targetId2 = argmin(distance.cdist(list2, self.gridv[indexb], 'euclidian'))
        target2 = self.gridv[listId0[targetId2]]