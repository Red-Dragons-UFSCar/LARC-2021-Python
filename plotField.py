import matplotlib.pyplot as plt
import numpy as np
import threading
from threading import Timer
import time

import behaviours
from bridge import (Vision)
from simClasses import *
#from strategy import *

from vss_communication import StrategyControl

# IDs dos robôs em ordem 0, 1 e 2 na visão da cin
id_robots = [6, 10, 5]

class RepeatTimer(Timer):  
    def run(self):  
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)  
            print(' ')  

class PlotField:
    def __init__(self):
        self.figureOpen = False

    def plot_interactive(self, target, robot, obstacle=None):
        self.univec = behaviours.Univector()  # Objeto univector
        self.x_pos = range(1, 150, 5)  # Plot do campo inteiro
        self.y_pos = range(1, 150, 5)

        self.robo = robot

        self.x_plot = []
        self.y_plot = []
        self.V = []

        for i in self.x_pos:
            for j in self.y_pos:
                self.robo._coordinates.X = i  # Variação da posição do robô
                self.robo._coordinates.Y = j
                if obstacle is None:
                    self.theta = self.univec.hip_vec_field(self.robo, target)
                else:
                    # Calculo do angulo desejado pelo campo hiperbólico
                    self.theta = self.univec.univec_field_h(self.robo, target,
                                                            obstacle)

                self.theta.astype(np.float64)  # Adequações
                if type(self.theta) == type(np.array([])):
                    self.theta = self.theta[0]

                self.matrix = self.univec.rot_matrix(self.theta)  # Criando vetores unitarios com o angulo retornado
                self.vetPos = np.dot(self.matrix, np.array([[1], [0]]))
                self.V.append([list(self.vetPos[0])[0], list(self.vetPos[1])[0]])
                self.x_plot.append(i)
                self.y_plot.append(j)

        self.V = np.array(self.V)
        origin = np.array([self.x_plot, self.y_plot])

        if not self.figureOpen:
            plt.ion()
            plt.isinteractive()
            self.fig, ax = plt.subplots(1, 1)
            #self.Q = ax.quiver(*origin, self.V[:, 0], self.V[:, 1])
            self.Q = ax.quiver(self.x_plot, self.y_plot, self.V[:, 0], self.V[:, 1])
            self.figureOpen = True
            print("Abri")
        else:
            self.Q.set_UVC(self.V[:, 0], self.V[:, 1])

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        #plt.quiver(*origin, V[:,0], V[:,1])
        #plt.show(block=False)


