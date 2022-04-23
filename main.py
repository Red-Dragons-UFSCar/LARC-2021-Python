import time
import sys

import fouls
from bridge import (Actuator, Replacer, Vision, Referee)
from simClasses import *
from strategy import *

if __name__ == "__main__":

    # checking possible errors about the writing of commands
    try:
        team = sys.argv[1]
        strategySelected = sys.argv[2]
    except:
        print("[ERROR]")
        print("Please enter as parameters the team and the strategy that will be used")
        print("Exemples:")
        print("python3 main.py blue default")
        print("python3 main.py yellow twoAttackers")
        sys.exit()

    if team != "blue" and team != "yellow":
        print("Select a valid team! ")
        print("To play as blue, the first argument must be 'blue")
        print("To play as yellow, the first argument must be 'yellow'")
        sys.exit()

    if strategySelected != "default" and strategySelected != "twoAttackers":
        print("Select a valid strategy")
        print("To play with the default strategy, the second argument must be 'default'")
        print("To play with the two attackers strategy, the second argument must be 'twoAttackers'")
        sys.exit()

    # Choose team (my robots are yellow)
    if team == "yellow":
        mray = True
    else:
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

    strategy = Strategy(robot0, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, ball, mray, strategySelected)

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
        robot0.sim_get_pose(data_our_bot[0])
        robot1.sim_get_pose(data_our_bot[1])
        robot2.sim_get_pose(data_our_bot[2])
        robotEnemy0.sim_get_pose(data_their_bots[0])
        robotEnemy1.sim_get_pose(data_their_bots[1])
        robotEnemy2.sim_get_pose(data_their_bots[2])
        ball.sim_get_pose(data_ball)

        if ref_data["game_on"]:
            # If the game mode is set to "Game on"
            strategy.decider()

        elif ref_data["foul"] == 1 and ref_data["yellow"] == (not mray):
            # detecting defensive penalty
            strategy.penaltyDefensive = True
            actuator.stop()
            fouls.replacement_fouls(replacement, ref_data, mray)

        elif ref_data["foul"] == 1 and ref_data["yellow"] == (mray):
            # detecting offensive penalty
            strategy.penaltyOffensive = True
            actuator.stop()
            fouls.replacement_fouls(replacement, ref_data, mray)

        elif ref_data["foul"] != 7:
            if ref_data["foul"] != 5:  # Changing the flag except in the Stop case
                strategy.penaltyOffensive = False
                strategy.penaltyDefensive = False
            fouls.replacement_fouls(replacement, ref_data, mray)
            actuator.stop()

        else:
            actuator.stop()

        # synchronize code execution based on runtime and the camera FPS
        t2 = time.time()
        if t2 - t1 < 1 / 60:
            time.sleep(1 / 60 - (t2 - t1))
