import time
import threading
import action
from numpy import *


class PenaltyHandler:
    def __init__(self, strategy_object, robots, enemy_robots, ball, mray):
        self.defensive_penalty_tactics = ['spin', 'spin-v', 'direct']
        self.offensive_penalty_tactics = ['spin', 'direct', 'switch']
        self.timer = 0
        self.current_offensive_tactic = self.offensive_penalty_tactics.index(strategy_object.penaltyStrategies[0])
        self.current_defensive_tactic = self.defensive_penalty_tactics.index(strategy_object.penaltyStrategies[1])
        self.strategy = strategy_object
        self.robots = robots
        self.enemy_robots = enemy_robots
        self.ball = ball
        self.mray = mray
        self.checking_for_score_change = False
        self.aop = strategy_object.aop
        self.adp = strategy_object.adp

    def handle_penalty(self, penalty_state, score):
        if penalty_state == 1:
            self.handle_offensive_penalty()
        elif penalty_state == 2:
            self.handle_defensive_penalty()

    def handle_offensive_penalty(self):
        # calls function to change the penalty tactic in case of score change
        if not self.checking_for_score_change:
            self.checking_for_score_change = True
            threading.Thread(target=self.change_offensive_tactic, args=(self.strategy.get_score(),)).start()
        self.penalty_mode_offensive()

    def handle_defensive_penalty(self):
        # calls function to change the penalty tactic in case of score change
        if not self.checking_for_score_change:
            self.checking_for_score_change = True
            threading.Thread(target=self.change_defensive_tactic, args=(self.strategy.get_score(),)).start()
        self.penalty_mode_defensive()

    def penalty_mode_offensive(self):
        """Input: None
        Description: Penalty kick offence strategy.
        Output: None."""
        ball_coordinates = self.ball.get_coordinates()
        robot_coordinates = self.robots[2].get_coordinates()
        action.screen_out_ball(self.robots[0], self.ball, 10, left_side=not self.mray)  # Goalkeeper keeps in goal
        action.shoot(self.robots[1], self.ball, left_side=not self.mray)  # Defender going to the rebound

        current_tactic = self.offensive_penalty_tactics[self.current_offensive_tactic]
        match current_tactic:
            case 'spin':
                action.attacker_penalty_spin(self.robots[2], self.ball)
            case 'direct':
                action.attacker_penalty_direct(self.robots[2], self.ball, left_side=not self.mray)
            case 'switch':
                action.attacker_penalty_switch(self.robots[2])
            case _:
                print("Invalid tactic: " + current_tactic)
                print("Using default tactic: spin")
                action.attacker_penalty_spin(self.robots[2], self.ball)


        # If the ball gets away from the robot, stop the penalty mode
        if sqrt((ball_coordinates.X - robot_coordinates.X) ** 2 + (ball_coordinates.Y - robot_coordinates.Y) ** 2) > 30:
            self.strategy.end_penalty_state()

    def penalty_mode_defensive(self):
        """Input: None
        Description: Penalty kick defence strategy, goalkeeper defends goal, other robots chase ball.
        Output: None."""
        ball_coordinates = self.ball.get_coordinates()
        current_tactic = self.defensive_penalty_tactics[self.current_defensive_tactic]



        match current_tactic:
            case 'spin':
                action.defender_penalty_spin(self.robots[0], self.ball, left_side=not self.mray)
            case 'spin-v':
                action.defender_penalty_spin_proj_vel(self.robots[0], self.ball, left_side=not self.mray,
                                                        friend1=self.robots[1],
                                                        friend2=self.robots[2], enemy1=self.enemy_robots[0],
                                                        enemy2=self.enemy_robots[1],
                                                        enemy3=self.enemy_robots[2])
            case 'direct':
                action.defender_penalty(self.robots[0], self.ball, left_side=not self.mray)
            case _:
                print("Invalid tactic: " + current_tactic)
                print("Using default tactic: spin")
                action.defender_penalty_spin(self.robots[0], self.ball, left_side=not self.mray)

        # Defenders behaviour in defensive penalty
        action.shoot(self.robots[1], self.ball, left_side=not self.mray)  # Robot 1 chasing ball
        action.shoot(self.robots[2], self.ball, left_side=not self.mray)  # Robot 2 chasing ball

        # If the ball gets away from the defensive area, stops the penalty mode
        if not self.mray:
            if ball_coordinates.X > 48 or ball_coordinates.Y < 30 or ball_coordinates.Y > 100:
                self.strategy.end_penalty_state()
        else:
            if ball_coordinates.X < 112 or ball_coordinates.Y < 30 or ball_coordinates.Y > 100:
                self.strategy.end_penalty_state()


    def change_offensive_tactic(self, score):
        time.sleep(2)
        if score == self.strategy.get_score() and self.aop == "on":
            self.current_offensive_tactic = (self.current_offensive_tactic + 1) % len(self.offensive_penalty_tactics)
        self.checking_for_score_change = False

    def change_defensive_tactic(self, score):
        time.sleep(2)
        if score != self.strategy.get_score() and self.adp == "on":
            self.current_defensive_tactic = (self.current_defensive_tactic + 1) % len(self.defensive_penalty_tactics)
        self.checking_for_score_change = False
