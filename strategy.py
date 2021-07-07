import action


class Strategy:
    def __init__(self, robot0, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, ball, mray):
        self.robot0 = robot0
        self.robot1 = robot1
        self.robot2 = robot2
        self.robotEnemy0 = robotEnemy0
        self.robotEnemy1 = robotEnemy1
        self.robotEnemy2 = robotEnemy2
        self.ball = ball
        self.mray = mray
    

    def basicStg(self):
        """Picks a strategy depending on the status of the field"""
        
        #For the time being, the only statuses considered are which side of the field the ball is in
        if self.ball.xPos < 0:
            action.shoot(self.robot2, self.ball,leftSide= not self.mray, friend1 = self.robot0, friend2 = self.robot1, enemy1=self.robotEnemy0,  enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
            action.protectGoal(self.robot1, self.ball,50, leftSide= not self.mray)
            action.screenOutBall(self.robot0, self.ball, 10, leftSide= not self.mray)

        else:
            action.shoot(self.robot2, self.ball, leftSide= not self.mray, friend1 = self.robot0, friend2 = self.robot1, enemy1=self.robotEnemy0,  enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
            action.protectGoal(self.robot1, self.ball,50, leftSide= not self.mray)
            action.screenOutBall(self.robot0, self.ball, 10, leftSide= not self.mray)

    





