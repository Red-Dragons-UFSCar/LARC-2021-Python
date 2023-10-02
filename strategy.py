import action, penalty_handler
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
        self.score = [0, 0]  # Current score, [our score, enemy score]
        self.penalty_state = 0  # 0 = no peanlty, 1 = offensive penalty, 2 = defensive penalty
        self.strategy = strategies[0]
        self.penaltyStrategies = strategies[1:3]
        self.aop = strategies[3]
        self.adp = strategies[4]
        self.leader = None
        self.follower = None
        self.leader_time = 0
        self.penalty_handler = penalty_handler.PenaltyHandler(self, self.robots, self.enemy_robots, self.ball,
                                                              self.mray)
        self.goal_already_happened = False
        self.flagDefenderAttack = False
        self.sideKeepPosition = 0

    def handle_game_on(self):
        if self.goal_already_happened:
            self.goal_already_happened = False
        self.decider()
        #action.defender_spin(self.robots[0], self.ball, left_side=not self.mray)  # Attacker behavior

    def handle_goal(self, foul_was_yellow):
        if self.goal_already_happened:
            return
        self.goal_already_happened = True
        match self.mray:
            case True if foul_was_yellow:
                self.score[1] += 1
                print("gol inimigo")
            case True if not foul_was_yellow:
                self.score[0] += 1
                print("Gol nosso")
            case False if foul_was_yellow:
                self.score[0] += 1
                print("Gol nosso")
            case False if not foul_was_yellow:
                self.score[1] += 1
                print("gol inimigo")
        print(self.score)

    def get_score(self):
        return self.score.copy()

    def end_penalty_state(self):
        self.penalty_state = 0

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
        if self.penalty_state:
            self.penalty_handler.handle_penalty(self.penalty_state, self.score.copy())
            return
        match self.strategy:
            case 'default':
                self.coach()
            case 'twoAttackers':
                self.coach2()
            case _:
                print("Strategy not found")

    def coach2(self):
        """Input: None
        Description: Advanced strategy, one goalkeeper defends while two robots chase the ball, with one leading and the other in support.
        Output: None."""
        ball_coordinates = self.ball.get_coordinates()
        if self.mray:
            if ball_coordinates.X > 75:
                self.stg_def_v2()
            else:
                self.stg_att_v2()
        else:
            if ball_coordinates.X > 75:
                self.stg_att_v2()
            else:
                self.stg_def_v2()
    
    def coach_fisico(self):
        self.robot_goalkeeper = self.robots[0]
        self.robot_defender = self.robots[1]
        self.robot_attacker = self.robots[2]

        self.lim_def_area_x = 35
        self.lim_def_area_y_s = 110
        self.lim_def_area_y_i = 30
        
        self.goalkeeper()
        self.defender()
        self.attacker()

    def goalkeeper(self):
        ball_coordinates = self.ball.get_coordinates()
        self.mray = False
        if not self.mray:
            if ball_coordinates.X < self.lim_def_area_x and self.lim_def_area_y_i < ball_coordinates.Y < self.lim_def_area_y_s:  # If the ball has inside of defense area
                if self.robot_goalkeeper.calculate_distance(self.ball)<9:
                    if self.robot_goalkeeper._coordinates.Y < self.ball._coordinates.Y:
                        self.robot_goalkeeper.sim_set_vel(0, -20)
                    else:
                        self.robot_goalkeeper.sim_set_vel(0, 20)
                else:
                    action.defender_penalty(self.robot_goalkeeper, self.ball,left_side=not self.mray)  # Goalkeeper move ball away
            else:
                action.screen_out_ball(self.robot_goalkeeper, self.ball, 20, left_side=not self.mray, upper_lim=85,
                                       lower_lim=40)  # Goalkeeper keeps in goal
        else:  # The same idea for other team
            if ball_coordinates.X > 160-self.lim_def_area_x and self.lim_def_area_y_i < ball_coordinates.Y < self.lim_def_area_y_s:  # If the ball has inside of defense area
                if self.robot_goalkeeper.calculate_distance(self.ball)<9:
                    if self.robot_goalkeeper._coordinates.Y < self.ball._coordinates.Y:
                        self.robot_goalkeeper.sim_set_vel(0, 20)
                    else:
                        self.robot_goalkeeper.sim_set_vel(0, -20)
                else:
                    action.defender_penalty(self.robot_goalkeeper, self.ball,left_side=not self.mray)  # Goalkeeper move ball away
            else:
                action.screen_out_ball(self.robot_goalkeeper, self.ball, 20, left_side=not self.mray, upper_lim=81,
                                       lower_lim=42)
        self.mray = True
                
    def defender_standard(self):
        ball_coordinates = self.ball.get_coordinates()
        if not self.mray:
            if ball_coordinates.X < 85: 
                if ball_coordinates.X < self.lim_def_area_x and self.lim_def_area_y_i < ball_coordinates.Y < self.lim_def_area_y_s:  # If the ball has inside of defense area
                    action.screen_out_ball(self.robot_defender, self.ball, 55, left_side=not self.mray)
                else:
                    action.defender_spin(self.robot_defender, self.ball, left_side=not self.mray)  # Defender chases ball
            else:
                action.screen_out_ball(self.robot_defender, self.ball, 60, left_side=not self.mray, upper_lim=120, lower_lim=10)  # Defender behavior
        
        else:  # The same idea for other team
            if ball_coordinates.X > 65:
                if ball_coordinates.X < 160-self.lim_def_area_x and self.lim_def_area_y_i < ball_coordinates.Y < self.lim_def_area_y_s:  # If the ball has inside of defense area
                    action.screen_out_ball(self.robot_defender, self.ball, 55, left_side=not self.mray)
                else:
                    action.defender_spin(self.robot_defender, self.ball, left_side=not self.mray)  # Defender chases ball
            else:
                action.screen_out_ball(self.robot_defender, self.ball, 60, left_side=not self.mray, upper_lim=120, lower_lim=10)  # Defender behavior
    
    def defender(self):
        ball_coordinates = self.ball.get_coordinates() # Coordenadas da bola
        attacker_coordinates = self.robot_attacker.get_coordinates()
        
        if not self.mray: # Lado esquerdo
            if ball_coordinates.X < 85:  # Defendendo
                # Se a bola está na área de defesa
                if ball_coordinates.X < self.lim_def_area_x and self.lim_def_area_y_i < ball_coordinates.Y < self.lim_def_area_y_s:  # If the ball has inside of defense area
                    action.screen_out_ball(self.robot_defender, self.ball, 55, left_side=not self.mray)
                else:
                    action.defender_spin(self.robot_defender, self.ball, left_side=not self.mray)  # Defender chases ball
            else:   # Atacando
                # Condicoes para avançar o robo zagueiro
                if ball_coordinates.X < 107.5 and self.flagDefenderAttack: # Retorno do zagueiro
                    self.flagDefenderAttack = False
                elif ball_coordinates.X > 112.5 and not self.flagDefenderAttack: # Avanço do zagueiro
                    self.flagDefenderAttack = True

                # Definicão da posição de espera na intermediaria
                if ball_coordinates.X < 112.5:
                    if ball_coordinates.Y > 65:
                        self.sideKeepPosition = 0
                    else:
                        self.sideKeepPosition = 1
                
                # Se ele for para o ataque
                if self.flagDefenderAttack:
                    # Condição de bola na area de atuacao
                    area = (ball_coordinates.X > 125) and (ball_coordinates.Y > 40) and (ball_coordinates.Y < 90)
                    attacker_area = (attacker_coordinates.X > 125) and (attacker_coordinates.Y > 50) and (attacker_coordinates.Y < 80)
                    if area and not attacker_area: # Se a bola está na área
                        action.defender_spin(self.robot_defender, self.ball, left_side=not self.mray)  # Defender chases ball
                    else: # Mantem posicao de espera
                        if self.sideKeepPosition==0:
                            action.go_to_point(self.robot_defender, 112.5, 25, 0)
                        else:
                            action.go_to_point(self.robot_defender, 112.5, 105, 0)
                    
                    if (ball_coordinates.Y > 100) and self.sideKeepPosition == 1:
                        self.sideKeepPosition = 0
                    elif (ball_coordinates.Y < 30) and self.sideKeepPosition == 0:
                        self.sideKeepPosition = 1
                    
                else: # Se ele se mantem na defesa
                    action.screen_out_ball(self.robot_defender, self.ball, 60, left_side=not self.mray, upper_lim=120, lower_lim=10)  # Defender behavior
            print(self.sideKeepPosition)

        else:  # The same idea for other team
            if ball_coordinates.X > 85:  # Defendendo
                # Se a bola está na área de defesa
                if ball_coordinates.X > 160 - self.lim_def_area_x and self.lim_def_area_y_i < ball_coordinates.Y < self.lim_def_area_y_s:  # If the ball has inside of defense area
                    action.screen_out_ball(self.robot_defender, self.ball, 55, left_side=not self.mray)
                else:
                    action.defender_spin(self.robot_defender, self.ball, left_side=not self.mray)  # Defender chases ball
            else:   # Atacando
                # Condicoes para avançar o robo zagueiro
                if ball_coordinates.X > 52.5 and self.flagDefenderAttack: # Retorno do zagueiro
                    self.flagDefenderAttack = False
                elif ball_coordinates.X < 47.5 and not self.flagDefenderAttack: # Avanço do zagueiro
                    self.flagDefenderAttack = True

                # Definicão da posição de espera na intermediaria
                if ball_coordinates.X < 47.5:
                    if ball_coordinates.Y > 65:
                        self.sideKeepPosition = 2
                    else:
                        self.sideKeepPosition = 3
                
                # Se ele for para o ataque
                if self.flagDefenderAttack:
                    # Condição de bola na area de atuacao
                    area = (ball_coordinates.X < 35) and (ball_coordinates.Y > 40) and (ball_coordinates.Y < 90)
                    attacker_area = (attacker_coordinates.X < 35) and (attacker_coordinates.Y > 50) and (attacker_coordinates.Y < 80)
                    if area and not attacker_area: # Se a bola está na área
                        action.defender_spin(self.robot_defender, self.ball, left_side=not self.mray)  # Defender chases ball
                    else: # Mantem posicao de espera
                        if self.sideKeepPosition==2:
                            action.go_to_point(self.robot_defender, 47.5, 25, 180)
                        elif self.sideKeepPosition==3:
                            action.go_to_point(self.robot_defender, 47.5, 105, 180)
                    
                    if (ball_coordinates.Y > 100) and self.sideKeepPosition == 3:
                        self.sideKeepPosition = 2
                    elif (ball_coordinates.Y < 30) and self.sideKeepPosition == 2:
                        self.sideKeepPosition = 3
                    
                else: # Se ele se mantem na defesa
                    action.screen_out_ball(self.robot_defender, self.ball, 60, left_side=not self.mray, upper_lim=120, lower_lim=10)  # Defender behavior
            print(self.sideKeepPosition)

    def attacker(self):

        ball_coordinates = self.ball.get_coordinates() # Coordenadas da bola

        if self.mray:
            if ball_coordinates.X > 85:
                if ball_coordinates.Y > 65:
                    action.go_to_point(self.robot_attacker, 47.5, 25, 180)
                else:
                    action.go_to_point(self.robot_attacker, 47.5, 105, 180)
                #action.screen_out_ball(self.robots[2], self.ball, 110, left_side=not self.mray, upper_lim=120,
                #                lower_lim=10)  # Attacker stays in midfield
            else:
                action.defender_spin(self.robots[2], self.ball, left_side=not self.mray)  # Attacker behavior
        else:
            if ball_coordinates.X < 85:
                if ball_coordinates.Y > 65:
                    action.go_to_point(self.robot_attacker, 112.5, 25, 180)
                else:
                    action.go_to_point(self.robot_attacker, 112.5, 105, 180)
                #action.screen_out_ball(self.robots[2], self.ball, 110, left_side=not self.mray, upper_lim=120,
                #                lower_lim=10)  # Attacker stays in midfield
            else:
                action.defender_spin(self.robots[2], self.ball, left_side=not self.mray)  # Attacker behavior
                        
    def coach(self):
        """Input: None
        Description: The standard strategy, one robot as attacker, another as defender and another as goalkeeper.
        Output: None."""
        ball_coordinates = self.ball.get_coordinates()
        if self.mray:
            if ball_coordinates.X > 85:
                self.basic_stg_def_2()
            else:
                self.basic_stg_att()
        else:
            if ball_coordinates.X > 85:
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
                action.defender_spin(self.robots[1], self.ball, left_side=not self.mray)  # Defender chases ball
                action.screen_out_ball(self.robots[0], self.ball, 14, left_side=not self.mray, upper_lim=81,
                                       lower_lim=42)  # Goalkeeper keeps in goal
        else:  # The same idea for other team
            if ball_coordinates.X > 130 and 30 < ball_coordinates.Y < 110:
                action.defender_penalty(self.robots[0], self.ball, left_side=not self.mray)
                action.screen_out_ball(self.robots[1], self.ball, 55, left_side=not self.mray)
            else:
                action.defender_spin(self.robots[1], self.ball, left_side=not self.mray)
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
        action.screen_out_ball(self.robots[0], self.ball, 22, left_side=not self.mray, upper_lim=81,
                               lower_lim=42)  # Goalkeeper behavior

    def basic_stg_def_2(self):
        """Input: None
        Description: Basic defense strategy with robot stop detection
        Output: None."""
        if not self.mray:
            if self.ball._coordinates.X < 40 and 30 < self.ball._coordinates.Y < 110:  # If the ball has inside of defense area
                if self.robots[0].calculate_distance(self.ball)<9:
                    if self.robots[0]._coordinates.Y < self.ball._coordinates.Y:
                        self.robots[0].sim_set_vel(0, -20)
                    else:
                        self.robots[0].sim_set_vel(0, 20)
                else:
                    action.defender_penalty(self.robots[0], self.ball,left_side=not self.mray)  # Goalkeeper move ball away
                action.screen_out_ball(self.robots[1], self.ball, 55, left_side=not self.mray)

            else:
                action.defender_spin(self.robots[1], self.ball, left_side=not self.mray)  # Defender chases ball
                action.screen_out_ball(self.robots[0], self.ball, 22, left_side=not self.mray, upper_lim=81,
                                       lower_lim=42)  # Goalkeeper keeps in goal
            if self.ball._coordinates.Y > 65:
                action.go_to_point(self.robots[2], 110, 45, pi/2)
            else:
                action.go_to_point(self.robots[2], 110, 85, pi/2)
            #action.screen_out_ball(self.robots[2], self.ball, 110, left_side=not self.mray)
            #action.go_to_point(self.robots[2], 105, 65, pi/2)
        else:  # The same idea for other team
            if self.ball._coordinates.X > 135 and 30 < self.ball._coordinates.Y < 110:
                if self.robots[0].calculate_distance(self.ball)<9:
                    if self.robots[0]._coordinates.Y > self.ball._coordinates.Y:
                        self.robots[0].sim_set_vel(0, -20)
                    else:
                        self.robots[0].sim_set_vel(0, 20)
                else:
                    action.defender_penalty(self.robots[0], self.ball, left_side=not self.mray)
                action.screen_out_ball(self.robots[1], self.ball, 55, left_side=not self.mray)
            else:
                action.defender_spin(self.robots[1], self.ball, left_side=not self.mray)
                action.screen_out_ball(self.robots[0], self.ball, 22, left_side=not self.mray, upper_lim=81,
                                       lower_lim=42)
            action.screen_out_ball(self.robots[2], self.ball, 110, left_side=not self.mray)
            #action.go_to_point(self.robots[2], 65, 65, pi/2)

        #action.screen_out_ball(self.robots[2], self.ball, 110, left_side=not self.mray, upper_lim=120,
        #                       lower_lim=10)  # Attacker stays in midfield
        

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
                if self.robots[0].calculate_distance(self.ball)<12:
                    if self.robots[0]._coordinates.Y < self.ball._coordinates.Y:
                        self.robots[0].sim_set_vel(0, -20)
                    else:
                        self.robots[0].sim_set_vel(0, 20)
                else:
                    action.defender_penalty(self.robots[0], self.ball,
                                             left_side=not self.mray)  # Goalkeeper move ball away
                self.two_attackers()
            else:
                self.two_attackers()
                action.screen_out_ball(self.robots[0], self.ball, 22, left_side=not self.mray, upper_lim=84,
                                       lower_lim=42)  # Goalkeeper stays on the goal
        else:  # The same ideia, but for other team
            if self.ball._coordinates.X > 130 and 30 < self.ball._coordinates.Y < 110:
                if self.robots[0].calculate_distance(self.ball)<12:
                    if self.robots[0]._coordinates.Y > self.ball._coordinates.Y:
                        self.robots[0].sim_set_vel(0, -20)
                    else:
                        self.robots[0].sim_set_vel(0, 20)
                else:
                    action.defender_penalty(self.robots[0], self.ball, left_side=not self.mray)
                self.two_attackers()
            else:
                self.two_attackers()
                action.screen_out_ball(self.robots[0], self.ball, 22, left_side=not self.mray, upper_lim=84,
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
        action.screen_out_ball(self.robots[0], self.ball, 22, left_side=not self.mray, upper_lim=84, lower_lim=42)
        self.robots[0].contStopped = 0

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
