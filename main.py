import time
import argparse

import fouls
from bridge import (Actuator, Replacer, Vision, Referee)
from simClasses import *
from strategy import *

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

    args = parser.parse_args()

    # Choose team (my robots are yellow)
    if args.team == "yellow":
        mray = True
    else:
        mray = False


    # Initialize all clients
    actuator = Actuator(mray, "127.0.0.1", 20011)
    replacement = Replacer(mray, "224.5.23.2", 10004)
    vision = Vision(mray, "224.0.0.1", 10002)
    referee = Referee(mray, "224.5.23.2", 10003)

    # Initialize all  objects
    robots = []
    for i in range(args.num_robots):
        robot = Robot(i, actuator, mray)
        robots.append(robot)

    enemy_robots = []
    for i in range(args.num_robots):
        robot = Robot(i, actuator, not mray)
        enemy_robots.append(robot)

    for robot in robots:
        robot.set_enemies(enemy_robots)
        robot.set_friends(robots.copy())

    ball = Ball()

    list_strategies = [args.strategy, args.op, args.dp]
    strategy = Strategy(robots, enemy_robots, ball, mray, list_strategies)

    # Main infinite loop
    while True:
        t1 = time.time()
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
        for index, robot in enumerate(robots):
            robot.set_simulator_data(data_our_bot[index])
        
        for index, robot in enumerate(enemy_robots):
            robot.set_simulator_data(data_their_bots[index])
        ball.set_simulator_data(data_ball)

        if ref_data["game_on"]:
            # If the game mode is set to "Game on"
            strategy.decider()

        elif ref_data["foul"] == 1 and ref_data["yellow"] == (not mray):
            # detecting defensive penalty
            strategy.penaltyDefensive = True
            actuator.stop()
            fouls.replacement_fouls(replacement, ref_data, mray, args.op, args.dp)

        elif ref_data["foul"] == 1 and ref_data["yellow"] == (mray):
            # detecting offensive penalty
            strategy.penaltyOffensive = True
            actuator.stop()
            fouls.replacement_fouls(replacement, ref_data, mray, args.op, args.dp)

        elif ref_data["foul"] != 7:
            if ref_data["foul"] != 5:  # Changing the flag except in the Stop case
                strategy.penaltyOffensive = False
                strategy.penaltyDefensive = False
            fouls.replacement_fouls(replacement, ref_data, mray, args.op, args.dp)
            actuator.stop()

        else:
            actuator.stop()

        # synchronize code execution based on runtime and the camera FPS
        t2 = time.time()
        if t2 - t1 < 1 / 60:
            time.sleep(1 / 60 - (t2 - t1))