if __name__ == '__main__':
    mray = True

    #vision = Vision(mray, "224.0.0.1", 10002)
    client_control = StrategyControl(ip='224.5.23.2', port=10015, yellowTeam=mray, logger=False, pattern='ssl', convert_coordinates=True)  # Criação do objeto do controle e estratégia

    teamYellow = mray

    robot0 = Robot(0, actuator=None, mray=mray)
    robot1 = Robot(1, actuator=None, mray=mray)
    robot2 = Robot(2, actuator=None, mray=mray)
    robots = [robot0, robot1, robot2]
    for robot in robots:
        #robot.set_enemies(enemy_robots)
        robot.set_friends(robots.copy())

    robotEnemy0 = Robot(0, actuator=None, mray=teamYellow)
    robotEnemy1 = Robot(1, actuator=None, mray=teamYellow)
    robotEnemy2 = Robot(2, actuator=None, mray=teamYellow)

    ball = Ball()

    #strategy = Strategy(robot0, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, ball, mray)

    plot = PlotField()

    data_our_bot = []
    data_their_bots = []
    data_ball = []

    def getData(ball, robots):
        client_control.update(mray)
        field = client_control.get_data_Red()

        data_our_bot = field[0]["our_bots"]  # Salva os dados dos robôs aliados
        data_their_bots = field[0]["their_bots"]  # Salva os dados dos robôs inimigos
        data_ball = field[0]["ball"]  # Salva os dados da bola

        data_our_bot2 = []
        for i in range(len(data_our_bot)):
            if data_our_bot[i]['robot_id'] > 2:
                data_our_bot2.append(data_our_bot[i])
        
        data_our_bot = data_our_bot2

        for i in range(len(data_our_bot)):  # Separação de dados recebidos da visão
            for index, robot in enumerate(robots):
                if data_our_bot[i]["robot_id"] == id_robots[index]:  # Se o id do robô recebido é igual ao robô desejado (Código Cin)
                    data_our_bot[i]["robot_id"] = id_robots.index(data_our_bot[i]["robot_id"])  # Adequação de ID dos robôs
                    data_our_bot[i]["orientation"] = np.arctan2(np.sin(data_our_bot[i]["orientation"] + np.pi), np.cos(data_our_bot[i]["orientation"] + np.pi))  # Adequação de orientação dos robôs
                    robot.set_simulator_data(data_our_bot[i])
                    break
        
        for i in range(len(data_ball)):
            ball.set_simulator_data(data_ball)

        print(data_ball['x'])
        #time.sleep(1/60)

    x = RepeatTimer((1/120), getData, args=(ball, robots))
    x.start()
    
    while True:
        # Atualiza os dados da visão
        #client_control.update(mray)
        #field = client_control.get_data_Red()

        #data_our_bot = field[0]["our_bots"]  # Salva os dados dos robôs aliados
        #data_their_bots = field[0]["their_bots"]  # Salva os dados dos robôs inimigos
        #data_ball = field[0]["ball"]  # Salva os dados da bola

        # Atualiza em cada objeto do campo os dados da visão
        #robot0.sim_get_pose(data_our_bot[0])
        #robot1.sim_get_pose(data_our_bot[1])
        #robot2.sim_get_pose(data_our_bot[2])
        #robotEnemy0.sim_get_pose(data_their_bots[0])
        #robotEnemy1.sim_get_pose(data_their_bots[1])
        #robotEnemy2.sim_get_pose(data_their_bots[2])
        #ball.sim_get_pose(data_ball)
        # data_our_bot2 = []
        # for i in range(len(data_our_bot)):
        #     if data_our_bot[i]['robot_id'] > 2:
        #         data_our_bot2.append(data_our_bot[i])
        
        # data_our_bot = data_our_bot2

        # for i in range(len(data_our_bot)):  # Separação de dados recebidos da visão
        #     for index, robot in enumerate(robots):
        #         if data_our_bot[i]["robot_id"] == id_robots[index]:  # Se o id do robô recebido é igual ao robô desejado (Código Cin)
        #             data_our_bot[i]["robot_id"] = id_robots.index(data_our_bot[i]["robot_id"])  # Adequação de ID dos robôs
        #             data_our_bot[i]["orientation"] = np.arctan2(np.sin(data_our_bot[i]["orientation"] + np.pi), np.cos(data_our_bot[i]["orientation"] + np.pi))  # Adequação de orientação dos robôs
        #             robot.set_simulator_data(data_our_bot[i])
        #             break
        
        # for i in range(len(data_ball)):
        #     ball.set_simulator_data(data_ball)

        # Shoot
        # if not mray:
        #    arrivalTheta=arctan2(65-ball.yPos,150-ball.xPos) #? Angle between the ball and point (150,65)
        # else:
        #    arrivalTheta=arctan2(65-ball.yPos,-ball.xPos) #? Angle between the ball and point (0,65)

        # Shoot 2
        '''
        if not mray:
            if (ball.yPos > 45) and (ball.yPos < 85):
                arrivalTheta = 0
            elif ball.yPos <= 45:
                y = 45 + (45 - ball.yPos) / (45 - 0) * 20
                arrivalTheta = arctan2(y - 45, 160 - ball.xPos)
            else:
                y = 85 - (ball.yPos - 85) / (130 - 85) * 20
                arrivalTheta = arctan2(y - 85, 160 - ball.xPos)
        else:
            if (ball.yPos > 45) and (ball.yPos < 85):
                arrivalTheta = pi
            elif ball.yPos <= 45:
                y = 45 + (45 - ball.yPos) / (45 - 0) * 20
                arrivalTheta = arctan2(y - 45, 10 - ball.xPos)
            else:
                y = 85 - (ball.yPos - 85) / (130 - 85) * 20
                arrivalTheta = arctan2(y - 85, 10 - ball.xPos)
        '''
        arrivalTheta=0

        print(ball._coordinates.Y)
        robots[2].target.set_coordinates(ball._coordinates.X, ball._coordinates.X, arrivalTheta)
        robots[2].obst.update()

        plot.plot_interactive(robots[2].target, robots[2], robots[2].obst)

