import simClasses
import main
import action
import numpy

def strategy(ball, robot0, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2):
    """Picks a strategy depending on the status of the field"""
    
    #For the time being, the only statuses considered are which side of the field the ball is in
    if ball.Ypos > 0:
        action.shoot(robot2,ball,leftSide= not mray, friend1 = robot0, friend2 = robot1, enemy1=robotEnemy0,  enemy2=robotEnemy1, enemy3=robotEnemy2)
        action.protectGoal(robot1, ball,50, leftSide= not mray)
        action.screenOutBall(robot0,ball,10,leftSide= not mray)

    else:
        action.shoot(robot2,ball,leftSide= not mray, friend1 = robot0, friend2 = robot1, enemy1=robotEnemy0,  enemy2=robotEnemy1, enemy3=robotEnemy2)
        action.protectGoal(robot1, ball,50, leftSide= not mray)
        action.screenOutBall(robot0,ball,10,leftSide= not mray)

    





