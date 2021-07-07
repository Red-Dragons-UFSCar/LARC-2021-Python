#!/usr/bin/env python3

from bridge import (Actuator, Replacer, Vision, Referee,
                        NUM_BOTS, convert_angle, Entity)

from math import pi, fmod, atan2, fabs

from simClasses import *

from strategy import *

if __name__ == "__main__":

    # Choose team (my robots are yellow)
    mray = False

    # Initialize all clients
    actuator = Actuator(mray, "127.0.0.1", 20011)
    replacement = Replacer(mray, "224.5.23.2", 10004)
    vision = Vision(mray, "224.0.0.1", 10002)
    referee = Referee(mray, "224.5.23.2", 10003)

    # Initialize all  objects
    robot0 = Robot(0, actuator)
    robot1 = Robot(1, actuator)
    robot2 = Robot(2, actuator)

    robotEnemy0 = Robot(0, actuator)
    robotEnemy1 = Robot(1, actuator)
    robotEnemy2 = Robot(2, actuator)

    ball = Ball()

    strategy = Strategy(robot0, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, ball)

    # Main infinite loop
    while True:
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

        if ref_data["game_on"]:
            # Se o modo de jogo estiver em "Game on"
            strategy.basicStg()


        elif ref_data["foul"] != 7:
            # foul behaviour
            actuator.stop()

        else:
            # halt behavior
            actuator.stop()
