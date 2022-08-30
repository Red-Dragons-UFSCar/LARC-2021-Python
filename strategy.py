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
        self.stOffensePenalty = strategies[1]
        self.stDefensePenalty = strategies[2]
        self.leader = None
        self.follower = None
        self.leader_time = 0

    def set_leader(self, leader):
        """Input: None
        Description: Sets the leader robot.
        Output: None."""
        self.leader = leader

    def set_follower(self, follower):
        """Input: None
        Description: Sets the follower robot.
        Output: None."""
        self.follower = follower

    def get_leader(self):
        """Input: None
        Description: Returns the leader robot.
        Output: Leader robot."""
        return self.leader

    def get_follower(self):
        """Input: None
        Description: Returns the follower robot.
        Output: Follower robot."""
        return self.follower

    def set_leader_time(self, time):
        """Input: Time
        Description: Sets the time of the leader.
        Output: None."""
        self.leader_time = time

    def get_leader_time(self):
        """Input: None
        Description: Returns the time of the leader.
        Output: Time."""
        return self.leader_time

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
        ball_coordinates = self.ball.get_coordinates()
        if self.penaltyDefensive:
            self.penalty_mode_defensive()
        elif self.penaltyOffensive:
            self.penalty_mode_offensive()
        else:
            # For the time being, the only statuses considered are which side of the field the ball is in
            if self.mray:
                if ball_coordinates.X > 85:
                    self.stg_def_v2()
                else:
                    self.stg_att_v2()
            else:
                if ball_coordinates.X > 85:
                    self.stg_att_v2()
                else:
                    self.stg_def_v2()

    def coach(self):
        """Input: None
        Description: The standard strategy, one robot as attacker, another as defender and another as goalkeeper.
        Output: None."""
        ball_coordinates = self.ball.get_coordinates()
        if self.penaltyDefensive:
            self.penalty_mode_defensive()
        elif self.penaltyOffensive:
            self.penalty_mode_offensive_spin()
        else:
            # For the time being, the only statuses considered are which side of the field the ball is in
            if self.mray:
                if ball_coordinates.X > 85:
                    self.basic_stg_def_2()
                else:
                    self.basic_stg_att()
            else:
                if ball_coordinates.x > 85:
                    self.basic_stg_att()
                else:
                    self.basic_stg_def_2()

    def basic_stg_def(self):
        """Input: None
        Description: Basic defence strategy, goalkeeper blocks goal and advance in ball, defender chases ball,
                    attacker holds in midfield.
        Output: None."""
        ball_coordinates = self.ball.get_coordinates()
        if not self.mray:
            if ball_coordinates.X < 30 and 30 < ball_coordinates.Y < 110:  # If the ball has inside of defense area
                action.defender_penalty(self.robots[0], self.ball, left_side=not self.mray)  # Goalkeeper move ball away
                action.screen_out_ball(self.robots[1], self.ball, 55, left_side=not self.mray)
            else:
                action.shoot(self.robots[1], self.ball, left_side=not self.mray)  # Defender chases ball
                action.screen_out_ball(self.robots[0], self.ball, 14, left_side=not self.mray, upper_lim=81,
                                       lower_lim=42)  # Goalkeeper keeps in goal
        else:  # The same idea for other team
            if ball_coordinates.X > 130 and 30 < ball_coordinates.Y < 110:
                action.defender_penalty(self.robots[0], self.ball, left_side=not self.mray)
                action.screen_out_ball(self.robots[1], self.ball, 55, left_side=not self.mray)
            else:
                action.shoot(self.robots[1], self.ball, left_side=not self.mray)
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
            if self.ball._coordinates.X < 40 and 30 < self.ball._coordinates.Y < 110:  # If the ball has inside of defense area
                action.defender_penalty_spin(self.robots[0], self.ball,
                                               left_side=not self.mray)  # Goalkeeper move ball away
                action.screen_out_ball(self.robots[1], self.ball, 55, left_side=not self.mray)
            else:
                action.defender_spin(self.robots[1], self.ball, left_side=not self.mray)  # Defender chases ball
                action.screen_out_ball(self.robots[0], self.ball, 14, left_side=not self.mray, upper_lim=81,
                                       lower_lim=42)  # Goalkeeper keeps in goal
        else:  # The same idea for other team
            if self.ball._coordinates.X > 130 and 30 < self.ball._coordinates.Y < 110:
                action.defender_penalty_spin(self.robots[0], self.ball, left_side=not self.mray)
                action.screen_out_ball(self.robots[1], self.ball, 55, left_side=not self.mray)
            else:
                action.defender_spin(self.robots[1], self.ball, left_side=not self.mray)
                action.screen_out_ball(self.robots[0], self.ball, 14, left_side=not self.mray, upper_lim=81,
                                       lower_lim=42)

        action.screen_out_ball(self.robots[2], self.ball, 110, left_side=not self.mray, upper_lim=120,
                               lower_lim=10)  # Attacker stays in midfield

        # Verification if robot has stopped
        if ((abs(self.robots[0]._coordinates.rotation) < deg2rad(10)) or (
                abs(self.robots[0]._coordinates.rotation) > deg2rad(170))) and (
                self.robots[0]._coordinates.X < 20 or self.robots[0]._coordinates.X > 150):
            self.robots[0].contStopped += 1
        else:
            self.robots[0].contStopped = 0

    def stg_def_v2(self):
        """Input: None
        Description: Defence part of followleader method, a robot leads chasing ball, other supports, goalie blocks
             goal and move ball away when close to the goal
        Output: None."""
        if not self.mray:
            if self.ball._coordinates.X < 40 and 30 < self.ball._coordinates.Y < 110:  # If the ball has inside of defense area
                action.defender_penalty_spin(self.robots[0], self.ball,
                                               left_side=not self.mray)  # Goalkeeper move ball away
                self.two_attackers()
            else:
                self.two_attackers()
                action.screen_out_ball(self.robots[0], self.ball, 16, left_side=not self.mray, upper_lim=84,
                                       lower_lim=42)  # Goalkeeper stays on the goal
        else:  # The same ideia, but for other team
            if self.ball._coordinates.X > 130 and 30 < self.ball._coordinates.Y < 110:
                action.defender_penalty_spin(self.robots[0], self.ball, left_side=not self.mray)
                self.two_attackers()
            else:
                self.two_attackers()
                action.screen_out_ball(self.robots[0], self.ball, 16, left_side=not self.mray, upper_lim=84,
                                       lower_lim=42)

        # Verification if robot has stopped
        if ((abs(self.robots[0]._coordinates.rotation) < deg2rad(10)) or (
                abs(self.robots[0]._coordinates.rotation) > deg2rad(170))) and (
                self.robots[0]._coordinates.X < 20 or self.robots[0]._coordinates.X > 150):
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
        ball_coordinates = self.ball.get_coordinates()
        if self.stDefensePenalty == 'spin':
            # Goalkeeper behaviour in defensive penalty
            action.defender_penalty_spin(self.robots[0], self.ball, left_side=not self.mray)
        elif self.stDefensePenalty == 'direct':
            # Goalkeeper behaviour in defensive penalty
            action.defender_penalty(self.robots[0], self.ball, left_side=not self.mray)
        # Defenders behaviour in defensive penalty
        action.shoot(self.robots[1], self.ball, left_side=not self.mray)  # Robot 1 chasing ball
        action.shoot(self.robots[2], self.ball, left_side=not self.mray)  # Robot 2 chasing ball

        # If the ball gets away from the defensive area, stops the penalty mode
        if not self.mray:
            if ball_coordinates.X > 48 or ball_coordinates.Y < 30 or ball_coordinates.Y > 100:
                self.penaltyDefensive = False
        else:
            if ball_coordinates.X < 112 or ball_coordinates.Y < 30 or ball_coordinates.Y > 100:
                self.penaltyDefensive = False

    def penalty_mode_offensive(self):
        """Input: None
        Description: Penalty kick offence strategy.
        Output: None."""
        ball_coordinates = self.ball.get_coordinates()
        robot_coordinates = self.robots[2].get_coordinates()
        action.screen_out_ball(self.robots[0], self.ball, 10, left_side=not self.mray)  # Goalkeeper keeps in goal
        action.shoot(self.robots[1], self.ball, left_side=not self.mray)  # Defender going to the rebound

        if self.stOffensePenalty == 'spin':
            action.attacker_penalty_spin(self.robots[2], self.ball)
        elif self.stOffensePenalty == 'direct':
            action.attacker_penalty_direct(self.robots[2])

        # If the ball gets away from the robot, stop the penalty mode
        if sqrt((ball_coordinates.X - robot_coordinates.X) ** 2 + (ball_coordinates.Y - robot_coordinates.Y) ** 2) > 30:
            self.penaltyOffensive = False

    def penalty_mode_offensive_spin(self):
        """Input: None
        Description: Penalty kick offence strategy with spin.
        Output: None."""
        ball_coordinates = self.ball.get_coordinates()
        robot_coordinates = self.robots[2].get_coordinates()
        action.screen_out_ball(self.robots[0], self.ball, 10, left_side=not self.mray)  # Goalkeeper keeps in defense
        action.shoot(self.robots[1], self.ball, left_side=not self.mray)  # Defender going to the rebound

        if not self.robots[2].dist(self.ball) < 9:  # If the attacker is not closer to the ball
            action.girar(self.robots[2], 100, 100)  # Moving forward
        else:
            if self.robots[2].teamYellow:  # Team verification
                if self.robots[2].yPos < 65:
                    action.girar(self.robots[2], 0, 100)  # Shoots the ball spinning up
                else:
                    action.girar(self.robots[2], 100, 0)  # Shoots the ball spinning down
            else:
                if self.robots[2].yPos > 65:
                    action.girar(self.robots[2], 0, 100)  # Shoots the ball spinning down
                else:
                    action.girar(self.robots[2], 100, 0)  # Shoots the ball spinning up

        # If the ball gets away from the robot, stop the penalty mode
        if sqrt((ball_coordinates.X - robot_coordinates.X) ** 2 + (ball_coordinates.Y - robot_coordinates.X) ** 2) > 30:
            self.penaltyOffensive = False

    def penalty_mode_offensive_mirror(self):
        ball_coordinates = self.ball.get_coordinates()
        robot_coordinates = self.robots[2].get_coordinates()
        action.screen_out_ball(self.robots[0], self.ball, 10, left_side=not self.mray)  # Goalkeeper keeps in defense
        action.shoot(self.robots[1], self.ball, left_side=not self.mray)  # Defender going to the rebound
        if self.robots[2].teamYellow:
            action.girar(self.robots[2], 30, 40)
        else:
            action.girar(self.robots[2], 40, 30)
        if sqrt((ball_coordinates.X - robot_coordinates.X) ** 2 + (
                ball_coordinates.Y - robot_coordinates.Y) ** 2) > 20:
            self.penaltyOffensive = False

    def two_attackers(self):
        """Input: None
        Description: Calls leader and follower technique for use in strategies.
        Output: None."""
        action.follow_leader(self.robots[1], self.robots[2], self.ball, self)
