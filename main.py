import time
import argparse

import fouls
from bridge import (Actuator, Replacer, Vision, Referee)
from simClasses import *
from strategy import *

from vss_communication import StrategyControl

import action

import pandas as pd

vetor_angulo = []
vetor_tempo = []

t_start = time.time()
t1 = time.time()

if __name__ == "__main__":

    # Fazer tratamento de entradas erradas

    parser = argparse.ArgumentParser(description='Argumentos para execução do time no simulador FIRASim')

    parser.add_argument('-t', '--team', type=str, default="blue",
                        help="Define o time/lado que será executado: blue ou yellow")
    parser.add_argument('-s', '--strategy', type=str, default="twoAttackers",
                        help="Define a estratégia que será jogada: twoAttackers ou default" )
    parser.add_argument('-nr', '--num_robots', type=int, default=3,
                        help="Define a quantia de robos de cada lado")
    parser.add_argument('-op', '--offensivePenalty', type=str, default='spin', dest='op',
                        help="Define o tipo de cobrança ofensiva de penalti: spin ou direct")
    parser.add_argument('-dp', '--defensivePenalty', type=str, default='direct', dest='dp',
                        help="Define o tipo de defesa de penalti: spin ou direct")
    parser.add_argument('-aop', '--adaptativeOffensivePenalty', type=str, default='off', dest='aop', 
                        help="Controla a troca de estratégias de penalti durante o jogo")
    parser.add_argument('-adp', '--adaptativeDeffensivePenalty', type=str, default='off', dest='adp', 
                        help="Controla a troca de estratégias de penalti durante o jogo")


    args = parser.parse_args()

    # Choose team (my robots are yellow)
    if args.team == "yellow":
        mray = True
    else:
        mray = False


    # Initialize all clients (simulation)
    actuator = Actuator(mray, "127.0.0.1", 20011)
    # replacement = Replacer(mray, "224.5.23.2", 10004)
    # vision = Vision(mray, "224.0.0.1", 10002)
    referee = Referee(mray, "224.5.23.2", 10003)

    # Intialize all clients (real)
    client_control = StrategyControl()

    # Initialize all  objects
    robots = []
    for i in range(args.num_robots):
        robot = Robot(i, client_control, mray)
        robots.append(robot)

    #robots = [robots[2], robots[1], robots[0]]

    enemy_robots = []
    for i in range(args.num_robots):
        robot = Robot(i, client_control, not mray)
        enemy_robots.append(robot)

    for robot in robots:
        robot.set_enemies(enemy_robots)
        robot.set_friends(robots.copy())

    ball = Ball()

    list_strategies = [args.strategy, args.op, args.dp, args.aop, args.adp]
    strategy = Strategy(robots, enemy_robots, ball, mray, list_strategies)
    v = 0.2
    incremento = 0.3

    # Main infinite loop
    t1 = time.time()
    while True:
        
        
        client_control.update()
        field, errorCode = client_control.get_data_Red()

        #'''
        if errorCode == 0:
            data_our_bot = field["our_bots"]  # Save data from allied robots
            data_their_bots = field["their_bots"]  # Save data from enemy robots
            data_ball = field["ball"]  # Save the ball data

            # Updates vision data on each field object
            for index, robot in enumerate(robots):
                robot.set_simulator_data(data_our_bot[index])
            
            for index, robot in enumerate(enemy_robots):
                robot.set_simulator_data(data_their_bots[index])

            ball.set_simulator_data(data_ball)

            #print(ball.get_coordinates().X)
            #strategy.handle_game_on()
            strategy.coach2()
            #action.defender_spin(robots[2], ball, left_side=not mray)  # Attacker behavior
            #robots[2].sim_set_vel(20, 0.5)
            
            #action.shoot(robots[2], ball)
            #action.rectangle(robots[2])
            #action.screen_out_ball(robots[0], ball, 130, True, upper_lim = 90, lower_lim= 50)
            #action.screen_out_ball(robots[1], ball, 110, True, upper_lim = 100, lower_lim= 30)
            #action.defender_spin(robots[2], ball)
            #'''
            # synchronize code execution based on runtime and the camera FPS
            if v >= 30:
                incremento = incremento*(-1)
            elif v <= -30:
                incremento = incremento*(-1)
            v = v + incremento
            #robots[2].sim_set_vel(0, v        print("Fim")
            t2 = time.time()
            #if t2 - t1 < 1 / 60:
                #time.sleep(1 / 60 - (t2 - t1))
