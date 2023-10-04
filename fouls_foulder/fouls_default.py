from numpy import arctan2,pi,sqrt,cos,sin,array,matmul,amin,where,zeros,delete,append,int32,deg2rad
from bridge import (Actuator, Replacer, Vision, Referee,NUM_BOTS, convert_angle, Entity)
import random
from simClasses import Ball
from action import Robot2Position, SendRobotPosition

def automatic_replacement(ref_data, mray, robot0, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2):
    ball = Ball()
    list_r0 = []
    list_r1 = []
    list_r2 = []

    strategy = 'default'

    teamYellow = (ref_data["teamcolor"] == 1)
    
    if mray == False:
        if ref_data["foul"] == 1 or ref_data["foul"] == 2:
            if teamYellow: # Defensivo
                list_r0 = SendRobotPosition(mray, ref_data, robot0.index, strategy)
                list_r1 = SendRobotPosition(mray, ref_data, robot1.index, strategy)
                list_r2 = SendRobotPosition(mray, ref_data, robot2.index, strategy)
            else: # Ofensivo
                list_r0 = SendRobotPosition(mray, ref_data, robot0.index, strategy)
                list_r1 = SendRobotPosition(mray, ref_data, robot1.index, strategy)
                list_r2 = SendRobotPosition(mray, ref_data, robot2.index, strategy) 
                '''
                rand = random.random()
                if rand > 1/2:
                    list_r2 = SendRobotPosition(mray, ref_data, robot2.index, strategy, 'if') 
                else:
                    list_r2 = SendRobotPosition(mray, ref_data, robot2.index, strategy, 'else') 
                """r = random.uniform(0,1)
                if r <0.5:
                    entidade4 = Entity(x=180, y=70,a=50, index=4)
                else:
                    entidade4 = Entity(x=180, y=110,a=-50, index=4)"""
                '''
            Robot2Position(robot0, ball, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, list_r0, list_r1, list_r2)

        elif ref_data["foul"] == 3:
            list_r0 = SendRobotPosition(mray, ref_data, robot0.index, strategy)
            list_r1 = SendRobotPosition(mray, ref_data, robot1.index, strategy)
            list_r2 = SendRobotPosition(mray, ref_data, robot2.index, strategy)
            Robot2Position(robot0, ball, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, list_r0, list_r1, list_r2)

        elif ref_data["foul"] == 4:
            list_r0 = SendRobotPosition(mray, ref_data, robot0.index, strategy)
            list_r1 = SendRobotPosition(mray, ref_data, robot1.index, strategy)
            list_r2 = SendRobotPosition(mray, ref_data, robot2.index, strategy)

            Robot2Position(robot0, ball, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, list_r0, list_r1, list_r2)

    if mray == True:
        if ref_data["foul"] == 1 or ref_data["foul"] == 2:
            if teamYellow: # Ofensivo
                list_r0 = SendRobotPosition(mray, ref_data, robot0.index, strategy)
                list_r1 = SendRobotPosition(mray, ref_data, robot1.index, strategy)
                list_r2 = SendRobotPosition(mray, ref_data, robot2.index, strategy) 
                '''
                rand = random.random()
                if rand > 1/2:
                    list_r2 = SendRobotPosition(mray, ref_data, robot2.index, strategy, 'if') 

                else:
                    list_r2 = SendRobotPosition(mray, ref_data, robot2.index, strategy, 'else') 
                '''
                """r = random.uniform(0,1)
                if r <0.5:
                    entidade4 = Entity(x=180, y=70,a=50, index=4)
                else:
                    entidade4 = Entity(x=180, y=110,a=-50, index=4)"""
            else:
                list_r0 = SendRobotPosition(mray, ref_data, robot0.index, strategy)
                list_r1 = SendRobotPosition(mray, ref_data, robot1.index, strategy)
                list_r2 = SendRobotPosition(mray, ref_data, robot2.index, strategy)
            Robot2Position(robot0, ball, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, list_r0, list_r1, list_r2)

        elif ref_data["foul"] == 3 or ref_data["foul"] == 2:
            list_r0 = SendRobotPosition(mray, ref_data, robot0.index, strategy)
            list_r1 = SendRobotPosition(mray, ref_data, robot1.index, strategy)
            list_r2 = SendRobotPosition(mray, ref_data, robot2.index, strategy)
            Robot2Position(robot0, ball, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, list_r0, list_r1, list_r2)

        elif ref_data["foul"] == 4:
            list_r0 = SendRobotPosition(mray, ref_data, robot0.index, strategy)
            list_r1 = SendRobotPosition(mray, ref_data, robot1.index, strategy)
            list_r2 = SendRobotPosition(mray, ref_data, robot2.index, strategy)
            
            Robot2Position(robot0, ball, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, list_r0, list_r1, list_r2)