from bridge import (Actuator, Replacer, Vision, Referee,
                        NUM_BOTS, convert_angle, Entity)

from math import pi, fmod, atan2, fabs

import sys

from simClasses import *
import action
import fouls

import time

from strategy import *

if __name__ == "__main__":

    try:
        team = sys.argv[1]
        strategySelected = sys.argv[2]
    except:
        print("[ERRO]")
        print("Digite por parametros o time e a estratégia utilizada")
        print("Exemplos:")
        print("python3 main.py blue default")
        print("python3 main.py yellow twoAttackers")
        sys.exit()

    if team != "blue" and team != "yellow":
        print("Selecione um time válido! ")
        print("Para jogar com o azul, o primeiro argumento deve ser 'blue'")
        print("Para jogar com o amarelo, o primeiro argumento deve ser 'yellow'")
        sys.exit()

    if strategySelected != "default" and strategySelected != "twoAttackers":
        print("Selecione uma estratégia válida! ")
        print("Para jogar com a estratégia default, o segundo argumento deve ser 'default'")
        print("Para jogar com a estratégia dois Atacantes, o segundo argumento deve ser 'twoAttackers'")
        sys.exit()

    # Choose team (my robots are yellow)
    if team == "yellow":
        mray = True
    else:
        mray = False

    #mray = True

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

    strategy = Strategy(robot0, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, ball, mray, strategySelected)

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
        robotEnemy0.simGetPose(data_their_bots[0])
        robotEnemy1.simGetPose(data_their_bots[1])
        robotEnemy2.simGetPose(data_their_bots[2])
        ball.simGetPose(data_ball)

        #if ref_data["game_on"] or ref_data['foul'] == 5:
        if ref_data["game_on"]:
            # Se o modo de jogo estiver em "Game on"
            #strategy.twoAttackers()
            #strategy.coach()
            strategy.decider()
            #action.defenderSpin(robot2, ball, leftSide=not mray, friend1=robot0, friend2=robot1,
                         #enemy1=robotEnemy0, enemy2=robotEnemy1, enemy3=robotEnemy2)
            #action.screenOutBall(robot0, ball, 14, not mray, upperLim=81, lowerLim=42)
            #action.screenOutBall(self.robot0, self.ball, 14, leftSide=not self.mray, upperLim=81, lowerLim=42)

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
                strategy.penaltyOffensive = False
                strategy.penaltyDefensive = False
            fouls.replacement_fouls(replacement,ref_data,mray)
            actuator.stop()

        else:
            actuator.stop()

        t2 = time.time()
        if t2-t1<1/60:
            time.sleep(1/60 - (t2-t1))
