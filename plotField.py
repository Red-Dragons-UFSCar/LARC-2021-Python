import numpy as np
import matplotlib.pyplot as plt

import behaviours
from bridge import (Actuator, Replacer, Vision, Referee,
                        NUM_BOTS, convert_angle, Entity)
from simClasses import *
import action
import fouls

from strategy import *

class PlotField:
    def __init__(self):
        self.figureOpen = False

    def plotInteractive(self, target, obstacle = None):
        self.univec = behaviours.Univector()                                                 # Objeto univector
        self.x_pos = range(1, 150, 5)                                                        # Plot do campo inteiro
        self.y_pos = range(1, 150, 5)

        self.robo = Robot(0, "nada")

        self.x_plot = []
        self.y_plot = []
        self.V = []

        for i in self.x_pos:
            for j in self.y_pos:
                self.robo.xPos = i                                                           # Variação da posição do robô
                self.robo.yPos = j
                if obstacle == None:
                    self.theta = self.univec.hipVecField(self.robo, target)
                else:
                    self.theta = self.univec.univecField_H(self.robo, target, obstacle)              # Calculo do angulo desejado pelo campo hiperbólico

                self.theta.astype(np.float64)                                                # Adequações
                if type(self.theta) == type(np.array([])):
                    self.theta = self.theta[0]

                self.matrix = self.univec.rotMatrix(self.theta)                                        # Criando vetores unitarios com o angulo retornado
                self.vetPos = np.dot(self.matrix,np.array([[1], [0]]))
                self.V.append([list(self.vetPos[0])[0], list(self.vetPos[1])[0]])
                self.x_plot.append(i)
                self.y_plot.append(j)

        self.V = np.array(self.V)
        origin = np.array([self.x_plot,self.y_plot])

        if not self.figureOpen:
            plt.ion()
            self.fig, ax = plt.subplots(1,1)
            self.Q = ax.quiver(*origin, self.V[:,0], self.V[:,1])
            self.figureOpen = True
        else:
            self.Q.set_UVC(self.V[:,0], self.V[:,1])

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        #plt.quiver(*origin, V[:,0], V[:,1])
        #plt.show(block=True)

if __name__ == '__main__':
    mray = False

    vision = Vision(mray, "224.0.0.1", 10002)

    robot0 = Robot(0, actuator=None)
    robot1 = Robot(1, actuator=None)
    robot2 = Robot(2, actuator=None)

    robotEnemy0 = Robot(0, actuator=None)
    robotEnemy1 = Robot(1, actuator=None)
    robotEnemy2 = Robot(2, actuator=None)

    ball = Ball()

    strategy = Strategy(robot0, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, ball, mray)

    plot = PlotField()

    while True:
        # Atualiza os dados da visão
        vision.update()
        field = vision.get_field_data()

        data_our_bot = field["our_bots"]        #Salva os dados dos robôs aliados
        data_their_bots = field["their_bots"]   #Salva os dados dos robôs inimigos
        data_ball = field["ball"]               #Salva os dados da bola

        # Atualiza em cada objeto do campo os dados da visão
        robot0.simGetPose(data_our_bot[0])
        robot1.simGetPose(data_our_bot[1])
        robot2.simGetPose(data_our_bot[2])
        robotEnemy0.simGetPose(data_their_bots[0])
        robotEnemy1.simGetPose(data_their_bots[1])
        robotEnemy2.simGetPose(data_their_bots[2])
        ball.simGetPose(data_ball)

        if not mray:
            arrivalTheta=arctan2(65-ball.yPos,150-ball.xPos) #? Angle between the ball and point (150,65)
        else:
            arrivalTheta=arctan2(65-ball.yPos,-ball.xPos) #? Angle between the ball and point (0,65)

        robot2.target.update(ball.xPos,ball.yPos,arrivalTheta)
        robot2.obst.update(robot2,robot0,robot1,robotEnemy0,robotEnemy1,robotEnemy2)

        plot.plotInteractive(robot2.target, robot2.obst)
