# Bibliotecas nativas
import argparse
from numpy import sin, cos, arctan2, pi
import serial
from threading import Timer
import time

# Bibliotecas estruturais
import action
from bridge import (Actuator, Replacer, Vision)
import fouls
from fouls_handler import FoulsHandler
from simClasses import *
from strategy import *
from vss_communication import StrategyControl, Referee

# Classe para interrupção de tempo
class RepeatTimer(Timer):  
    def run(self):  
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)  

# Flag que ativa a comunicação com o Referee
COM_REF = True

# Eletronica
ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/ttyUSB0' # Mudar aqui dependendo da COM do transmissor
ser.open()

def verifyDirection(v):
    """Input: Velocidade linear
    Description: Determina a palavra binária de direção da eletrônica a partir da velocidade linear recebida
    da estratégia.
    Output: Direção (2 bits)"""
    if v > 0:
        direction = 0b01
    elif v < 0:
        direction = 0b10
    else:
        direction = 0b11
    return direction

def getData(ball, robots, mray):
    """Input: Objeto da bola, lista de objetos dos robôs
    Description: Determina a palavra binária de direção da eletrônica a partir da velocidade linear recebida
    da estratégia.
    Output: Direção (2 bits)"""
    #TODO Colocar os robos adversários aqui também

    # Informações da visão
    client_control.update(mray)
    field = client_control.get_data()

    if mray:
        data_our_bot = field[0]["robots_yellow"]  # Salva os dados dos robôs aliados
        data_their_bots = field[0]["robots_blue"]  # Salva os dados dos robôs inimigos
    else:
        data_our_bot = field[0]["robots_blue"]  # Salva os dados dos robôs aliados
        data_their_bots = field[0]["robots_yellow"]  # Salva os dados dos robôs inimigos
    
    data_ball = field[0]["ball"]  # Salva os dados da bola

    #print(data_our_bot)

    data_our_bot2 = []
    for i in range(len(data_our_bot)): # Tratamento provisório dos dados da visão - utilização de IDs maiores que 2
        if data_our_bot[i]['robot_id'] > 2:
            data_our_bot2.append(data_our_bot[i])
    
    data_our_bot = data_our_bot2

    for i in range(len(data_our_bot)):  # Separação de dados recebidos da visão
        for index, robot in enumerate(robots):
            if data_our_bot[i]["robot_id"] == id_robots[index]:  # Se o id do robô recebido é igual ao robô desejado (Código Cin)
                data_our_bot[i]["robot_id"] = id_robots.index(data_our_bot[i]["robot_id"])  # Adequação de ID dos robôs
                data_our_bot[i]["orientation"] = arctan2(sin(data_our_bot[i]["orientation"] + pi), cos(data_our_bot[i]["orientation"] + pi))  # Adequação de orientação dos robôs
                robot.set_simulator_data(data_our_bot[i])
                break
    
    for i in range(len(data_ball)): # Recebimento dos dados da bola
        ball.set_simulator_data(data_ball)

# IDs dos robôs em ordem 0, 1 e 2 na visão da cin
id_robots = [6, 10, 5]

t_start = time.time()
t1 = time.time()

