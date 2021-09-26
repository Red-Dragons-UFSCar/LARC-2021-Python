import action


class Strategy:
    def __init__(self, robot0, robot1, robot2, robot3, robot4, robotEnemy0, robotEnemy1, robotEnemy2, robotEnemy3, robotEnemy4, ball, mray):
        self.robot0 = robot0
        self.robot1 = robot1
        self.robot2 = robot2
        self.robot3 = robot3
        self.robot4 = robot4
        self.robotEnemy0 = robotEnemy0
        self.robotEnemy1 = robotEnemy1
        self.robotEnemy2 = robotEnemy2
        self.robotEnemy3 = robotEnemy3
        self.robotEnemy4 = robotEnemy4
        self.ball = ball
        self.mray = mray

    def coach(self):
        """Picks a strategy depending on the status of the field"""
        # For the time being, the only statuses considered are which side of the field the ball is in
        if self.mray:
            if self.ball.xPos > 135:
                self.basicStgDef()
            else:
                self.basicStgAtt()
        else:
            if self.ball.xPos > 115:
                self.basicStgAtt()
            else:
                self.basicStgDef()

    def basicStgDef(self):
        """Basic original strategy"""
        action.screenOutBall(self.robot3, self.ball, 135, leftSide=not self.mray, upperLim=85, lowerLim=5)
        action.screenOutBall(self.robot4, self.ball, 135, leftSide=not self.mray, upperLim=175, lowerLim=95)
        if not self.mray:
            if self.ball.xPos < 40 and self.ball.yPos > 50 and self.ball.yPos < 130:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
                action.screenOutBall(self.robot1, self.ball, 55, leftSide=not self.mray, upperLim=85, lowerLim=5)
                action.screenOutBall(self.robot2, self.ball, 55, leftSide=not self.mray, upperLim=175, lowerLim=95)
            else:
                listRobots = [self.robot0, self.robot3, self.robot4, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4]
                action.Master_Slave(self.robot1,self.robot2, listRobots, self.ball)
                action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
        else:
            if self.ball.xPos > 195 and self.ball.yPos > 50 and self.ball.yPos < 130:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
                action.screenOutBall(self.robot1, self.ball, 55, leftSide=not self.mray, upperLim=85, lowerLim=5)
                action.screenOutBall(self.robot2, self.ball, 55, leftSide=not self.mray, upperLim=175, lowerLim=95)
            else:
                listRobots = [self.robot0, self.robot3, self.robot4, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4]
                action.Master_Slave(self.robot1,self.robot2, listRobots, self.ball)
                action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)

    def basicStgAtt(self):
        """Basic alternative strategy"""
        listRobots = [self.robot0, self.robot1, self.robot2, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4]
        action.Master_Slave(self.robot3,self.robot4, listRobots, self.ball)

        action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
        action.screenOutBall(self.robot1, self.ball, 90, leftSide=not self.mray, upperLim=85, lowerLim=5)
        action.screenOutBall(self.robot2, self.ball, 90, leftSide=not self.mray, upperLim=175, lowerLim=95)
