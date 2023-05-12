from replace_protobuf import replacer_all
from ag import GA

#import fouls
from bridge import (Actuator, Replacer, Vision, Referee)
from simClasses import *
from strategy import *
from execution import univec_controller

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
    varmin = 0.1
    varmax = 10
    maxit = 1000
    npop = 100

    flagTime = False
    flagColision = False

    # Initialize genetic alg    
    ga_univector = GA(nvar,varmin,varmax,maxit,npop)
    ga_univector.initialize_pop()

    # Cenário 0
    # pos_x_0   = [15,15]
    # pos_y_0   = [65,65]
    # pos_ang_0 = [0,0]

    # pos_x_1   = [50,70]
    # pos_y_1   = [60,60]
    # pos_ang_1 = [0,0]

    # pos_x_2   = [122.5,105]
    # pos_y_2   = [70,70]
    # pos_ang_2 = [0,0]

    # pos_x_ball = [160,145] # Alvo
    # pos_y_ball = [65,65]


    # Cenário 1
    pos_x_0   = [27.5,85,142.5] # Robo treinado
    pos_y_0   = [105,65,25]
    pos_ang_0 = [-90,0,90]

    pos_x_1   = [105,105,105]
    pos_y_1   = [105,105,105]
    pos_ang_1 = [0,0,0]

    pos_x_2   = [122.5,122.5,122.5]
    pos_y_2   = [65,65,65]
    pos_ang_2 = [0,0,0]

    pos_x_0_e   = [160,160,160] # Robos do outro time
    pos_y_0_e   = [65,65,65]
    pos_ang_0_e = [0,0,0]

    pos_x_ball = [0,0,0]
    pos_y_ball = [0,0,0]

    target_x = [142.5,142.5,142.5]
    target_y = [105,105,105]
    target_angle = [-180,-180,-180]

    # timer
    start_time = 0
    finish_time = 0
    start_enviroment = True

    # Delay necessário para o teleporte dos robôs
    time_delay = 5/60

    # Tresholds
    timer_limit = 10
    distance_colision = 10 

    logInfo = True

    # Main infinite loop
    while True:
        t1 = time.time()
        
        # Criação de um novo ambiente para treinamento
        if start_enviroment:
            if logInfo: print('Teleport enviroment ', ga_univector.position)

            # Teleporte dos robôs - Timers necessários!
            time.sleep(time_delay)
            replacer_all([pos_x_0[ga_univector.position], pos_x_1[ga_univector.position], pos_x_2[ga_univector.position]],
                         [pos_y_0[ga_univector.position], pos_y_1[ga_univector.position], pos_y_2[ga_univector.position]], 
                         [pos_ang_0[ga_univector.position], pos_ang_1[ga_univector.position], pos_ang_2[ga_univector.position]], 
                         [pos_x_0_e[ga_univector.position], 1000, 1000], 
                         [pos_y_0_e[ga_univector.position], 400, 450], 
                         [pos_ang_0_e[ga_univector.position], 0, 0], 
                         pos_x_ball[ga_univector.position], 
                         pos_y_ball[ga_univector.position])
            robot0.target.update(target_x[ga_univector.position], target_y[ga_univector.position], target_angle[ga_univector.position])
            time.sleep(time_delay)

            # Início do tempo de amostragem do cenário
            start_time = time.time()

            # Atualização de variáveis
            ga_univector.position = ga_univector.position + 1
            start_enviroment = False

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

        # Definição da bola como alvo
        robot0.obst.update(robot0, robot1, robot2, robotEnemy0,robotEnemy1,robotEnemy2) # Definir melhor os obstáculos
	
        # check if robot achive the goal or any foul has occured
        if robot0.arrive() or flagTime or flagColision:
            # Stop the robot
            robot0.sim_set_vel(0, 0)

            #if flagTime or flagColision:
            #    dt = 500    # Penalty in cost function (review in future)
            #else:
            #    dt = time.time() - start_time
            dt = time.time() - start_time

            # Informações do individuo
            dy = robot0.yPos - target_y[ga_univector.position-1]
            dang = np.arctan2(np.sin(robot0.theta-target_angle[ga_univector.position-1]*np.pi/180), 
                              np.cos(robot0.theta-target_angle[ga_univector.position-1]*np.pi/180))

            # Atualiza as variáveis de fitness
            ga_univector.update_cost_param(dy,dang,dt)

            # Próximo cenário é disponibilizado
            start_enviroment = True

            # Verificação se os cenários acabaram - Individuo concluido
            if ga_univector.position == len(pos_x_0):

                # Atualiza a função de fitness do individuo
                ga_univector.cost_func(ga_univector.vec_dt, ga_univector.vec_dang, ga_univector.vec_dy, flagTime, flagColision)

                if logInfo:
                    print("Generation " + str(ga_univector.generation+1) +  ", Individual " + str(ga_univector.individual+1) + " finished!")
                    print("Parameters: ", ga_univector.pop[ga_univector.individual])
                    print("Fitness value: ", ga_univector.cost)
                    print("-----")

                ga_univector.individual += 1 
                ga_univector.position = 0

                # Processo genético do algoritmo
                if ga_univector.individual == ga_univector.npop:

                    ga_univector.nextGen()

                    if logInfo: 

                        print("\n-----GENERATION END-----")
                        print("General infos:")
                        print("Fitness Average: ", sum(ga_univector.vec_cost)/ga_univector.npop)
                        print("Better fitness: ", ga_univector.cost_better)
                        print("Better parameters: ", ga_univector.pop[ga_univector.index_better])
                        print("-----")
                        
                        print("\n-------------------- NEXT GENERATION --------------------\n")
                    
                    ga_univector.resetInfos()

                # Reseta as variaveis de controle de punições
                flagTime = False
                flagColision = False

            start_time = time.time()

        # Função de controle do robô
        else:
            Go_To_Goal(robot0, ball, ga_univector.pop[ga_univector.individual])

            # Verificação de colisão
            if robot0.dist(robot1) < distance_colision or robot0.dist(robot2) < distance_colision or robot0.dist(robotEnemy0) < distance_colision:
                flagColision = True

                if logInfo: print("[WARNING] - Colision!")

            # Verificação de tempo decorrido
            if time.time() - start_time > timer_limit:
                flagTime = True

                if logInfo: print('[WARNING] - Timeout!')
        
        # synchronize code execution based on runtime and the camera FPS
        t2 = time.time()
        if t2 - t1 < 1 / 60:
            time.sleep(1 / 60 - (t2 - t1))