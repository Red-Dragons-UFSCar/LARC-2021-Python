import action
from numpy import *


class Strategy:

    """Input: Friendly robots, enemy robots, ball, side of field, strategy object.
    Description: This class contains all functions and objects related to selecting a game strategy.
    Output: None"""

    def __init__(self, robots, enemy_robots, ball, mray, strategies):

        self.robots = robots
        self.enemy_robots = enemy_robots
        self.ball = ball
        self.mray = mray
        self.penaltyDefensive = False
        self.penaltyOffensive = False
        self.strategy = strategies[0]
        self.stOfensePenalty = strategies[1]
        self.stDefensePenalty = strategies[2]

    def decider(self):
        """Input: None
        Description: Calls the function that initiates the selected strategy.
        Output: Prints a warning in case of error."""
        if self.strategy == 'default':
            self.coach()
        elif self.strategy == 'twoAttackers':
            self.coach2()
        else:
            print("There was an error in strategy selection")

    def coach2(self):
        """Input: None
        Description: Advanced strategy, one goalkeeper defends while two robots chase the ball, with one leading and the other in support.
        Output: None."""
        if self.penaltyDefensive:
            self.penalty_mode_defensive()
        elif self.penaltyOffensive:
            self.penalty_mode_offensive()
        else:
            # For the time being, the only statuses considered are which side of the field the ball is in
            if self.mray:
                if self.ball.coordinates.X > 85:
                    self.stg_def_v2()
                else:
                    self.stg_att_v2()
            else:
                if self.ball.coordinates.X > 85:
                    self.stg_att_v2()
                else:
                    self.stg_def_v2()

    def coach(self):
        """Input: None
        Description: The standard strategy, one robot as attacker, another as defender and another as goalkeeper.
        Output: None."""
        if self.penaltyDefensive:
            self.penalty_mode_defensive()
        elif self.penaltyOffensive:
            self.penalty_mode_offensive_spin()
        else:
            # For the time being, the only statuses considered are which side of the field the ball is in
            if self.mray:
                if self.ball.coordinates.X > 85:
                    self.basic_stg_def_2()
                else:
                    self.basic_stg_att()
            else:
                if self.ball.coordinates.x > 85:
                    self.basic_stg_att()
                else:
                    self.basic_stg_def_2()

    def basic_stg_def(self):
        """Input: None
        Description: Basic defence strategy, goalkeeper blocks goal and advance in ball, defender chases ball, attacker holds in midfield.
        Output: None.
        """
        if not self.mray:
            if self.ball.coordinates.X < 30 and 30 < self.ball.coordinates.Y < 110: # If the ball has inside of defense area
                action.defender_penalty_direct(self.robots[0], self.ball, left_side=not self.mray) # Goalkeeper move ball away
                action.screen_out_ball(self.robots[1], self.ball, 55, left_side=not self.mray)
            else:
                action.shoot(self.robots[1], self.ball, left_side=not self.mray, friend1=self.robots[0], friend2=self.robots[2],
                             enemy1=self.enemy_robots[0], enemy2=self.enemy_robots[1], enemy3=self.enemy_robots[2]) # Defender chases ball
                action.screen_out_ball(self.robots[0], self.ball, 14, left_side=not self.mray, upper_lim=81,
                                       lower_lim=42)  # Goalkeeper keeps in goal
        else: # The same idea for other team
            if self.ball.coordinates.X > 130 and 30 < self.ball.coordinates.Y < 110:
                action.defender_penalty_direct(self.robots[0], self.ball, left_side=not self.mray)
                action.screen_out_ball(self.robots[1], self.ball, 55, left_side=not self.mray)
            else:
                action.shoot(self.robots[1], self.ball, left_side=not self.mray, friend1=self.robots[0], friend2=self.robots[2],
                             enemy1=self.enemy_robots[0], enemy2=self.enemy_robots[1], enemy3=self.enemy_robots[2])
                action.screen_out_ball(self.robots[0], self.ball, 14, left_side=not self.mray, upper_lim=81,
                                       lower_lim=42)

        action.screen_out_ball(self.robots[2], self.ball, 110, left_side=not self.mray, upper_lim=120,
                               lower_lim=10)  # Attacker stays in midfield

    def basic_stg_att(self):
        """Input: None
        Description: Basic attack strategy, goalkeeper blocks goal, defender screens midfield, attacker chases ball.
        Output: None."""
        action.defender_spin(self.robots[2], self.ball, left_side=not self.mray)  # Attacker behavior
        action.screen_out_ball(self.robots[1], self.ball, 60, left_side=not self.mray, upper_lim=120,
                               lower_lim=10)  # Defender behavior
        action.screen_out_ball(self.robots[0], self.ball, 14, left_side=not self.mray, upper_lim=81,
                               lower_lim=42)  # Goalkeeper behavior

    def basic_stg_def_2(self):
        """Input: None
        Description: Basic defense strategy with robot stop detection
        Output: None."""
        if not self.mray:
            if self.ball.coordinates.X < 40 and 30 < self.ball.coordinates.Y < 110: # If the ball has inside of defense area
                action.defender_penalty_direct(self.robots[0], self.ball, left_side=not self.mray) # Goalkeeper move ball away
                action.screen_out_ball(self.robots[1], self.ball, 55, left_side=not self.mray)
            else:
                action.defender_spin(self.robots[1], self.ball, left_side=not self.mray)  # Defender chases ball
                action.screen_out_ball(self.robots[0], self.ball, 14, left_side=not self.mray, upper_lim=81,
                                       lower_lim=42)  # Goalkeeper keeps in goal
        else: # The same idea for other team
            if self.ball.coordinates.X > 130 and 30 < self.ball.coordinates.Y < 110:
                action.defender_penalty_direct(self.robots[0], self.ball, left_side=not self.mray)
                action.screen_out_ball(self.robots[1], self.ball, 55, left_side=not self.mray)
            else:
                action.defender_spin(self.robots[1], self.ball, left_side=not self.mray)
                action.screen_out_ball(self.robots[0], self.ball, 14, left_side=not self.mray, upper_lim=81,
                                       lower_lim=42)

        action.screen_out_ball(self.robots[2], self.ball, 110, left_side=not self.mray, upper_lim=120,
                               lower_lim=10)  # Attacker stays in midfield

        # Verification if robot has stopped
        if ((abs(self.robots[0].coordinates.rotation) < deg2rad(10)) or (abs(self.robots[0].coordinates.rotation) > deg2rad(170))) and (
                self.robots[0].coordinates.X < 20 or self.robots[0].coordinates.X > 150):
            self.robots[0].contStopped += 1
        else:
            self.robots[0].contStopped = 0

    def stg_def_v2(self):
        """Input: None
        Description: Defence part of followleader method, a robot leads chasing ball, other supports, goalie blocks
             goal and move ball away when close to the goal
        Output: None."""
        if not self.mray:
            if self.ball.coordinates.X < 40 and 30 < self.ball.coordinates.Y < 110: # If the ball has inside of defense area
                action.defender_penalty_direct(self.robots[0], self.ball, left_side=not self.mray) # Goalkeeper move ball away
                self.two_attackers()
            else:
                self.two_attackers()
                action.screen_out_ball(self.robots[0], self.ball, 16, left_side=not self.mray, upper_lim=84,
                                       lower_lim=42)  # Goalkeeper keeps in goal
        else: # The same ideia, but for other team
            if self.ball.coordinates.X > 130 and 30 < self.ball.coordinates.Y < 110:
                action.defender_penalty_direct(self.robots[0], self.ball, left_side=not self.mray)
                self.two_attackers()
            else:
                self.two_attackers()
                action.screen_out_ball(self.robots[0], self.ball, 16, left_side=not self.mray, upper_lim=84,
                                       lower_lim=42)

        # Verification if robot has stopped
        if ((abs(self.robots[0].coordinates.rotation) < deg2rad(10)) or (abs(self.robots[0].coordinates.rotation) > deg2rad(170))) and (
                self.robots[0].coordinates.X < 20 or self.robots[0].coordinates.X > 150):
            self.robots[0].contStopped += 1
        else:
            self.robots[0].contStopped = 0

    def stg_att_v2(self):
        """Input: None
        Description: Offence part of followleader method, one robot leads chasing ball, another supports, goalkeeper blocks goal.
        Output: None."""
        self.two_attackers()
        action.screen_out_ball(self.robots[0], self.ball, 16, left_side=not self.mray, upper_lim=84, lower_lim=42)
        self.robots[0].contStopped = 0

    def penalty_mode_defensive(self):

        """Input: None
        Description: Penalty kick defence strategy, goalkeeper defends goal, other robots chase ball.
        Output: None."""
        
        if self.stDefensePenalty == 'spin':
            action.defender_penalty_spin(self.robots[0], self.ball, left_side=not self.mray, friend1=self.robots[1],
                                    friend2=self.robots[2],
                                    enemy1=self.enemy_robots[0], enemy2=self.enemy_robots[1], enemy3=self.enemy_robots[2]) # Goalkeeper behaviour in defensive penalty
        elif self.stDefensePenalty == 'direct':
            action.defender_penalty_direct(self.robots[0], self.ball, left_side=not self.mray, friend1=self.robots[1],
                                    friend2=self.robots[2],
                                    enemy1=self.enemy_robots[0], enemy2=self.enemy_robots[1], enemy3=self.enemy_robots[2]) # Goalkeeper behaviour in defensive penalty


        action.shoot(self.robots[1], self.ball, left_side=not self.mray, friend1=self.robots[0], friend2=self.robots[2],
                     enemy1=self.enemy_robots[0], enemy2=self.enemy_robots[1], enemy3=self.enemy_robots[2]) # Robot 1 chasing ball
        action.shoot(self.robots[2], self.ball, left_side=not self.mray, friend1=self.robots[0], friend2=self.robots[1],
                     enemy1=self.enemy_robots[0], enemy2=self.enemy_robots[1], enemy3=self.enemy_robots[2]) # Robot 2 chasing ball

        # If the ball gets away from the defensive area, stops the penalty mode
        if not self.mray:
            if self.ball.coordinates.X > 48 or self.ball.coordinates.Y < 30 or self.ball.coordinates.Y > 100:
                self.penaltyDefensive = False
        else:
            if self.ball.coordinates.X < 112 or self.ball.coordinates.Y < 30 or self.ball.coordinates.Y > 100:
                self.penaltyDefensive = False

    def penalty_mode_offensive(self):
        """Input: None
        Description: Penalty kick offence strategy.
        Output: None."""
        action.screen_out_ball(self.robots[0], self.ball, 10, left_side=not self.mray)  # Goalkeeper keeps in goal
        action.shoot(self.robots[1], self.ball, left_side=not self.mray, friend1=self.robots[0], friend2=self.robots[2],
                     enemy1=self.enemy_robots[0], enemy2=self.enemy_robots[1], enemy3=self.enemy_robots[2]) # Defender going to the rebound
        #action.attack_penalty(self.robots[2], self.ball, leftSide=not self.mray, friend1=self.robots[0], friend2=self.robots[1],
        #                      enemy1=self.enemy_robots[0], enemy2=self.enemy_robots[1], enemy3=self.enemy_robots[2]) # Attacker behaviour in penalty

        if self.stOfensePenalty == 'spin':
            action.attacker_penalty_spin(self.robots[2], self.ball)
        elif self.stOfensePenalty == 'direct':
            action.attacker_penalty_direct(self.robots[2])



        # If the ball gets away from the robot, stop the penalty mode
        if sqrt((self.ball.coordinates.X - self.robots[2].coordinates.X) ** 2 + (self.ball.coordinates.Y - self.robots[2].yPos) ** 2) > 30:
            self.penaltyOffensive = False

    def penalty_mode_offensive_spin(self):
        """Input: None
        Description: Penalty kick offence strategy with spin.
        Output: None."""
        action.screen_out_ball(self.robots[0], self.ball, 10, left_side=not self.mray)  # Goalkeeper keeps in defense
        action.shoot(self.robots[1], self.ball, left_side=not self.mray, friend1=self.robots[0], friend2=self.robots[2],
                     enemy1=self.enemy_robots[0], enemy2=self.enemy_robots[1], enemy3=self.enemy_robots[2]) # Defender going to the rebound

        if not self.robots[2].dist(self.ball) < 9: # If the attacker is not closer to the ball
            action.girar(self.robots[2], 100, 100) # Moving forward
        else:
            if self.robots[2].teamYellow: # Team verification
                if self.robots[2].yPos < 65:
                    action.girar(self.robots[2], 0, 100) # Shoots the ball spinning up
                else:
                    action.girar(self.robots[2], 100, 0) # Shoots the ball spinning down
            else:
                if self.robots[2].yPos > 65:
                    action.girar(self.robots[2], 0, 100) # Shoots the ball spinning down
                else:
                    action.girar(self.robots[2], 100, 0) # Shoots the ball spinning up

        # If the ball gets away from the robot, stop the penalty mode
        if sqrt((self.ball.coordinates.X - self.robots[2].coordinates.X) ** 2 + (self.ball.coordinates.Y - self.robots[2].yPos) ** 2) > 30:
            self.penaltyOffensive = False


    def penalty_mode_offensive_mirror(self):
        action.screen_out_ball(self.robots[0], self.ball, 10, left_side=not self.mray)  # Goalkeeper keeps in defense
        action.shoot(self.robots[1], self.ball, left_side=not self.mray, friend1=self.robots[0], friend2=self.robots[2],
                     enemy1=self.enemy_robots[0], enemy2=self.enemy_robots[1], enemy3=self.enemy_robots[2]) # Defender going to the rebound
        if self.robots[2].teamYellow:
            action.girar(self.robots[2],30,40)
        else:
            action.girar(self.robots[2],40,30)
        if sqrt((self.ball.coordinates.X - self.robots[2].coordinates.X) ** 2 + (self.ball.coordinates.Y - self.robots[2].yPos) ** 2) > 20:
            self.penaltyOffensive = False

    """
    Input: None
    Description: Calls leader and follower technique for use in strategies.
    Output: None.
    """

    def two_attackers(self):
        """Input: None
        Description: Calls leader and follower technique for use in strategies.
        Output: None."""
        action.followLeader(self.robots[0], self.robots[1], self.robots[2], self.ball, self.enemy_robots[0], self.enemy_robots[1],
                            self.enemy_robots[2])
