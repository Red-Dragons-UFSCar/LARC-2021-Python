from numpy import arctan2,pi,sqrt,cos,sin,array,matmul,amin,where,zeros,delete,append,int32, argmin

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
    def update(self,robot,obstacles):
        n = len(obstacles)
        dist = zeros(n)
        for i in range(n):
            dist[i] = robot.dist(obstacles[i])
        minima = min(dist)
        index = 0
        for i in range(n):
            if minima==dist[i]:
                index = i
        self.setObst(obstacles[index].xPos,obstacles[index].yPos,obstacles[index].v,obstacles[index].theta)

    def update2(self,robot,ball,friends,enemys):
        enemys = array(enemys)
        d_ball=array([[enemys[0].dist(ball)],
                      [enemys[1].dist(ball)],
                      [enemys[2].dist(ball)],
                      [enemys[3].dist(ball)],
                      [enemys[4].dist(ball)]])
        index=argmin(d_ball)
        if d_ball[index] < 15:
            enemys = delete(enemys, [index])

        if not robot.teamYellow:
            xGol = 235
            yGol = 90
        else:
            xGol = 15
            yGol = 90

        if len(enemys)==5:
            d1 = sqrt( (xGol-enemys[0].xPos)**2 + (yGol-enemys[0].yPos)**2 )
            d2 = sqrt( (xGol-enemys[1].xPos)**2 + (yGol-enemys[1].yPos)**2 )
            d3 = sqrt( (xGol-enemys[2].xPos)**2 + (yGol-enemys[2].yPos)**2 )
            d4 = sqrt( (xGol-enemys[3].xPos)**2 + (yGol-enemys[3].yPos)**2 )
            d5 = sqrt( (xGol-enemys[4].xPos)**2 + (yGol-enemys[4].yPos)**2 )
            d_gol=array([[d1],
                         [d2],
                         [d3],
                         [d4],
                         [d5]])
            index=argmin(d_gol)
            dballgol = sqrt( (xGol-ball.xPos)**2 + (yGol-ball.yPos)**2 )
            if d_gol[index] < 30 and dballgol < 30:
                enemys = delete(enemys, index)
        else:
            d1 = sqrt( (xGol-enemys[0].xPos)**2 + (yGol-enemys[0].yPos)**2 )
            d2 = sqrt( (xGol-enemys[1].xPos)**2 + (yGol-enemys[1].yPos)**2 )
            d3 = sqrt( (xGol-enemys[2].xPos)**2 + (yGol-enemys[2].yPos)**2 )
            d4 = sqrt( (xGol-enemys[3].xPos)**2 + (yGol-enemys[3].yPos)**2 )
            d_gol=array([[d1],
                         [d2],
                         [d3],
                         [d4]])
            index=argmin(d_gol)
            dballgol = sqrt( (xGol-ball.xPos)**2 + (yGol-ball.yPos)**2 )
            if d_gol[index] < 30 and dballgol < 30:
                enemys = delete(enemys, index)

        enemys = append(enemys, friends[0])
        enemys = append(enemys, friends[1])
        enemys = append(enemys, friends[2])
        enemys = append(enemys, friends[3])

        d_robot = zeros(len(enemys))
        # for i in range(len(enemys)):
        #     print("Index: ", enemys[i].index)
        for i in range(len(enemys)):
           d_robot[i] = robot.dist(enemys[i])

        index=argmin(d_robot)
        self.setObst(enemys[index].xPos,enemys[index].yPos,0,0)
        # if robot.index == 4:
        #     if enemys[index].teamYellow:
        #         print("Obstaculo: Amarelo " + str(enemys[index].index))
        #     else:
        #         print("Obstaculo: Azul " + str(enemys[index].index))
        # self.setObst(enemys[index].xPos,enemys[index].yPos,0,0)

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
