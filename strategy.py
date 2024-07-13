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

    def coach(self, selectedStrategy):
        """"Picks a strategy depending on the status of the field"""
        # For the time being, the only statuses considered are which side of the field the ball is in
        if self.penaltyDefensive == True:
            self.penaltyModeDefensive()
        elif self.penaltyOffensive == True:
            #self.penaltyReto()
            self.penaltyModeOffensiveSpin()
            #self.penaltyModeOffensiveNewSpin()
        else: # If the game is not in penalty mode
            if selectedStrategy == "blockingWallDeffense":
                self.breakWallStgAtt()
            elif selectedStrategy == "wallDeffenseDefault":
                self.wallDeffenseDefault()
            elif selectedStrategy == "default5v5":
                self.basicStg()
            elif selectedStrategy == "tripleAttack":
                self.tripleAttack()
            elif selectedStrategy == "breakWallAtaque":
                self.breakWallAtaque()
            elif selectedStrategy == "breakWallZaga":
                self.breakWallZaga()
            elif selectedStrategy == "pivAla":
                self.grid_field()
            else:
                self.basicStg()

    def grid_field(self):
        self.defensive_up = False
        self.defensive_down = False
        self.defensive_center = False
        self.offensive_up = False
        self.offensive_down = False
        self.offensive_center = False

        self.pivo = self.robot4
        self.ala_esquerdo = self.robot3
        self.ala_direito = self.robot2
        self.zagueiro = self.robot1
        self.goleiro = self.robot0

        # TODO: fazer para o amarelo
        if self.mray:
            if self.ball.xPos > 130:
                action.defesa_atacantes(self.ball, self.robot0, self.robot1, self.robot4, self.robot3, self.robot2, 
                                self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
    
            else:
                if self.ball.yPos > 130:
                    self.offensive_up = True
                elif self.ball.yPos < 50:
                    self.offensive_down = True
                else:
                    self.offensive_center = True
                self.ala_esquerdo_strategy()
                self.ala_direito_strategy()
        else:
            if self.ball.xPos > 120:
                if self.ball.yPos > 130:
                    self.offensive_up = True
                elif self.ball.yPos < 50:
                    self.offensive_down = True
                else:
                    self.offensive_center = True

                self.ala_esquerdo_strategy()
                self.ala_direito_strategy()
            else:
                action.defesa_atacantes(self.ball, self.robot0, self.robot1, self.robot4, self.robot3, self.robot2, 
                                self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
                
        
    
        self.pivo_strategy()
        action.defenderWall(self.robot0, self.robot1,self.ball, leftSide=not self.mray)
        #self.zagueiro_strategy()
        #self.goleiro_strategy()

    def pivo_strategy(self):

        if not self.mray and self.ball.xPos > 205 and self.ball.yPos > 65 and self.ball.yPos < 115 or self.mray and self.ball.xPos < 45 and self.ball.yPos > 65 and self.ball.yPos < 115:
            action.shoot(self.robot4, self.ball, leftSide=not self.mray)
        else:
            action.breakWall(self.robot4, self.ball, self.quadrant,self.robot0, self.robot1, self.robotEnemy0, self.robotEnemy1,
                                                                                self.robotEnemy2, self.robotEnemy3, self.robotEnemy4,
                                                                                leftSide=not self.mray)
        """if self.offensive_center:
            action.defenderSpin(self.pivo, self.ball, left_side=not self.pivo.teamYellow, friend1=self.ala_esquerdo, friend2=self.ala_direito,
                                friend3=self.zagueiro, friend4=self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2,
                                enemy3=self.robotEnemy3, enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
        elif self.offensive_down or self.offensive_up:
            action.screenOutBall_diagonal(self.pivo,self.ball,leftSide=not self.pivo.teamYellow)
        else:
            action.screenOutBall_inverse(self.pivo, self.ball, 135, leftSide= not self.pivo.teamYellow, upperLim=130, lowerLim=50)
        """ 
        
    def ala_esquerdo_strategy(self):
        if self.mray:
            condition_idle_attack = self.ball.xPos < 50
            idle_point_attack_x, idle_point_attack_y, idle_point_attack_theta =  30, 120, -pi/2
            idle_point_midfield_x, idle_point_midfield_y, idle_point_midfield_theta =  90, 150, -pi

            condition_defense_toBall = self.ball.xPos > 200 

            condition_idle_deffense = self.ball.xPos > 200 and self.ball.yPos < 130
            idle_point_deffense_x, idle_point_deffense_y, idle_point_deffense_theta =  180, 150, 0
        else:
            condition_idle_attack = self.ball.xPos > 200
            idle_point_attack_x, idle_point_attack_y, idle_point_attack_theta =  220, 120, -pi/2
            idle_point_midfield_x, idle_point_midfield_y, idle_point_midfield_theta =  150, 150, 0

            condition_defense_toBall = self.ball.xPos < 50 

            condition_idle_deffense = self.ball.xPos < 50 and self.ball.yPos < 130
            idle_point_deffense_x, idle_point_deffense_y, idle_point_deffense_theta =  70, 150, 0


        if self.offensive_up:
            action.defenderSpin(self.ala_esquerdo, self.ball, left_side=not self.ala_esquerdo.teamYellow, friend1=self.pivo, friend2=self.ala_direito, 
                                friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            
        elif self.offensive_down:
            if condition_idle_attack:
                xPoint = idle_point_attack_x
                yPoint = idle_point_attack_y
                theta = idle_point_attack_theta
                action.go_to_point(self.ala_esquerdo, self.ball, xPoint, yPoint, theta, friend1=self.pivo, friend2=self.ala_direito, 
                                   friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                   enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            else:
                xPoint = idle_point_midfield_x
                yPoint = idle_point_midfield_y
                theta = idle_point_midfield_theta
                action.go_to_point(self.ala_esquerdo, self.ball, xPoint, yPoint, theta, friend1=self.pivo, friend2=self.ala_direito, 
                                   friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                   enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
                
        elif self.offensive_center:
            if self.ala_esquerdo.dist(self.ball) < 25:
                self.ala_esquerdo.spin = False
                action.defenderSpin(self.ala_esquerdo, self.ball, left_side=not self.ala_esquerdo.teamYellow, friend1=self.pivo, friend2=self.ala_direito, 
                                    friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                    enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            elif condition_idle_attack:
                xPoint = idle_point_attack_x
                yPoint = idle_point_attack_y
                theta = idle_point_attack_theta
                action.go_to_point(self.ala_esquerdo, self.ball, xPoint, yPoint, theta, friend1=self.pivo, friend2=self.ala_direito, 
                                   friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                   enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            else:
                action.go_to_point(self.ala_esquerdo, self.ball, self.pivo.xPos, self.pivo.yPos+40, 0, friend1=self.pivo, friend2=self.ala_direito, 
                                   friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                   enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
                
        elif self.defensive_up:
            if condition_idle_deffense:
                xPoint = idle_point_deffense_x
                yPoint = idle_point_deffense_y
                theta = idle_point_deffense_theta
                action.go_to_point(self.ala_esquerdo, self.ball, xPoint, yPoint, theta, friend1=self.pivo, friend2=self.ala_direito, 
                                   friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                   enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            elif condition_defense_toBall :
                action.defenderSpin(self.ala_esquerdo, self.ball, left_side=not self.ala_esquerdo.teamYellow, friend1=self.pivo, friend2=self.ala_direito, 
                                    friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                    enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            else:
                pass # Definido no follow leader do zagueiro

        elif self.defensive_center or self.defensive_down:
            if condition_defense_toBall:
                xPoint = idle_point_deffense_x
                yPoint = idle_point_deffense_y
                theta = idle_point_deffense_theta
                action.go_to_point(self.ala_esquerdo, self.ball, xPoint, yPoint, theta, friend1=self.pivo, friend2=self.ala_direito, 
                                friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            else:
                action.go_to_point(self.ala_esquerdo, self.ball, self.zagueiro.xPos, self.zagueiro.yPos+40, 0, friend1=self.pivo, friend2=self.ala_direito, 
                                friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
        else:
            self.ala_esquerdo.simSetVel2(0,0)

    def ala_direito_strategy(self):
        if self.mray:
            condition_idle_attack = self.ball.xPos < 50
            idle_point_attack_x, idle_point_attack_y, idle_point_attack_theta =  30, 60, pi/2
            idle_point_midfield_x, idle_point_midfield_y, idle_point_midfield_theta =  90, 30, -pi

            condition_defense_toBall = self.ball.xPos > 200 

            condition_idle_deffense = self.ball.xPos > 200 and self.ball.yPos < 130
            idle_point_deffense_x, idle_point_deffense_y, idle_point_deffense_theta =  180, 30, 0
        else:
            condition_idle_attack = self.ball.xPos > 200
            idle_point_attack_x, idle_point_attack_y, idle_point_attack_theta =  220, 60, -pi/2
            idle_point_midfield_x, idle_point_midfield_y, idle_point_midfield_theta =  150, 30, 0

            condition_defense_toBall = self.ball.xPos < 50

            condition_idle_deffense = self.ball.xPos < 50 and self.ball.yPos > 50
            idle_point_deffense_x, idle_point_deffense_y, idle_point_deffense_theta =  70, 30, 0

        if self.offensive_down:
            action.defenderSpin(self.ala_direito, self.ball, left_side=not self.ala_esquerdo.teamYellow, friend1=self.pivo, friend2=self.ala_esquerdo, 
                                friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
        elif self.offensive_up:
            if condition_idle_attack:
                xPoint = idle_point_attack_x
                yPoint = idle_point_attack_y
                theta = idle_point_attack_theta
                action.go_to_point(self.ala_direito, self.ball, xPoint, yPoint, theta, friend1=self.pivo, friend2=self.ala_esquerdo, 
                                   friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                   enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            else:
                xPoint = idle_point_midfield_x
                yPoint = idle_point_midfield_y
                theta = idle_point_midfield_theta
                action.go_to_point(self.ala_direito, self.ball, xPoint, yPoint, theta, friend1=self.pivo, friend2=self.ala_esquerdo, 
                                   friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                   enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
        elif self.offensive_center:
            if self.ala_direito.dist(self.ball) < 25:
                self.ala_direito.spin = False
                action.defenderSpin(self.ala_direito, self.ball, left_side=not self.ala_esquerdo.teamYellow, friend1=self.pivo, friend2=self.ala_esquerdo, 
                                friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            elif condition_idle_attack:
                xPoint = idle_point_attack_x
                yPoint = idle_point_attack_y
                theta = idle_point_attack_theta
                action.go_to_point(self.ala_direito, self.ball, xPoint, yPoint, theta, friend1=self.pivo, friend2=self.ala_esquerdo, 
                                   friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                   enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            else:
                action.go_to_point(self.ala_direito, self.ball, self.pivo.xPos, self.pivo.yPos-40, 0, friend1=self.pivo, friend2=self.ala_esquerdo, 
                                   friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                   enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
        elif self.defensive_down:
            if condition_idle_deffense:
                xPoint = idle_point_deffense_x
                yPoint = idle_point_deffense_y
                theta = idle_point_deffense_theta
                action.go_to_point(self.ala_direito, self.ball, xPoint, yPoint, theta, friend1=self.pivo, friend2=self.ala_esquerdo, 
                                   friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                   enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            elif self.ball.xPos < 50:
                action.defenderSpin(self.ala_direito, self.ball, left_side=not self.ala_esquerdo.teamYellow, friend1=self.pivo, friend2=self.ala_esquerdo, 
                                friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            else:
                pass # Definido no follow leader do zagueiro
        elif self.defensive_up or self.defensive_center:
            if condition_defense_toBall:
                xPoint = idle_point_deffense_x
                yPoint = idle_point_deffense_y
                theta = idle_point_deffense_theta
                action.go_to_point(self.ala_direito, self.ball, xPoint, yPoint, theta, friend1=self.pivo, friend2=self.ala_esquerdo, 
                                   friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                   enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            else:
                action.go_to_point(self.ala_direito, self.ball, self.zagueiro.xPos, self.zagueiro.yPos-40, 0, friend1=self.pivo, friend2=self.ala_esquerdo, 
                                    friend3=self.zagueiro, friend4 = self.goleiro, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                    enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
        else:
            self.ala_direito.simSetVel2(0,0)

    def zagueiro_strategy(self):
        if self.mray:
            condition_goalkeeper_area = self.ball.xPos > 220 and self.ball.yPos > 50 and self.ball.yPos < 130
            condition_defender_toBall = self.ball.xPos > 200
        else:
            condition_goalkeeper_area = self.ball.xPos < 30 and self.ball.yPos > 50 and self.ball.yPos < 130
            condition_defender_toBall = self.ball.xPos < 50

        if self.defensive_center:
            if condition_goalkeeper_area:
                action.screenOutBall(self.zagueiro, self.ball, 45, leftSide=not self.mray, upperLim=175, lowerLim=5)
            else:
                action.defenderSpin(self.zagueiro, self.ball, left_side=not self.ala_esquerdo.teamYellow, friend1=self.goleiro, friend2=self.ala_esquerdo, 
                                    friend3=self.ala_direito, friend4=self.pivo, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                    enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
        elif self.defensive_up:
            if condition_defender_toBall:
                action.defenderSpin(self.zagueiro, self.ball, left_side=not self.ala_esquerdo.teamYellow, friend1=self.goleiro, friend2=self.ala_esquerdo, 
                                    friend3=self.ala_direito, friend4=self.pivo, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                    enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            else:
                action.followLeader(self.goleiro, self.zagueiro, self.ala_esquerdo, self.ball, self.robotEnemy0, self.robotEnemy1,
                                self.robotEnemy2,self.robotEnemy3,self.robotEnemy4)
        elif self.defensive_down:
            if condition_defender_toBall:
                action.defenderSpin(self.zagueiro, self.ball, left_side=not self.ala_esquerdo.teamYellow, friend1=self.goleiro, friend2=self.ala_esquerdo, 
                                    friend3=self.ala_direito, friend4=self.pivo, enemy1=self.robotEnemy1, enemy2=self.robotEnemy2, enemy3=self.robotEnemy3, 
                                    enemy4=self.robotEnemy4, enemy5=self.robotEnemy0)
            else:
                action.followLeader(self.goleiro, self.zagueiro, self.ala_direito, self.ball, self.robotEnemy0, self.robotEnemy1,
                                self.robotEnemy2,self.robotEnemy3,self.robotEnemy4)
        elif self.offensive_center or self.offensive_down or self.offensive_up:
            action.screenOutBall(self.zagueiro, self.ball, 105, leftSide=not self.mray, upperLim=110, lowerLim=70)
        else:
            self.zagueiro.simSetVel2(0,0)

    def goleiro_strategy(self):
        if not self.mray:
            if self.ball.xPos < 40 and self.ball.yPos > 50 and self.ball.yPos < 130:
                action.defenderPenalty(self.goleiro, self.ball, leftSide=not self.mray)
            else:
                action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
        else:
            if self.ball.xPos > 195 and self.ball.yPos > 50 and self.ball.yPos < 130:
                action.defenderPenalty(self.goleiro, self.ball, leftSide=not self.mray)
            else:
                action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
        if ((abs(self.robot0.theta) < deg2rad(10)) or (abs(self.robot0.theta) > deg2rad(170))) and (self.robot0.xPos < 25 or self.robot0.xPos > 225):
            self.robot0.contStopped += 1
        else:
            self.robot0.contStopped = 0


    def breakWallAtaque(self):
        if self.mray:
            if self.ball.xPos < 125:
                self.breakWallStgAttFraco()
            else:
                self.wallStgDefAtaqueFraco()
        else:
            if self.ball.xPos < 125:
                self.wallStgDefAtaqueFraco()
            else:
                self.breakWallStgAttFraco()

    def breakWallZaga(self):
        if self.mray:
            if self.ball.xPos < 125:
                self.breakWallStgAttZagueiroLinha()
            else:
                self.wallStgDefZagueirOlinha()
        else:
            if self.ball.xPos < 125:
                self.wallStgDefZagueirOlinha()
            else:
                self.breakWallStgAttZagueiroLinha()

    def basicStg(self):
        if self.mray:
            if self.ball.xPos < 125:
                self.basicStgAtt()
            else:
                self.basicStgDef()
        else:
            if self.ball.xPos < 125:
                self.basicStgDef()
            else:
                self.basicStgAtt()

    def wallDeffenseDefault(self):
        if self.mray:
            if self.ball.xPos < 125:
                self.wallStgAtt()
            else:
                self.wallStgDef()
        else:
            if self.ball.xPos < 125:
                self.wallStgDef()
            else:
                self.wallStgAtt()

    def tripleAttack(self):
        if self.mray:
            if self.ball.xPos < 125:
                self.tripleStgAtt()
            else:
                self.basicStgDef()
        else:
            if self.ball.xPos < 125:
                self.basicStgDef()
            else:
                self.tripleStgAtt()


    #coloca 3 robos na função triple_ataque e o goleiro e o zagueiro fazem screenOut 
    def tripleStgAtt(self):
        action.triple_ataque(self.ball, self.robot2, self.robot3, self.robot4, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
        action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
        action.screenOutBall(self.robot1, self.ball, 105, leftSide=not self.mray, upperLim=175, lowerLim=95)

    #ataque básico segue o líder não utilizado
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

    #defesa original segue o líder
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

    #ataque segue o líder com dois robos, os e goleiro fazem screenOut
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

    def penaltyModeOffensiveNewSpin(self):
        if not self.robot4.teamYellow:
            action.girar(self.robot4,100,-100)
        else:
            action.girar(self.robot4,-100,100)
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
        
    #posição de ataque na estratégia de wall Deffense
    #o ataque utiliza o segue o líder espelhado e os zagueiros ficam na posição de barreira
    def wallStgAtt(self):
        action.ataque(self.ball, self.robot3, self.robot4, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
        action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
        action.defenderWall(self.robot1, self.robot2,self.ball, leftSide=not self.mray)

    #ataque com estratégia para quebrar defesa de barreira reovendo o goleiro
    #dois robos atacam normalmente e um terceiro fica parado na área adversária esperando a bola chegar perto para realizar um chute
    #os zagueiros ficam na estratégia de barreira
    def breakWallStgAtt(self):           
        if not self.mray and self.ball.xPos > 205 and self.ball.yPos > 65 and self.ball.yPos < 115 or self.mray and self.ball.xPos < 45 and self.ball.yPos > 65 and self.ball.yPos < 115:
            action.shoot(self.robot4, self.ball, leftSide=not self.mray)
        else:
            action.breakWall(self.robot4, self.ball, self.quadrant,self.robot0, self.robot1, self.robotEnemy0, self.robotEnemy1,
                                                                                self.robotEnemy2, self.robotEnemy3, self.robotEnemy4,
                                                                                leftSide=not self.mray)
        
        if self.mray and self.ball.xPos > 210 and self.ball.yPos > 65 and self.ball.yPos < 115 or not self.mray and self.ball.xPos < 40 and self.ball.yPos > 65 and self.ball.yPos < 115:
            action.defenderPenalty(self.robot3, self.ball, leftSide=not self.mray)
        else:
            action.defenderWall(self.robot1, self.robot2,self.ball, leftSide=not self.mray)

        action.ataque(self.ball, self.robot0, self.robot3, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)

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

    #posição de defesa da estratégia de barreira
    #fixa os zagueiros na posição e faz os atacantes voltarem para buscar a bola na área de defesa
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

    #estratégia de quebra de barreira removendo um dos atacantes
    #a zaga e o goleiro funcionam como a estratégia de barreira padrão
    #um robô fica parado na área esperando a bola e bloqueando a barreira
    #e outro robô fica tentando levar a bola ao gol
    def breakWallStgAttFraco(self):
        action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)
        action.defesa_atacante_solo(self.ball, self.robot0, self.robot1, self.robot2, self.robot3, self.robot4, 
                                self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
        if not self.mray and self.ball.xPos > 205 and self.ball.yPos > 65 and self.ball.yPos < 115 or self.mray and self.ball.xPos < 45 and self.ball.yPos > 65 and self.ball.yPos < 115:
            action.shoot(self.robot4, self.ball, leftSide=not self.mray)
        else:
            action.breakWall(self.robot4, self.ball, self.quadrant,self.robot0, self.robot1, self.robotEnemy0, self.robotEnemy1,
                                                                                self.robotEnemy2, self.robotEnemy3, self.robotEnemy4,
                                                                                leftSide=not self.mray)
        
        if self.mray and self.ball.xPos > 210 and self.ball.yPos > 65 and self.ball.yPos < 115 or not self.mray and self.ball.xPos < 40 and self.ball.yPos > 65 and self.ball.yPos < 115:
            action.defenderPenalty(self.robot3, self.ball, leftSide=not self.mray)
        else:
            action.defenderWall(self.robot1,self.robot2,self.ball, leftSide=not self.mray)

    #posição de defesa na estratégia de quebra de barreira utilizando um dos atacantes
    def wallStgDefAtaqueFraco(self):
        action.defesa_atacante_solo(self.ball, self.robot0, self.robot1, self.robot2, self.robot3, self.robot4, 
                                self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)


        if not self.mray and self.ball.xPos > 205 and self.ball.yPos > 65 and self.ball.yPos < 115 or self.mray and self.ball.xPos < 45 and self.ball.yPos > 65 and self.ball.yPos < 115:
            action.shoot(self.robot4, self.ball, leftSide=not self.mray)
        else:
            action.breakWall(self.robot4, self.ball, self.quadrant,self.robot0, self.robot1, self.robotEnemy0, self.robotEnemy1,
                                                                                self.robotEnemy2, self.robotEnemy3, self.robotEnemy4,
                                                                                leftSide=not self.mray)
        
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

    #posição de ataque na estratégia de quebra de barreira utilizando um dos zagueiros
    #o ataque funciona com dois robôs e um terceiro que foi removido da zaga
    #fica parado dentro da área adversária esperando a bola e bloquando a barreira
    def breakWallStgAttZagueiroLinha(self):
        action.screenOutBall(self.robot0, self.ball, 20, leftSide=not self.mray, upperLim=110, lowerLim=70)

        if not self.mray and self.ball.xPos > 205 and self.ball.yPos > 65 and self.ball.yPos < 115 or self.mray and self.ball.xPos < 45 and self.ball.yPos > 65 and self.ball.yPos < 115:
            action.shoot(self.robot4, self.ball, leftSide=not self.mray)
        else:
            action.breakWall(self.robot4, self.ball, self.quadrant,self.robot0, self.robot1, self.robotEnemy0, self.robotEnemy1,
                                                                                self.robotEnemy2, self.robotEnemy3, self.robotEnemy4,
                                                                                leftSide=not self.mray)
        
        if self.mray and self.ball.xPos > 210 and self.ball.yPos > 65 and self.ball.yPos < 115 or not self.mray and self.ball.xPos < 40 and self.ball.yPos > 65 and self.ball.yPos < 115:
            action.defenderPenalty(self.robot3, self.ball, leftSide=not self.mray)
        else:
            action.defenderWallSolo(self.robot2,self.ball, leftSide=not self.mray)
        action.ataque(self.ball, self.robot1, self.robot3, self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)

    #posição de defesa da estratégia de quebra de barreira utilizando um dos zagueiros
    def wallStgDefZagueirOlinha(self):
        action.defesa_atacante_solo(self.ball, self.robot0, self.robot1, self.robot2, self.robot3, self.robot4, 
                                self.robotEnemy0, self.robotEnemy1, self.robotEnemy2, self.robotEnemy3, self.robotEnemy4)
        

        if not self.mray and self.ball.xPos > 205 and self.ball.yPos > 65 and self.ball.yPos < 115 or self.mray and self.ball.xPos < 45 and self.ball.yPos > 65 and self.ball.yPos < 115:
            action.shoot(self.robot4, self.ball, leftSide=not self.mray)
        else:
            action.breakWall(self.robot4, self.ball, self.quadrant,self.robot0, self.robot1, self.robotEnemy0, self.robotEnemy1,
                                                                                self.robotEnemy2, self.robotEnemy3, self.robotEnemy4,
                                                                                leftSide=not self.mray)
        
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