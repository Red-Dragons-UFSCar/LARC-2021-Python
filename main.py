from bridge import (Actuator, Replacer, Vision, Referee,
                        NUM_BOTS, convert_angle, Entity)

from math import pi, fmod, atan2, fabs
from action import defenderWall, atacante_lider,ataque,defenderPenalty,defesa_atacantes
import sys

from simClasses import *
import action
import fouls

import time

from strategy import *

if __name__ == "__main__":

    try:
        team = sys.argv[1]
    except:
        print("[ERRO]")
        print("Digite como parâmetro o time que você ira jogar!")
        print("Exemplo: python3 main.py yellow")
        sys.exit()

    if team != "blue" and team != "yellow":
        print("[ERRO]")
        print("Selecione um time válido! ")
        print("Para jogar com o azul, o primeiro argumento deve ser 'blue'")
        print("Para jogar com o amarelo, o primeiro argumento deve ser 'yellow'")
        sys.exit()

    # Choose team (my robots are yellow)
    if team == "yellow":
        mray = True
    else:
        mray = False

    # Initialize all clients
    actuator = Actuator(mray, "127.0.0.1", 20011)
    replacement = Replacer(mray, "224.5.23.2", 10006)
    vision = Vision(mray, "224.0.0.1", 10042)
    referee = Referee(mray, "224.5.23.2", 10047)

    # Initialize all  objects
    robot0 = Robot(0, actuator, mray)
    robot1 = Robot(1, actuator, mray)
    robot2 = Robot(2, actuator, mray)
    robot3 = Robot(3, actuator, mray)
    robot4 = Robot(4, actuator, mray)

    robotEnemy0 = Robot(0, actuator, not mray)
    robotEnemy1 = Robot(1, actuator, not mray)
    robotEnemy2 = Robot(2, actuator, not mray)
    robotEnemy3 = Robot(3, actuator, not mray)
    robotEnemy4 = Robot(4, actuator, not mray)

    ball = Ball()

    strategy = Strategy(robot0, robot1, robot2, robot3, robot4, robotEnemy0, robotEnemy1, robotEnemy2, robotEnemy3, robotEnemy4, ball, mray)

    # Main infinite loop
    while True:
        t1 = time.time()
        # Atualiza a situação das faltas
        referee.update()
        ref_data = referee.get_data()

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
        robot3.simGetPose(data_our_bot[3])
        robot4.simGetPose(data_our_bot[4])
        robotEnemy0.simGetPose(data_their_bots[0])
        robotEnemy1.simGetPose(data_their_bots[1])
        robotEnemy2.simGetPose(data_their_bots[2])
        robotEnemy3.simGetPose(data_their_bots[3])
        robotEnemy4.simGetPose(data_their_bots[4])
        ball.simGetPose(data_ball)

        #strategy.coach()
        #defenderWall(robot1,robot2,ball)
        


        if ref_data["game_on"]:
            # Se o modo de jogo estiver em "Game on"
            strategy.coach()

        elif ref_data["foul"] == 1 and ref_data["yellow"] == (not mray):
            #Detectando penalti defensivo
            strategy.penaltyDefensive = True
            actuator.stop()
            fouls.replacement_fouls(replacement,ref_data,mray)

        elif ref_data["foul"] == 1 and ref_data["yellow"] == (mray):
            #Detectando penalti ofensivo
            strategy.penaltyOffensive = True
            actuator.stop()
            fouls.replacement_fouls(replacement,ref_data,mray)

        elif ref_data["foul"] != 7:
            if ref_data["foul"] != 5: # Mudando a flag exceto em caso de Stop
                Strategy.penaltyOffensive = False
                Strategy.penaltyDefensive = False
            fouls.replacement_fouls(replacement,ref_data,mray)
            actuator.stop()

        else:
            actuator.stop()

        t2 = time.time()
        if t2-t1<1/60:
            time.sleep(1/60 - (t2-t1))
