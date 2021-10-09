import action
from numpy import *

class Strategy:
    def __init__(self, robot0, robot1, robot2, robotEnemy0, robotEnemy1, robotEnemy2, ball, mray, strategy):
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
        self.strategy = strategy

    def decider(self):
        if self.strategy == 'default':
            self.coach()
        elif self.strategy == 'twoAttackers':
            self.coach2()
        else:
            print("Algo deu errado na seleção de estratégias")

    def coach2(self):
        """Picks a strategy depending on the status of the field"""
        # For the time being, the only statuses considered are which side of the field the ball is in
        if self.penaltyDefensive == True:
            self.penaltyModeDefensive()
        elif self.penaltyOffensive == True:
            self.penaltyModeOffensiveSpin()
        else:
            if self.mray:
                if self.ball.xPos > 85:
                    self.StgDef_V2()
                else:
                    self.StgAtt_V2()
            else:
                if self.ball.xPos > 85:
                    self.StgAtt_V2()
                else:
                    self.StgDef_V2()

    def coach(self):
        """Picks a strategy depending on the status of the field"""
        # For the time being, the only statuses considered are which side of the field the ball is in
        if self.penaltyDefensive == True:
            self.penaltyModeDefensive()
        elif self.penaltyOffensive == True:
            self.penaltyModeOffensiveSpin()
        else:
            if self.mray:
                if self.ball.xPos > 85:
                    self.basicStgDef2()
                else:
                    self.basicStgAtt()
            else:
                if self.ball.xPos > 85:
                    self.basicStgAtt()
                else:
                    self.basicStgDef2()

    def basicStgDef(self):
        """Basic original strategy with goalkeeper advance"""
        if not self.mray:
            if self.ball.xPos < 30 and self.ball.yPos > 30 and self.ball.yPos < 110:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
                action.screenOutBall(self.robot1, self.ball, 55, leftSide=not self.mray)
            else:
                action.shoot(self.robot1, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot2,
                             enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
                action.screenOutBall(self.robot0, self.ball, 14, leftSide=not self.mray, upperLim=81, lowerLim=42)
        else:
            if self.ball.xPos > 130 and self.ball.yPos > 30 and self.ball.yPos < 110:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
                action.screenOutBall(self.robot1, self.ball, 55, leftSide=not self.mray)
            else:
                action.shoot(self.robot1, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot2,
                             enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
                action.screenOutBall(self.robot0, self.ball, 14, leftSide=not self.mray, upperLim=81, lowerLim=42)
        action.screenOutBall(self.robot2, self.ball, 110, leftSide=not self.mray, upperLim=120, lowerLim=10)

    def basicStgAtt(self):
        """Basic alternative strategy"""
        action.defenderSpin(self.robot2, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot1,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        action.screenOutBall(self.robot1, self.ball, 60, leftSide=not self.mray, upperLim=120, lowerLim=10)
        action.screenOutBall(self.robot0, self.ball, 14, leftSide=not self.mray, upperLim=81, lowerLim=42)

    def basicStgDef2(self):
        """Basic original strategy with goalkeeper advance and spin"""
        if not self.mray:
            if self.ball.xPos < 40 and self.ball.yPos > 30 and self.ball.yPos < 110:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
                action.screenOutBall(self.robot1, self.ball, 55, leftSide=not self.mray)
            else:
                action.defenderSpin(self.robot1, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot2,
                             enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
                action.screenOutBall(self.robot0, self.ball, 14, leftSide=not self.mray, upperLim=81, lowerLim=42)
        else:
            if self.ball.xPos > 130 and self.ball.yPos > 30 and self.ball.yPos < 110:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
                action.screenOutBall(self.robot1, self.ball, 55, leftSide=not self.mray)
            else:
                action.defenderSpin(self.robot1, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot2,
                             enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
                action.screenOutBall(self.robot0, self.ball, 14, leftSide=not self.mray, upperLim=81, lowerLim=42)
        action.screenOutBall(self.robot2, self.ball, 110, leftSide=not self.mray, upperLim=120, lowerLim=10)
        if ((abs(self.robot0.theta) < deg2rad(10)) or (abs(self.robot0.theta) > deg2rad(170))) and (self.robot0.xPos < 20 or self.robot0.xPos > 150):
            self.robot0.contStopped += 1
        else:
            self.robot0.contStopped = 0
        print(self.robot0.contStopped)

    def StgDef_V2(self):
        """Strategy with 2 robots moving with Master-Slave in defensive side"""
        if not self.mray:
            if self.ball.xPos < 40 and self.ball.yPos > 30 and self.ball.yPos < 110:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
                self.twoAttackers()
            else:
                self.twoAttackers()
                action.screenOutBall(self.robot0, self.ball, 16, leftSide=not self.mray, upperLim=84, lowerLim=42)
        else:
            if self.ball.xPos > 130 and self.ball.yPos > 30 and self.ball.yPos < 110:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
                self.twoAttackers()
            else:
                self.twoAttackers()
                action.screenOutBall(self.robot0, self.ball, 16, leftSide=not self.mray, upperLim=84, lowerLim=42)

        if ((abs(self.robot0.theta) < deg2rad(10)) or (abs(self.robot0.theta) > deg2rad(170))) and (self.robot0.xPos < 20 or self.robot0.xPos > 150):
            self.robot0.contStopped += 1
        else:
            self.robot0.contStopped = 0
        print(self.robot0.contStopped)

    def StgAtt_V2(self):
        """Strategy with 2 robots moving with Master-Slave in offensive side"""
        self.twoAttackers()
        action.screenOutBall(self.robot0, self.ball,16, leftSide=not self.mray, upperLim=84, lowerLim=42)

    def stgFullAtt(self):
        """Crazy test attack strategy"""
        action.shoot(self.robot2, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot1,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        action.shoot(self.robot1, self.ball, leftSide=not self.mray, friend1=self.robot1, friend2=self.robot2,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        action.screenOutBall(self.robot0, self.ball, 10, leftSide=not self.mray)

    def penaltyModeDefensive(self):
        '''Strategy to defend penalty situations'''
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
        '''Strategy to convert penalty offensive situations'''
        action.screenOutBall(self.robot0, self.ball, 10, leftSide=not self.mray)
        action.shoot(self.robot1, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot2,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        action.attackPenalty(self.robot2, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot1,
                 enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        if sqrt((self.ball.xPos-self.robot2.xPos)**2+(self.ball.yPos-self.robot2.yPos)**2) > 20:
            self.penaltyOffensive = False

    def penaltyModeOffensiveSpin(self):
        '''Strategy to convert penalty offensive situations'''
        action.screenOutBall(self.robot0, self.ball, 10, leftSide=not self.mray)
        action.shoot(self.robot1, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot2,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        if not self.robot2.dist(self.ball) < 9:
            action.girar(self.robot2, 100, 100)
        else:
            if self.robot2.teamYellow:
                if self.robot2.yPos < 65:
                    action.girar(self.robot2, 0, 100)
                else:
                    action.girar(self.robot2, 100, 0)
            else:
                if self.robot2.yPos > 65:
                    action.girar(self.robot2, 0, 100)
                else:
                    action.girar(self.robot2, 100, 0)
        if sqrt((self.ball.xPos-self.robot2.xPos)**2+(self.ball.yPos-self.robot2.yPos)**2) > 30:
            self.penaltyOffensive = False

    def twoAttackers(self):
        '''Strategy to move 2 robots at same time with Master-Slave'''
        action.Master_Slave(self.robot0, self.robot1,self.robot2, self.ball, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2)
