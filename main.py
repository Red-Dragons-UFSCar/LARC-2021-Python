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

    arrival_theta = 0
    robot.target.update(ball.xPos, ball.yPos, arrival_theta)
    v, w = univec_controller(robot, robot.target, ind,avoid_obst=False, double_face=False)
    #print('V linear: ', v)
    #print('V ang: ', w)
    robot.sim_set_vel(v, w)
    #print('-----------------------')

if __name__ == "__main__":

    mray = True

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
    maxit = 200
    npop = 20

    # Aux var
    cont_gen = 0
    cont_pos = 1
    cont_ind = 0
    vec_dt = []
    vec_dy = []
    vec_dang = []
    vec_flagsTime = []
    flagTime = False

    # Initialize genetic alg    
    ga_univector = GA(nvar,varmin,varmax,maxit,npop)
    ga_univector.initialize_pop()

    # Set position list
    pos_x = [15,47.5,85,122.5,155,122.5,85,47.5]
    pos_y = [65,115,120,115,65,25,20,25]
    pos_ang = [0,0,180,180,180,180,180,0]

    # timer
    start_time = 0
    finish_time = 0
    first_time = True

    # data var

    header = ['Generation','d_e', 'k_r','delta','k_o','d_min','Cost','index_dt','dt','index_dy','dy','index_dang','dang']
    data_csv = []

    # Main infinite loop
    while True:
        t1 = time.time()

        if first_time:
            replacer_all([pos_x[0], 1000, 1000],[pos_y[0], 250, 300], [0, 0, 0], [1000, 1000, 1000], [350, 400, 450], [0, 0, 0], 85, 65)
            robot0.target.update(ball.xPos, ball.yPos, theta = 0)
            start_time = time.time()
            first_time = False

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

        # check if robot achive the goal
        if robot0.arrive() or flagTime:
            finish_time = time.time()
            dt = finish_time - start_time
            dy = robot0.yPos - ball.yPos
            dang = robot0.theta
            vec_dt.append(dt)
            vec_dy.append(dy)
            vec_dang.append(dang)
            vec_flagsTime.append(flagTime)
            start_time = time.time()
            flagTime = False

            if cont_pos < len(pos_x):
                replacer_all([pos_x[cont_pos], 1000, 1000],[pos_y[cont_pos], 250, 300], [0, 0, 0], [1000, 1000, 1000], [350, 400, 450], [0, 0, 0], 85, 65)
                cont_pos = cont_pos + 1
            else:
                
                cont_pos = 1
                cont_ind += 1
                ga_univector.cost_func(vec_dt, vec_dang, vec_dy)
                flagTime = False
                vec_dt = []
                vec_dy = []
                vec_dang = []
                vec_flagsTime = []

                if len(ga_univector.vec_cost) == 2*ga_univector.npop:
                    temp_pop = np.zeros([2*ga_univector.npop,ga_univector.nvar])
                    aux_temp_pop = np.zeros([ga_univector.npop,ga_univector.nvar])
                    aux_cost = []
                    for i in range(2*ga_univector.npop):
                        if i < ga_univector.npop:
                            temp_pop[i] = ga_univector.oldPop[i]
                        else:
                            temp_pop[i] = ga_univector.pop[i-ga_univector.npop]
                    for i in range(ga_univector.npop):
                        min_value = min(ga_univector.vec_cost)
                        min_index = ga_univector.vec_cost.index(min_value)
                        aux_cost.append(min_value)
                        aux_temp_pop[i] = temp_pop[min_index]
                        ga_univector.vec_cost[min_index] = np.inf
                    ga_univector.pop = deepcopy(aux_temp_pop)
                    ga_univector.vec_cost = deepcopy(aux_cost)
                    #print("Os melhores foram selecionados!!!")
                    for i in range(ga_univector.npop):
                        data_csv.append([cont_gen,ga_univector.pop[i][0],ga_univector.pop[i][1],ga_univector.pop[i][2],ga_univector.pop[i][3],ga_univector.pop[i][4], ga_univector.vec_cost[i],
                                            ga_univector.index_dt[i], ga_univector.max_dt[i], ga_univector.index_dy[i], ga_univector.max_dy[i],ga_univector.index_dang[i], ga_univector.max_dang[i]])
                    ga_univector.findBetterCost()
                    with open('results.csv', 'w', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)

                        # write the header
                        writer.writerow(header)

                        # write multiple rows
                        writer.writerows(data_csv)

                        f.close()
                    print("Média da geração: ", sum(ga_univector.vec_cost)/ga_univector.npop)
                    print("Melhor custo: ", ga_univector.cost_better)
                    print("Parâmetros do individuo: ", ga_univector.pop[ga_univector.index_better])
                    print("----")
                    ga_univector.max_dt = []
                    ga_univector.index_dt = []
                    ga_univector.max_dy = []
                    ga_univector.index_dy = []
                    ga_univector.max_dang = []
                    ga_univector.index_dang = []
            

        elif cont_ind < ga_univector.npop:
            Go_To_Goal(robot0, ball, ga_univector.pop[cont_ind])
            if time.time() - start_time > 10:
                flagTime = True
                start_time = time.time()   
        else:
            ga_univector.nextGen()
            cont_gen += 1
            cont_pos = 1
            cont_ind = 0
            flagTime = False
            vec_dt = []
            vec_dy = []
            vec_dang = []
            vec_flagsTime = []            
        # synchronize code execution based on runtime and the camera FPS
        t2 = time.time()
        if t2 - t1 < 1 / 60:
            time.sleep(1 / 60 - (t2 - t1))