if __name__ == "__main__":

    # Fazer tratamento de entradas erradas

    parser = argparse.ArgumentParser(description='Argumentos para execução do time no simulador FIRASim')

    parser.add_argument('-t', '--team', type=str, default="blue",
                        help="Define o time que será jogado: blue ou yellow")
    parser.add_argument('-c', '--side', type=str, default='left',
                        help="Define o lado que será jogado: left ou right")
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

    # Choose side
    if args.side == 'left':
        left_side = True
    else:
        left_side = False


    currentFouls = FoulsHandler('default')

    # Initialize all clients (simulation)
    '''
    actuator = Actuator(mray, "127.0.0.1", 20011)
    replacement = Replacer(mray, "224.5.23.2", 10004)
    vision = Vision(mray, "224.0.0.1", 10002)
    referee = Referee(mray, "224.5.23.2", 10003)
    '''
    # Intialize all clients (real)
    client_control = StrategyControl(ip='224.5.23.2', port=10015, yellowTeam=mray, logger=False, pattern='ssl', convert_coordinates=True)  # Criação do objeto do controle e estratégia
    referee = Referee("224.5.23.2", 10003, logger=False)
    #referee = Referee(mray, "224.5.23.2", 10003)

    # Initialize all  objects
    robots = []
    for i in range(args.num_robots):
        robot = Robot(i, client_control, not left_side)
        robots.append(robot)
        # Substituindo o indice para sincronizar com a eletronica
        robots[i].index = i

    enemy_robots = []
    for i in range(args.num_robots):
        robot = Robot(i, client_control, left_side)
        enemy_robots.append(robot)

    for robot in robots:
        robot.set_enemies(enemy_robots)
        robot.set_friends(robots.copy())

    ball = Ball()

    list_strategies = [args.strategy, args.op, args.dp, args.aop, args.adp]
    strategy = Strategy(robots, enemy_robots, ball, not left_side, list_strategies)

    # Inicialização da thread de visão
    x = RepeatTimer((1/120), getData, args=(ball, robots, mray))
    x.start()

    selectedReplacer = "auto"
    #selectedReplacer = None

    # Main infinite loop
    t1 = time.time()
    while True:
        t1 = time.time()  # Inicio do tempo de execução

        referee.update()  # Atualiza os dados do referee
        data_ref, errorCodeRef = referee.get_data()
        #data_ref = referee.get_data()
        print(data_ref)

        if data_ref['foul'] != 5:
            current_ref = data_ref['foul']
            current_team_foul = data_ref['teamcolor']
            current_quad = data_ref['foulQuadrant']
        print(current_ref)

        if COM_REF:
            if data_ref["foul"] == 6:
                print("GAME ON")
                #strategy.coach()
                strategy.coach_fisico()
                #action.screen_out_ball(robots[2], ball, 85, True, upper_lim = 90, lower_lim= 50)
                #action.rectangle(robots[2])
                #action.defender_spin(robots[0], ball)
            elif data_ref["foul"] != 7:
                if selectedReplacer == "auto":
                    if data_ref["foul"] == 5 and (current_ref != -1 and current_ref != 6):
                        print("arruma stop")
                        data_ref["foul"] = current_ref
                        data_ref["teamcolor"] = current_team_foul
                        data_ref["foulQuadrant"] = current_quad
                        currentFouls.automatic_replacement(data_ref, not left_side, robots[0], robots[1], robots[2], enemy_robots[0], enemy_robots[1], enemy_robots[2])
                        data_ref["foul"] = 5
                        data_ref["foulQuadrant"] = 0
                    #actuator.stop()
                    elif current_ref == 6 or current_ref == 7:
                        robots[0].sim_set_vel(0, 0)
                        robots[1].sim_set_vel(0, 0)
                        robots[2].sim_set_vel(0, 0)
                        robots[0].face = 1
                        robots[1].face = 1
                        robots[2].face = 1 
                    else:
                        currentFouls.automatic_replacement(data_ref, not left_side, robots[0], robots[1], robots[2], enemy_robots[0], enemy_robots[1], enemy_robots[2])
                else:
                    robots[0].sim_set_vel(0, 0)
                    robots[1].sim_set_vel(0, 0)
                    robots[2].sim_set_vel(0, 0)
                    robots[0].face = 1
                    robots[1].face = 1
                    robots[2].face = 1
            else:
                print("GAME OFF")
                robots[0].sim_set_vel(0, 0)
                robots[1].sim_set_vel(0, 0)
                robots[2].sim_set_vel(0, 0)
                robots[0].face = 1
                robots[1].face = 1
                robots[2].face = 1 
        else:
            print("REF OFF")
            #action.rectangle(robots[2])
            #action.defender_spin(robots[2], ball)
            #action.screen_out_ball(robots[1], ball, 40, True, upper_lim = 90, lower_lim= 50)
            #strategy.coach()
            
        # ---- Envio de informações para a eletronica

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

        #if( not (vl_3 == 100 and vr_3 == 100) ):
        #    vl_3 = min(vl_3, 80)
        #    vr_3 = min(vr_3, 80)

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
