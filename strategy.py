import action
from numpy import *

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
        self.penaltyDefensive = False
        self.penaltyOffensive = False

    def coach(self):
        """Picks a strategy depending on the status of the field"""
        # For the time being, the only statuses considered are which side of the field the ball is in

        if self.penaltyDefensive == True:
            self.penaltyModeDefensive()
        elif self.penaltyOffensive == True:
            self.penaltyModeOffensive()
        else:
            if self.mray:
                if self.ball.xPos > 85:
                    self.basicStgDef()
                else:
                    self.basicStgAtt()
            else:
                if self.ball.xPos > 85:
                    self.basicStgAtt()
                else:
                    self.basicStgDef()

    def basicStgDef(self):
        """Basic original strategy"""
        if not self.mray:
            if self.ball.xPos < 40 and self.ball.yPos > 30 and self.ball.yPos < 110:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
                self.twoAttackers()
            else:
                self.twoAttackers()
                action.screenOutBall(self.robot0, self.ball, 10, leftSide=not self.mray, upperLim=81, lowerLim=42)
        else:
            if self.ball.xPos > 130 and self.ball.yPos > 30 and self.ball.yPos < 110:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
                self.twoAttackers()
            else:
                self.twoAttackers()
                action.screenOutBall(self.robot0, self.ball, 10, leftSide=not self.mray, upperLim=81, lowerLim=42)

    def basicStgAtt(self):
        """Basic alternative strategy"""
        self.twoAttackers()
        action.screenOutBall(self.robot0, self.ball, 10, leftSide=not self.mray, upperLim=81, lowerLim=42)

    def stgFullAtt(self):
        """Crazy test attack strategy"""
        action.shoot(self.robot2, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot1,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        action.shoot(self.robot1, self.ball, leftSide=not self.mray, friend1=self.robot1, friend2=self.robot2,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        action.screenOutBall(self.robot0, self.ball, 10, leftSide=not self.mray)

    def penaltyModeDefensive(self):
        action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray, friend1=self.robot1, friend2=self.robot2,
                 enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        action.shoot(self.robot1, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot2,
                 enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        action.shoot(self.robot2, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot1,
                 enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        if not self.mray:
            if self.ball.xPos >48 or self.ball.yPos < 30 or self.ball.yPos > 100:
                self.penaltyDefensive = False
        else:
            if self.ball.xPos < 112 or self.ball.yPos < 30 or self.ball.yPos > 100:
                self.penaltyDefensive = False

    def penaltyModeOffensive(self):
        action.screenOutBall(self.robot0, self.ball, 10, leftSide=not self.mray)
        action.shoot(self.robot1, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot2,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        action.attackPenalty(self.robot2, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot1,
                 enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        if sqrt((self.ball.xPos-self.robot2.xPos)**2+(self.ball.yPos-self.robot2.yPos)**2) > 20:
            self.penaltyOffensive = False

    def twoAttackers(self):

        action.Master_Slave(self.robot0, self.robot1,self.robot2, self.ball, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2)
        #action.screenOutBall(self.robot0, self.ball, 10, leftSide=not self.mray, upperLim=81, lowerLim=42)
