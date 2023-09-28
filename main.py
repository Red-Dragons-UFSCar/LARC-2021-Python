import time
import argparse

import fouls
from bridge import (Actuator, Replacer, Vision)
from simClasses import *
from strategy import *

from numpy import sin, cos, arctan2, pi

from vss_communication import StrategyControl, Referee

import action

import serial

from threading import Timer

class RepeatTimer(Timer):  
    def run(self):  
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)  

COM_REF = True

# Eletronica
ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/ttyUSB0' # Mudar aqui dependendo da COM do transmissor
ser.open()

def verifyDirection(v):
    if v > 0:
        direction = 0b01
    elif v < 0:
        direction = 0b10
    else:
        direction = 0b11
    return direction

# IDs dos robôs em ordem 0, 1 e 2 na visão da cin
id_robots = [6, 10, 5]

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
    client_control = StrategyControl(ip='224.5.23.2', port=10015, yellowTeam=mray, logger=False, pattern='ssl', convert_coordinates=True)  # Criação do objeto do controle e estratégia
    referee = Referee("224.5.23.2", 10005, logger=False)

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
        #print(data_our_bot)

        for i in range(len(data_our_bot)):  # Separação de dados recebidos da visão
            for index, robot in enumerate(robots):
                if data_our_bot[i]["robot_id"] == id_robots[index]:  # Se o id do robô recebido é igual ao robô desejado (Código Cin)
                    data_our_bot[i]["robot_id"] = id_robots.index(data_our_bot[i]["robot_id"])  # Adequação de ID dos robôs
                    data_our_bot[i]["orientation"] = arctan2(sin(data_our_bot[i]["orientation"] + pi), cos(data_our_bot[i]["orientation"] + pi))  # Adequação de orientação dos robôs
                    robot.set_simulator_data(data_our_bot[i])
                    break
        
        for i in range(len(data_ball)):
            ball.set_simulator_data(data_ball)
        
        #time.sleep(1/60)

    x = RepeatTimer((1/120), getData, args=(ball, robots))
    x.start()

    # Main infinite loop
    t1 = time.time()
    while True:
        t1 = time.time()  # Inicio do tempo de execução

        #client_control.update(mray)  # Atualiza os dados da visão
        #field, errorCode = client_control.get_data_Red()

        referee.update()  # Atualiza os dados do referee
        data_ref, errorCodeRef = referee.get_data()

        #'''
        #data_our_bot = field["our_bots"]  # Save data from allied robots
        #data_their_bots = field["their_bots"]  # Save data from enemy robots
        #print(data_our_bot)
        #data_ball = field["ball"]  # Save the ball data

        # Necessário testar ainda em campo real
        # Updates vision data on each field object
        #for index, robot in enumerate(robots):
            #robot.set_simulator_data(data_our_bot[index])

        #data_our_bot2 = []
        #for i in range(len(data_our_bot)):
        #    if data_our_bot[i]['robot_id'] > 2:
        #        data_our_bot2.append(data_our_bot[i])
        
        #data_our_bot = data_our_bot2

        #for i in range(len(data_our_bot)):  # Separação de dados recebidos da visão
        #    for index, robot in enumerate(robots):
        #        if data_our_bot[i]["robot_id"] == id_robots[index]:  # Se o id do robô recebido é igual ao robô desejado (Código Cin)
        #            data_our_bot[i]["robot_id"] = id_robots.index(data_our_bot[i]["robot_id"])  # Adequação de ID dos robôs
        #            data_our_bot[i]["orientation"] = arctan2(sin(data_our_bot[i]["orientation"] + pi), cos(data_our_bot[i]["orientation"] + pi))  # Adequação de orientação dos robôs
        #            robot.set_simulator_data(data_our_bot[i])
        #            break
        
        #print("Index: ", robots[0].index)
        #print("xPos: ", robots[0]._coordinates.X)
        #print(robots[0]._coordinates.rotation)
        #for i in range(len(data_ball)):
        #    ball.set_simulator_data(data_ball)
        
        # Testar ainda
        #for index, robot in enumerate(enemy_robots):
            #robot.set_simulator_data(data_their_bots[index])

        if COM_REF:
            if data_ref["foul"] == 6:
                print("GAME ON")
                #strategy.coach()
                #action.screen_out_ball(robots[2], ball, 85, True, upper_lim = 90, lower_lim= 50)
                #print(data_our_bot)
                #action.rectangle(robots[2])
                action.defender_spin(robots[2], ball)
            else:
                print("GAME OFF")
                robots[0].sim_set_vel(0, 0)
                robots[1].sim_set_vel(0, 0)
                robots[2].sim_set_vel(0, 0)
                robots[0].face = 1
                robots[1].face = 1
                robots[2].face = 1 
        else:
            #action.rectangle(robots[2])
            #action.defender_spin(robots[2], ball)
            #action.screen_out_ball(robots[1], ball, 40, True, upper_lim = 90, lower_lim= 50)
            #strategy.coach()
            print(robots[2]._coordinates.Y)
        
        # Eletronica

        vl_1 = int(robots[0].vR)
        vr_1 = int(robots[0].vL)
        vl_2 = int(robots[1].vR)
        vr_2 = int(robots[1].vL)
        vl_3 = int(robots[2].vR)
        vr_3 = int(robots[2].vL)

        # Direções de cada motor
        dirMot1_Robo1 = verifyDirection(vl_1)
        dirMot2_Robo1 = verifyDirection(vr_1)
        dirMot1_Robo2 = verifyDirection(vl_2)
        dirMot2_Robo2 = verifyDirection(vr_2)
        dirMot1_Robo3 = verifyDirection(vl_3)
        dirMot2_Robo3 = verifyDirection(vr_3)

        if( not (vl_3 == 100 and vr_3 == 100) ):
            vl_3 = min(vl_3, 80)
            vr_3 = min(vr_3, 80)

        # Palavra de Bytes de direção
        direcao1 = dirMot1_Robo1<<6 | dirMot2_Robo1<<4 | dirMot1_Robo2<<2 | dirMot2_Robo2
        direcao2 = dirMot1_Robo3<<6 | dirMot2_Robo3<<4

        # Vetor de mensagem para a eletrônica
        #print("Palavra: ", [111, direcao1, direcao2, vl_1, vr_1, vl_2, vr_2, vl_3, vr_3, 113])
        Rd = bytearray([111, direcao1, direcao2, abs(vl_1), abs(vr_1), abs(vl_2), abs(vr_2), abs(vl_3), abs(vr_3), 113])
        
        # Escrita na porta serial
        ser.write(Rd)

        t2 = time.time()  # Fim do tempo de execução
        # synchronize code execution based on runtime and the camera FPS
        if (t2 - t1) < 1 / 60:
            time.sleep(1 / 60 - (t2 - t1))
