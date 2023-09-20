import time
import argparse

import fouls
from bridge import (Actuator, Replacer, Vision)
from simClasses import *
from strategy import *

from numpy import sin, cos, arctan2, pi

from vss_communication import StrategyControl, Referee

import action

COM_REF = False

# IDs dos robôs em ordem 0, 1 e 2 na visão da cin
id_robots = [0, 9, 5]

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
    #referee = Referee(mray, "224.5.23.2", 10003)
    #referee = Referee("224.5.23.2", 10060, logger=False)

    # Intialize all clients (real)
    #client_control = StrategyControl(port=20020)
    client_control = StrategyControl(ip='224.5.23.2', port=10015, logger=False, pattern='ssl', convert_coordinates=True)  # Criação do objeto do controle e estratégia
    referee = Referee("224.5.23.2", 10003, logger=False)

    # Initialize all  objects
    robots = []
    for i in range(args.num_robots):
        robot = Robot(i, client_control, mray)
        robots.append(robot)
        # Substituindo o indice para sincronizar com a eletronica
        robots[i].index = i

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

    # Main infinite loop
    t1 = time.time()
    while True:
        t1 = time.time()  # Inicio do tempo de execução

        client_control.update(mray)  # Atualiza os dados da visão
        field, errorCode = client_control.get_data_Red()

        referee.update()  # Atualiza os dados do referee
        data_ref, errorCodeRef = referee.get_data()

        #'''
        data_our_bot = field["our_bots"]  # Save data from allied robots
        data_their_bots = field["their_bots"]  # Save data from enemy robots
        data_ball = field["ball"]  # Save the ball data

        # Necessário testar ainda em campo real
        # Updates vision data on each field object
        #for index, robot in enumerate(robots):
            #robot.set_simulator_data(data_our_bot[index])

        for i in range(len(data_our_bot)):  # Separação de dados recebidos da visão
            for index, robot in enumerate(robots):
                if data_our_bot[i]["robot_id"] == id_robots[index]:  # Se o id do robô recebido é igual ao robô desejado (Código Cin)
                    data_our_bot[i]["robot_id"] = id_robots.index(data_our_bot[i]["robot_id"])  # Adequação de ID dos robôs
                    data_our_bot[i]["orientation"] = arctan2(sin(data_our_bot[i]["orientation"] + pi), cos(data_our_bot[i]["orientation"] + pi))  # Adequação de orientação dos robôs
                    robot.set_simulator_data(data_our_bot[i])
                    break
        
        for i in range(len(data_ball)):
            ball.set_simulator_data(data_ball)
        
        # Testar ainda
        #for index, robot in enumerate(enemy_robots):
            #robot.set_simulator_data(data_their_bots[index])

        if COM_REF:
            if data_ref["foul"] == 6:
                print("GAME ON")
                strategy.coach()
                #action.screen_out_ball(robots[0], ball, 40, True, upper_lim = 90, lower_lim= 50)
                #action.rectangle(robots[2])
                #action.defender_spin(robots[2], ball)
            else:
                print("GAME OFF")
                robots[0].sim_set_vel(0, 0)
                robots[1].sim_set_vel(0, 0)
                robots[2].sim_set_vel(0, 0)
                robots[0].face = 1
                robots[1].face = 1
                robots[2].face = 1 
        else:
            action.rectangle(robots[2])
            #action.defender_spin(robots[2], ball)
            print(robots[2]._coordinates.Y)
        
        t2 = time.time()  # Fim do tempo de execução
        # synchronize code execution based on runtime and the camera FPS
        if (t2 - t1) < 1 / 60:
            time.sleep(1 / 60 - (t2 - t1))
