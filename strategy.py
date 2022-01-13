import action
from numpy import *

"""
Input: Friendly robots, enemy robots, ball, side of field, strategy object.
Description: This class contains all functions and objects related to selecting a game strategy.
Output: None
"""

class Strategy:
    def __init__(self, robot0, robot1, robot2, robot_enemy_0, robot_enemy_1, robot_enemy_2, ball, mray, strategy):
        self.robot0 = robot0
        self.robot1 = robot1
        self.robot2 = robot2
        self.robotEnemy0 = robot_enemy_0
        self.robotEnemy1 = robot_enemy_1
        self.robotEnemy2 = robot_enemy_2
        self.ball = ball
        self.mray = mray
        self.penaltyDefensive = False
        self.penaltyOffensive = False
        self.strategy = strategy
        
    """
    Input: None
    Description: Calls the function that initiates the selected strategy.
    Output: Prints a warning in case of error.
    """
    def decider(self):
        if self.strategy == 'default':
            self.coach()
        elif self.strategy == 'twoAttackers':
            self.coach2()
        else:
            print("Algo deu errado na seleção de estratégias")
    """
    Input: None
    Description: Advanced strategy, one goalkeeper defends while two robots chase the ball, with one leading and the other in support.
    Output: None.
    """
    def coach2(self):
        """Picks a strategy depending on the status of the field"""
        # For the time being, the only statuses considered are which side of the field the ball is in
        if self.penaltyDefensive:
            self.penalty_mode_defensive()
        elif self.penaltyOffensive:
            self.penalty_mode_offensive_spin()
        else:
            if self.mray:
                if self.ball.xPos > 85:
                    self.stg_def_v2()
                else:
                    self.stg_att_v2()
            else:
                if self.ball.xPos > 85:
                    self.stg_att_v2()
                else:
                    self.stg_def_v2()
    """
    Input: None
    Description: The standard strategy, one robot as attacker, another as defender and another as goalkeeper.
    Output: None.
    """
    def coach(self):
        """Picks a strategy depending on the status of the field"""
        # For the time being, the only statuses considered are which side of the field the ball is in
        if self.penaltyDefensive:
            self.penalty_mode_defensive()
        elif self.penaltyOffensive:
            self.penalty_mode_offensive_spin()
        else:
            if self.mray:
                if self.ball.xPos > 85:
                    self.basic_stg_def_2()
                else:
                    self.basic_stg_att()
            else:
                if self.ball.xPos > 85:
                    self.basic_stg_att()
                else:
                    self.basic_stg_def_2()

    """
    Input: None
    Description: Basic defence strategy, goalkeeper blocks goal, defender chases ball, attacker holds in midfield.
    Output: None.
    """               
    def basic_stg_def(self):
        """Basic original strategy with goalkeeper advance"""
        if not self.mray:
            if self.ball.xPos < 30 and 30 < self.ball.yPos < 110:
                action.defender_penalty(self.robot0, self.ball, left_side=not self.mray)
                action.screen_out_ball(self.robot1, self.ball, 55, left_side=not self.mray)
            else:
                action.shoot(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot2,
                             enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
                action.screen_out_ball(self.robot0, self.ball, 14, left_side=not self.mray, upper_lim=81, lower_lim=42)
        else:
            if self.ball.xPos > 130 and 30 < self.ball.yPos < 110:
                action.defender_penalty(self.robot0, self.ball, left_side=not self.mray)
                action.screen_out_ball(self.robot1, self.ball, 55, left_side=not self.mray)
            else:
                action.shoot(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot2,
                             enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
                action.screen_out_ball(self.robot0, self.ball, 14, left_side=not self.mray, upper_lim=81, lower_lim=42)
        action.screen_out_ball(self.robot2, self.ball, 110, left_side=not self.mray, upper_lim=120, lower_lim=10)
    
    """
    Input: None
    Description: Basic attack strategy, goalkeeper blocks goal, defender screens midfield, attacker chases ball.
    Output: None.
    """
    def basic_stg_att(self):
        """Basic alternative strategy"""
        action.defender_spin(self.robot2, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot1,
                             enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        action.screen_out_ball(self.robot1, self.ball, 60, left_side=not self.mray, upper_lim=120, lower_lim=10)
        action.screen_out_ball(self.robot0, self.ball, 14, left_side=not self.mray, upper_lim=81, lower_lim=42)
    
    """
    Input: None
    Description: Basic attack strategy, goalkeeper blocks goal and advances towards ball to defend, defender screens midfield, attacker chases ball.
    Output: None.
    """
    def basic_stg_def_2(self):
        """Basic original strategy with goalkeeper advance and spin"""
        if not self.mray:
            if self.ball.xPos < 40 and 30 < self.ball.yPos < 110:
                action.defender_penalty(self.robot0, self.ball, leftSide=not self.mray)
                action.screen_out_ball(self.robot1, self.ball, 55, left_side=not self.mray)
            else:
                action.defender_spin(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0,
                                     friend2=self.robot2,
                                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
                action.screen_out_ball(self.robot0, self.ball, 14, left_side=not self.mray, upper_lim=81, lower_lim=42)
        else:
            if self.ball.xPos > 130 and 30 < self.ball.yPos < 110:
                action.defender_penalty(self.robot0, self.ball, leftSide=not self.mray)
                action.screen_out_ball(self.robot1, self.ball, 55, left_side=not self.mray)
            else:
                action.defender_spin(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0,
                                     friend2=self.robot2,
                                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
                action.screen_out_ball(self.robot0, self.ball, 14, left_side=not self.mray, upper_lim=81, lower_lim=42)
        action.screen_out_ball(self.robot2, self.ball, 110, left_side=not self.mray, upper_lim=120, lower_lim=10)
        if ((abs(self.robot0.theta) < deg2rad(10)) or (abs(self.robot0.theta) > deg2rad(170))) and (
                self.robot0.xPos < 20 or self.robot0.xPos > 150):
            self.robot0.contStopped += 1
        else:
            self.robot0.contStopped = 0
    
    
    """
    Input: None
    Description: Defence part of master-slave method, one robot leads chasing ball, another supports, goalkeeper blocks goal.
    Output: None.
    """
    def stg_def_v2(self):
        """Strategy with 2 robots moving with Master-Slave in defensive side"""
        if not self.mray:
            if self.ball.xPos < 40 and 30 < self.ball.yPos < 110:
                action.defender_penalty(self.robot0, self.ball, left_side=not self.mray)
                self.two_attackers()
            else:
                self.two_attackers()
                action.screen_out_ball(self.robot0, self.ball, 16, left_side=not self.mray, upper_lim=84, lower_lim=42)
        else:
            if self.ball.xPos > 130 and 30 < self.ball.yPos < 110:
                action.defender_penalty(self.robot0, self.ball, left_side=not self.mray)
                self.two_attackers()
            else:
                self.two_attackers()
                action.screen_out_ball(self.robot0, self.ball, 16, left_side=not self.mray, upper_lim=84, lower_lim=42)

        if ((abs(self.robot0.theta) < deg2rad(10)) or (abs(self.robot0.theta) > deg2rad(170))) and (
                self.robot0.xPos < 20 or self.robot0.xPos > 150):
            self.robot0.contStopped += 1
        else:
            self.robot0.contStopped = 0
    
    """
    Input: None
    Description: Offence part of master-slave method, one robot leads chasing ball, another supports, goalkeeper blocks goal.
    Output: None.
    """
    def stg_att_v2(self):
        """Strategy with 2 robots moving with Master-Slave in offensive side"""
        self.two_attackers()
        action.screen_out_ball(self.robot0, self.ball, 16, left_side=not self.mray, upper_lim=84, lower_lim=42)
        self.robot0.contStopped = 0
    
    """
    Input: None
    Description: Penalty kick defence strategy, goalkeeper defends goal, other robots chase ball.
    Output: None.
    """
    def penalty_mode_defensive(self):
        """Strategy to defend penalty situations"""
        action.defender_penalty(self.robot0, self.ball, left_side=not self.mray, friend1=self.robot1,
                                friend2=self.robot2,
                                enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        action.shoot(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot2,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        action.shoot(self.robot2, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot1,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        if not self.mray:
            if self.ball.xPos > 48 or self.ball.yPos < 30 or self.ball.yPos > 100:
                self.penaltyDefensive = False
        else:
            if self.ball.xPos < 112 or self.ball.yPos < 30 or self.ball.yPos > 100:
                self.penaltyDefensive = False
    """
    Input: None
    Description: Penalty kick offence strategy.
    Output: None.
    # TODO: perguntar uma descrição dessa bagaça 
    """
    def penalty_mode_offensive(self):
        """Strategy to convert penalty offensive situations"""
        action.screen_out_ball(self.robot0, self.ball, 10, left_side=not self.mray)
        action.shoot(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot2,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        action.attack_penalty(self.robot2, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot1,
                              enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        if sqrt((self.ball.xPos - self.robot2.xPos) ** 2 + (self.ball.yPos - self.robot2.yPos) ** 2) > 20:
            self.penaltyOffensive = False
    """
    Input: None
    Description: Penalty kick offence strategy.
    Output: None.
    # TODO: perguntar uma descrição dessa bagaça 
    """
    def penalty_mode_offensive_spin(self):
        """Strategy to convert penalty offensive situations"""
        action.screen_out_ball(self.robot0, self.ball, 10, left_side=not self.mray)
        action.shoot(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot2,
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
        if sqrt((self.ball.xPos - self.robot2.xPos) ** 2 + (self.ball.yPos - self.robot2.yPos) ** 2) > 30:
            self.penaltyOffensive = False
    """
    Input: None
    Description: Calls leader and follower technique for use in strategies.
    Output: None.
    # TODO: perguntar uma descrição dessa bagaça 
    """
    def two_attackers(self):
        """Strategy to move 2 robots at same time with Master-Slave"""
        action.followLeader(self.robot0, self.robot1, self.robot2, self.ball, self.robotEnemy0, self.robotEnemy1,
                            self.robotEnemy2)
