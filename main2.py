from replace_protobuf import replacer_all
from ag import GA
from copy import deepcopy

#import fouls
from bridge import (Actuator, Replacer, Vision, Referee)
from simClasses import *
from strategy import *
from execution import univec_controller

import csv
import time

import numpy as np

def Go_To_Goal(robot, ball, ind):
    v, w = univec_controller(robot, robot.target, ind,avoid_obst=True,obst= robot.obst, double_face=False)
    robot.sim_set_vel(v, w)

if __name__ == "__main__":

    mray = False

    # Initialize all clients
    actuator = Actuator(mray, "127.0.0.1", 20011)
    replacement = Replacer(mray, "224.5.23.2", 10004)
    vision = Vision(mray, "224.0.0.1", 10002)
    referee = Referee(mray, "224.5.23.2", 10003)

    # Initialize all  objects
    robot0 = Robot(0, actuator, mray)
    robot1 = Robot(1, actuator, mray)
    robot2 = Robot(2, actuator, mray)

    robotEnemy0 = Robot(0, actuator, not mray)
    robotEnemy1 = Robot(1, actuator, not mray)
    robotEnemy2 = Robot(2, actuator, not mray)

    ball = Ball()
    
    # Genetic alg var
    nvar = 5
    varmin = 0
    varmax = 10
    maxit = 1000
    npop = 4

    flagTime = False
    flagColision = False

    # Initialize genetic alg    
    ga_univector = GA(nvar,varmin,varmax,maxit,npop)
    ga_univector.initialize_pop()

    # Set position list
    pos_x_0   = [15,15]
    pos_y_0   = [65,65]
    pos_ang_0 = [0,0]

    pos_x_1   = [50,70]
    pos_y_1   = [60,60]
    pos_ang_1 = [0,0]

    pos_x_2   = [122.5,105]
    pos_y_2   = [70,70]
    pos_ang_2 = [0,0]

    pos_x_ball = [140,125]
    pos_y_ball = [65,65]

    # timer
    start_time = 0
    finish_time = 0
    start_enviroment = True

    # Main infinite loop
    while True:
        t1 = time.time()

        if start_enviroment:
            print('Teleport position ', ga_univector.position)
            time.sleep(2)
            print(ga_univector.position)
            replacer_all([pos_x_0[ga_univector.position], pos_x_1[ga_univector.position], pos_x_2[ga_univector.position]],[pos_y_0[ga_univector.position], pos_y_1[ga_univector.position], pos_y_2[ga_univector.position]], [0, 0, 0], [1000, 1000, 1000], [350, 400, 450], [0, 0, 0], pos_x_ball[ga_univector.position], pos_y_ball[ga_univector.position])
            time.sleep(1)
            robot0.target.update(ball.xPos, ball.yPos, theta = 0)
            start_time = time.time()
            start_enviroment = False
            ga_univector.position = ga_univector.position + 1

        # Update the foul status
        referee.update()
        ref_data = referee.get_data()

        # Update the vision data
        vision.update()
        field = vision.get_field_data()

        data_our_bot = field["our_bots"]  # Save data from allied robots
        data_their_bots = field["their_bots"]  # Save data from enemy robots
        data_ball = field["ball"]  # Save the ball data

        # Updates vision data on each field object
        robot0.sim_get_pose(data_our_bot[0])
        robot1.sim_get_pose(data_our_bot[1])
        robot2.sim_get_pose(data_our_bot[2])
        robotEnemy0.sim_get_pose(data_their_bots[0])
        robotEnemy1.sim_get_pose(data_their_bots[1])
        robotEnemy2.sim_get_pose(data_their_bots[2])
        ball.sim_get_pose(data_ball)
        robot0.target.update(ball.xPos, ball.yPos, 0)
        robot0.obst.update(robot0, robot1, robot2)
	
        # check if robot achive the goal
        if robot0.arrive() or flagTime:
            if flagTime or flagColision:
                dt = 500
            else:
                dt = time.time() - start_time

            robot0.sim_set_vel(0, 0)
            print(dt)

            # Informações do individuo
            dy = robot0.yPos - ball.yPos
            dang = robot0.theta

            ga_univector.update_cost_param(dy,dang,dt,flagTime)

            flagTime = False
            flagColision = False
            start_enviroment = True

            # Reposicionamento para a próxima posição de treinamento
            if ga_univector.position == len(pos_x_0):
                # Todas as posições de treinamento foram concluidas para o individuo
                print('#### TERMINOU INDIVIDUO', ga_univector.individual ,'####')
                ga_univector.individual += 1 # -> Virar atributo da classe

                time.sleep(2)

                ga_univector.position = 0

                # Atualiza a função de fitness do individuo -> Passar
                ga_univector.cost_func(ga_univector.vec_dt, ga_univector.vec_dang, ga_univector.vec_dy)

                flagTime = False

                # Seleção dos individuos - Rever a seleção para algum padrão
                if ga_univector.individual == ga_univector.npop:

                    ga_univector.selection()

                    ga_univector.writeData()
            
            start_time = time.time()

        # Função de controle do robô
        # Talvez mudar essa ordem do if-else por que o else pula para a próxima geração
        elif ga_univector.individual < ga_univector.npop:
            Go_To_Goal(robot0, ball, ga_univector.pop[ga_univector.individual])
            if robot0.dist(robot1) < 7 or robot0.dist(robot2) < 7: # Rever essa distância de colisão
                flagColision = True
            if time.time() - start_time > 10:
                print('--- tempo estourou! ---')
                flagTime = True
                start_time = time.time()   
        else:
            print('Next Gen')
            ga_univector.nextGen()
            flagTime = False
            start_enviroment = True
        
        # synchronize code execution based on runtime and the camera FPS
        t2 = time.time()
        if t2 - t1 < 1 / 60:
            time.sleep(1 / 60 - (t2 - t1))
