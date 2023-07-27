import action
from numpy import *

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
        self.penaltyDefensive = False
        self.penaltyOffensive = False
        self.quadrant = 0
        self.alvo = 0

    def coach(self):
        """"Picks a strategy depending on the status of the field"""
        # For the time being, the only statuses considered are which side of the field the ball is in
        if self.penaltyDefensive == True:
            self.penaltyModeDefensive()
        elif self.penaltyOffensive == True:
            self.penaltyReto()
        else:
            if self.mray:
                if self.ball.xPos > 125:
                    self.wallStgDef()
                else:
                    self.wallStgAtt()
            else:
                if self.ball.xPos > 125:
                    self.wallStgAtt()
                else:
                    self.wallStgDef()

    def basicStgAtt2(self):
        if not self.mray:
            action.screenOutBall(self.robot1, self.ball, 105, leftSide=not self.mray, upperLim=85, lowerLim=5)
            action.screenOutBall(self.robot2, self.ball, 105, leftSide=not self.mray, upperLim=175, lowerLim=95)
            if self.ball.xPos < 40 and 60 < self.ball.yPos < 130:  # If the ball has inside of defense area
                action.defenderPenalty(self.robot0, self.ball,
                                             leftSide=not self.mray)  # Goalkeeper move ball away
            else:
                action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=115,
                                       lowerLim=65)  # Goalkeeper keeps in goal   
                action.ataque(self.ball,self.robot3,self.robot4,self.robotEnemy0,self.robotEnemy1,self.robotEnemy2,self.robotEnemy3,self.robotEnemy4)
        else:  # The same idea for other team
            action.screenOutBall(self.robot1, self.ball, 105, leftSide=not self.mray, upperLim=85, lowerLim=5)
            action.screenOutBall(self.robot2, self.ball, 105, leftSide=not self.mray, upperLim=175, lowerLim=95)
            if self.ball.xPos > 130 and 30 < self.ball.yPos < 110:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
            else:
                action.screenOutBall(self.robot0, self.ball, 14, leftSide=not self.mray, upperLim=115,
                                       lowerLim=65)
                action.Zagueiro(self.robot1,self.robot2,self.ball,45)
                action.ataque(self.ball,self.robot3,self.robot4,self.robotEnemy0,self.robotEnemy1,self.robotEnemy2,self.robotEnemy3,self.robotEnemy4)



    def basicStgDef(self):
        """Basic original strategy"""
        action.screenOutBall(self.robot3, self.ball, 150, leftSide=not self.mray, upperLim=85, lowerLim=5)
        action.screenOutBall(self.robot4, self.ball, 150, leftSide=not self.mray, upperLim=175, lowerLim=95)
        if not self.mray:
            if self.ball.xPos < 40 and self.ball.yPos > 50 and self.ball.yPos < 130:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
                action.screenOutBall(self.robot1, self.ball, 55, leftSide=not self.mray, upperLim=85, lowerLim=5)
                action.screenOutBall(self.robot2, self.ball, 55, leftSide=not self.mray, upperLim=175, lowerLim=95)
            else:
                #listRobots = [self.robot0, self.robot3, self.robot4, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4]
                friends = [self.robot0, self.robot3, self.robot4]
                enemys = [self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4]
                action.followLeader(self.robot0, self.robot1, self.robot2, self.ball, self.robotEnemy0, self.robotEnemy1,
                            self.robotEnemy2,self.robotEnemy3,self.robotEnemy4)
                action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
        else:
            if self.ball.xPos > 195 and self.ball.yPos > 50 and self.ball.yPos < 130:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
                action.screenOutBall(self.robot1, self.ball, 55, leftSide=not self.mray, upperLim=85, lowerLim=5)
                action.screenOutBall(self.robot2, self.ball, 55, leftSide=not self.mray, upperLim=175, lowerLim=95)
            else:
                #listRobots = [self.robot0, self.robot3, self.robot4, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4]
                friends = [self.robot0, self.robot3, self.robot4]
                enemys = [self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4]
                action.followLeader(self.robot0, self.robot1, self.robot2, self.ball, self.robotEnemy0, self.robotEnemy1,
                            self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
                action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
        if ((abs(self.robot0.theta) < deg2rad(10)) or (abs(self.robot0.theta) > deg2rad(170))) and (self.robot0.xPos < 25 or self.robot0.xPos > 225):
            self.robot0.contStopped += 1
        else:
            self.robot0.contStopped = 0


    def basicStgAtt(self):
        """Basic alternative strategy"""
        #listRobots = [self.robot0, self.robot1, self.robot2, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4]
        friends = [self.robot0, self.robot1, self.robot2]
        enemys = [self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4]
        action.followLeader(self.robot0, self.robot3, self.robot4, self.ball, self.robotEnemy0, self.robotEnemy1,
                            self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)

        action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
        action.screenOutBall(self.robot1, self.ball, 90, leftSide=not self.mray, upperLim=85, lowerLim=5)
        action.screenOutBall(self.robot2, self.ball, 90, leftSide=not self.mray, upperLim=175, lowerLim=95)


    def penaltyModeDefensive(self):
        '''Strategy to defend penalty situations'''
        action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)

        enemys = [self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4]
        friends = [self.robot0, self.robot2, self.robot3, self.robot4]
        action.shoot(self.robot1,self.ball,not self.mray,friends,enemys)

        friends = [self.robot0, self.robot1, self.robot3, self.robot4]
        action.shoot(self.robot2,self.ball,not self.mray,friends,enemys)

        if not self.mray:
            if self.ball.xPos >53 or self.ball.yPos < 60 or self.ball.yPos > 120:
                self.penaltyDefensive = False
        else:
            if self.ball.xPos < 182 or self.ball.yPos < 60 or self.ball.yPos > 100:
                self.penaltyDefensive = False

    def penaltyModeOffensiveSpin(self):
        '''Strategy to convert penalty offensive situations'''
        action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray)
        action.screenOutBall(self.robot1, self.ball, 90, leftSide=not self.mray, upperLim=85, lowerLim=5)

        enemys = [self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4]
        friends = [self.robot0, self.robot1, self.robot2, self.robot4]
        action.shoot(self.robot3,self.ball,not self.mray,friends,enemys)
        friends = [self.robot0, self.robot1, self.robot3, self.robot4]
        action.shoot(self.robot2,self.ball,not self.mray,friends,enemys)
        if not self.robot4.dist(self.ball) < 9:
            action.girar(self.robot4, 100, 100)
        else:
            if self.robot4.teamYellow:
                if self.robot4.yPos < 90:
                    action.girar(self.robot4, 0, 100)
                else:
                    action.girar(self.robot4, 100, 0)
            else:
                if self.robot4.yPos > 90:
                    action.girar(self.robot4, 0, 100)
                else:
                    action.girar(self.robot4, 100, 0)
        if sqrt((self.ball.xPos-self.robot4.xPos)**2+(self.ball.yPos-self.robot4.yPos)**2) > 30:
            self.penaltyOffensive = False

    def basicStgAtt3(self):
        """Basic alternative strategy"""
        #listRobots = [self.robot0, self.robot1, self.robot2, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4]
        friends = [self.robot0, self.robot1, self.robot2]
        enemys = [self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4]
        action.ataque(self.ball, self.robot3, self.robot4, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
        action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
       # action.screenOutBall(self.robot1, self.ball, 105, leftSide=not self.mray, upperLim=85, lowerLim=5)
        #action.screenOutBall(self.robot2, self.ball, 105, leftSide=not self.mray, upperLim=175, lowerLim=95)
        if not self.mray:
            action.Zagueiro(self.robot1,self.robot2,self.ball,45)
        else:
            action.Zagueiro(self.robot1,self.robot2,self.ball,45)
        

    def wallStgAtt(self):
        action.ataque(self.ball, self.robot3, self.robot4, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
        action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
        action.defenderWall(self.robot1, self.robot2,self.ball, leftSide=not self.mray)

    def breakWallStgAtt(self):
        if self.mray and self.ball.xPos > 130 or not self.mray and self.ball.xPos < 120 or self.quadrant == 0:
            self.quadrant = 0
            action.ataque(self.ball, self.robot3, self.robot4, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
            action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
            action.defenderWall(self.robot1, self.robot2,self.ball, leftSide=not self.mray)
        
        if self.mray and self.ball.xPos < 80 and self.ball.yPos < 35 and self.quadrant != 2 or self.quadrant == 3:
            self.quadrant = 3
        if self.mray and self.ball.xPos < 80 and self.ball.yPos > 145 and self.quadrant != 3 or self.quadrant == 2:
            self.quadrant = 2
        if not self.mray and self.ball.xPos > 170 and self.ball.yPos < 35 and self.quadrant != 1 or self.quadrant == 4:
            self.quadrant = 4
        if not self.mray and self.ball.xPos > 170 and self.ball.yPos > 145 and self.quadrant != 4 or self.quadrant == 1:
            self.quadrant = 1

        if self.quadrant != 0:
            action.ataque(self.ball, self.robot2, self.robot3, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
            action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
            action.defenderWallSolo(self.robot1, self.ball, leftSide=not self.mray)
            action.breakWall(self.robot4, self.ball, self.quadrant,self.robot0, self.robot1, self.robotEnemy0, self.robotEnemy1,
                                                                                 self.robotEnemy2, self.robotEnemy3, self.robotEnemy4,
                                                                                 leftSide=not self.mray)

    #Ainda não funciona direito
    def agressiveBreakWallStgAtt(self):
        if self.mray and self.ball.xPos > 90 or not self.mray and self.ball.xPos < 140 or self.quadrant == 0:
            self.quadrant = 0
            self.alvo = 0
        if self.mray and self.ball.xPos < 70 and self.ball.yPos < 25 and self.quadrant != 2 or self.quadrant == 3:
            self.quadrant = 3
            self.alvo = 2
        if self.mray and self.ball.xPos < 70 and self.ball.yPos > 155 and self.quadrant != 3 or self.quadrant == 2:
            self.quadrant = 2
            self.alvo = 3
        if not self.mray and self.ball.xPos > 180 and self.ball.yPos < 25 and self.quadrant != 1 or self.quadrant == 4:
            self.quadrant = 4
            self.alvo = 1
        if not self.mray and self.ball.xPos > 180 and self.ball.yPos > 155 and self.quadrant != 4 or self.quadrant == 1:
            self.quadrant = 1
            self.alvo = 4
        if self.alvo != 0:
            action.ataque(self.ball, self.robot2, self.robot3, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
        else:
            action.ataque(self.ball, self.robot2, self.robot3, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
        action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
        action.defenderWallSolo(self.robot1, self.ball, leftSide=not self.mray)
        action.breakWall(self.robot4, self.ball, self.quadrant,self.robot0, self.robot1, self.robotEnemy0, self.robotEnemy1,
                                                                                self.robotEnemy2, self.robotEnemy3, self.robotEnemy4,
                                                                                leftSide=not self.mray)


    def wallStgDef(self):
        action.defesa_atacantes(self.ball, self.robot0, self.robot1, self.robot2, self.robot3, self.robot4, 
                                self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
        """ Wall defense using two defenders"""
        if not self.mray:
            if self.ball.xPos < 40 and self.ball.yPos > 60 and self.ball.yPos < 130:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
            else:
                action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)           
        else:
            if self.ball.xPos > 215 and self.ball.yPos > 60 and self.ball.yPos < 130:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
            else:
                action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
        action.defenderWall(self.robot1, self.robot2,self.ball, leftSide=not self.mray)
        
    def penaltyReto(self):
        '''Strategy to convert penalty offensive situations'''
        action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray)
        action.screenOutBall(self.robot1, self.ball, 90, leftSide=not self.mray, upperLim=85, lowerLim=5)
        action.shoot_penalty(self.robot3, self.ball, leftSide=not self.mray)
        action.shoot_penalty(self.robot4, self.ball, leftSide=not self.mray)

        if sqrt((self.ball.xPos-self.robot4.xPos)**2+(self.ball.yPos-self.robot4.yPos)**2) > 30:
            self.penaltyOffensive = False

    def penaltyReto(self):
        '''Strategy to convert penalty offensive situations'''
        action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray)
        action.screenOutBall(self.robot1, self.ball, 90, leftSide=not self.mray, upperLim=85, lowerLim=5)

        action.girar(self.robot4, -200, 200)

        action.shoot_penalty(self.robot3, self.ball, leftSide=not self.mray)


        if sqrt((self.ball.xPos-self.robot4.xPos)**2+(self.ball.yPos-self.robot4.yPos)**2) > 30:
            self.penaltyOffensive = False

    def basicStgDef2(self):
        action.defesa_atacantes(self.ball, self.robot0, self.robot1, self.robot2, self.robot3, self.robot4, 
                                self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
        if not self.mray:
            if self.ball.xPos < 40 and 60 < self.ball.yPos < 130:  # If the ball has inside of defense area
                action.defenderPenalty(self.robot0, self.ball,
                                             leftSide=not self.mray)  # Goalkeeper move ball away
            else:
                action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110,
                                       lowerLim=70)  # Goalkeeper keeps in goal
                action.Zagueiro(self.robot1,self.robot2,self.ball,50)
                #action.defesa_atacantes(self.ball, self.robot0, self.robot1, self.robot2, self.robot3, self.robot4, 
                #                self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
        else:  # The same idea for other team
            if self.ball.xPos > 215 and 60 < self.ball.yPos < 130:
                action.defenderPenalty(self.robot0, self.ball, leftSide=not self.mray)
            else:
                action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=115,
                                       lowerLim=65)
                action.Zagueiro(self.robot1,self.robot2,self.ball,50)

    def penalty_mode_offensive_spin(self):
        """Input: None
        Description: Penalty kick offence strategy with spin.
        Output: None."""
        #ball_coordinates = self.ball.get_coordinates()
        #robot_coordinates = self.robots[2].get_coordinates()
        action.screenOutBall(self.robot0, self.ball, 10, leftSide=not self.mray)  # Goalkeeper keeps in defense
        action.shoot(self.robot1, self.ball, leftSide=not self.mray)  # Defender going to the rebound

        if not self.robot4.dist(self.ball) < 9:  # If the attacker is not closer to the ball
            action.girar(self.robot4, 100, 100)  # Moving forward
        else:
            if self.robot4.teamYellow:  # Team verification
                if self.robot4.yPos < 65:
                    action.girar(self.robot4, 0, 100)  # Shoots the ball spinning up
                else:
                    action.girar(self.robot4, 100, 0)  # Shoots the ball spinning down
            else:
                if self.robot2.yPos > 65:
                    action.girar(self.robot4, 0, 100)  # Shoots the ball spinning down
                else:
                    action.girar(self.robot4, 100, 0)  # Shoots the ball spinning up
        if sqrt((self.ball.xPos-self.robot4.xPos)**2+(self.ball.yPos-self.robot4.yPos)**2) > 30:
             self.penaltyOffensive = False


