from numpy import sqrt, zeros, int32


# from scipy.spatial import distance -> Descomentar quando atividade do Grid voltar

# Units: cm, rad, s


class KinematicBody:
    """Base class for all moving bodies"""
    def __init__(self):
        self.coordinates = SpatialCoordinates()
        self.velocities = Velocities()

    def set_coordinates(self, x, y, rotation):
        self.coordinates.X = x
        self.coordinates.Y = y
        self.coordinates.rotation = rotation

    def set_velocities(self, linear, angular, x, y):
        self.velocities.linear = linear
        self.velocities.angular = angular
        self.velocities.X = x
        self.velocities.Y = y

    def get_coordinates(self):
        """Returns tuple with X, Y and Angle"""
        return self.coordinates.X, self.coordinates.Y, self.coordinates.rotation

    def get_velocities(self):
        """Returns tuple wit linear velocity, angular velocity, X velocity and Y velocity"""
        return self.velocities.linear, self.velocities.angular, self.velocities.X, self.velocities.Y

    def calculate_distance(self, body):
        """calculates the distance between self and another kinematic body"""
        return sqrt((self.coordinates.X - body.coordinates.X) ** 2 + (self.coordinates.Y - body.coordinates.Y) ** 2)

    def calculate_distance_from_goal(self, mray):
        """Checks distance from object to one of the goals, choose which goal by using mray"""
        if not mray:  # Goal coordinates for each team
            x_gol = 160
            y_gol = 65
        else:
            x_gol = 10
            y_gol = 65

        return sqrt((x_gol - self.get_coordinates()[0]) ** 2 + (y_gol - self.get_coordinates()[1]) ** 2)

    def show_info(self):
        """Input: None
        Description: Logs location and velocity info on the console.
        Output: Obstacle data."""
        print('coordinates.X: {:.2f} | coordinates.Y: {:.2f} | theta: {:.2f} | velocity: {:.2f}'.format(
                    self.coordinates.X, self.coordinates.Y, float(self.coordinates.rotation), self.velocities.linear))


class SpatialCoordinates:
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.rotation = 0


class Velocities:
    def __init__(self):
        self.linear = 0
        self.angular = 0
        self.X = 0
        self.Y = 0

class Target(KinematicBody):
    """Input: Current target coordinates.
    Description: Stores coordinates for the robots' current target.
    Output: Current target coordinates."""

    def __init__(self):
        super().__init__()


    def show_info(self):
        """Input: None
        Description: Logs target coordinates to the console.
        Output: Current target coordinates."""
        print('coordinates.X: {:.2f} | coordinates.Y: {:.2f} | theta: {:.2f}'.format(self.coordinates.X, self.coordinates.Y,
                                                                   float(self.Coordinates.rotation)))


class Obstacle(KinematicBody):
    """Input: Coordinates and velocity of object.
    Description: Stores coordinates and velocity of an obstacle to a robot.
    Output: Coordinates and velocity of object."""

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

    def set_obst(self, coordinates):
        """Input: Coordinates of obstacle.
        Description: Sets obstacle coordinates with data from vision.
        Output: None"""
        self.set_coordinates(coordinates)

    def update(self, friends, enemy1=None, enemy2=None, enemy3=None):
        """Input: Object lists.
        Description: Detects the nearest object and sets it as the current obstacle to avoid.
        Output: Current obstacle."""
        enemies = [enemy1, enemy2, enemy3]
        distances = []
        for friend in friends:
            distances.append(friend)
        for enemy in enemies:
            if enemy is not None:
                distances.append(enemy)

        distances.sort(key=lambda a: self.robot.calculate_distance(a))
        obstacle = distances[0]
        self.set_obst(obstacle.get_coordinates())

    def update2(self, ball, friends, enemies):
        """Input: ball, robot's friends and enemies list
        Description: Detects the nearest object and sets it as the current obstacle to avoid with some exceptions:
                         1 - The enemy player closest to the goal is not be considered obstacle
                         2 - If ball is too close to the enemy robot, he is not be considered obstacle
        Output:"""
        obstacles = enemies.copy

        ball_distances = [enemy.calculate_distance(ball) for enemy in enemies]  # Distance to ball of all enemies robots
        goal_distances = [enemy.calculate_distance_from_goal(enemy.teamYellow) for enemy in enemies]

        for index in range(len(enemies)):
            if ball_distances[index] < 15:
                obstacles.pop(index)
            elif goal_distances[index] < 20 and ball.calculate_distance_from_goal() < 20:
                obstacles.pop(index)

        obstacles.extend(friends.copy)
        obstacles.sort(key=lambda a: self.robot.calculate_distance(a))

        # Setting current obstacle
        self.set_obst(obstacles[0].get_coordinates())


class Ball(KinematicBody):
    """Input: Ball coordinates.
    Description: Stores data on the game ball.
    Output: Ball data."""

    def __init__(self):
        super().__init__()
        self.pastPose = zeros(4).reshape(2, 2)  # Stores the last 3 positions (x,y) => updated on self.simGetPose()

    def set_simulator_data(self, data_ball):
        """Input: FIRASim ball location data.
        Description: Sets positional and velocity data from simulator.
        Output: None"""
        self.coordinates.X = data_ball.x + data_ball.vx * 100 * 8 / 60
        self.coordinates.Y = data_ball.y + data_ball.vy * 100 * 8 / 60

        # Check if prev is out of field, in this case reflect ball movement to reproduce the collision
        if self.coordinates.X > 160:
            self.coordinates.X = 160 - (self.coordinates.Y - 160)
        elif self.coordinates.X < 10:
            self.coordinates.X = 10 - (self.coordinates.Y - 10)

        if self.coordinates.Y > 130:
            self.coordinates.Y = 130 - (self.coordinates.Y - 130)
        elif self.coordinates.Y < 0:
            self.coordinates.Y = - self.coordinates.Y

        self.velocities.X = data_ball.vx
        self.velocities.Y = data_ball.vy


class Robot(KinematicBody):
    """Input: Robot data.
    Description: Stores data about robots in the game.
    Output: Robot data."""

    def __init__(self, index, actuator, mray):
        super().__init__()
        self.flagTrocaFace = False
        self.isLeader = None
        self.teamYellow = mray
        self.spin = False
        self.contStopped = 0
        self.holdLeader = 0
        self.index = int32(index)
        self.actuator = actuator
        self.face = 1  # ? Defines the current face of the robot
        self.rightMotor = 0  # ? Right motor handle
        self.leftMotor = 0  # ? Left motor handle
        self.vL = 0  # ? Left wheel velocity (cm/s) => updated on simClasses.py -> simSetVel()
        self.vR = 0  # ? Right wheel velocity (cm/s) =>  updated on simClasses.py -> simSetVel()
        if self.index == 0:  # ! Robot max velocity (cm/s)
            self.vMax = 40  # 35
        else:
            self.vMax = 50
        self.rMax = 3 * self.vMax  # ! Robot max rotation velocity (rad*cm/s)
        self.L = 7.5  # ? Base length of the robot (cm)
        self.R = 3.4  # ? Wheel radius (cm)
        self.obst = Obstacle(self)  # ? Defines the robot obstacle
        self.target = Target()  # ? Defines the robot target
        self.enemies = []
        self.friends = []

    def arrive(self):
        """Input: None.
        Description: Returns True if the distance between the target and the robot is less than 3cm - False otherwise
        Output: True or False."""
        if self.calculate_distance(self.target) <= 3:
            return True
        else:
            return False

    def sim_set_simulator_data(self, data_robot):
        """Input: Simulator robot data.
        Description: Sets positional and velocity data from simulator data
        Output: None."""
        self.set_coordinates(data_robot.x, data_robot.y, data_robot.a)
        linear_velocityv = sqrt(data_robot.vx ** 2 + data_robot.vy ** 2)
        self.set_velocities(linear_velocityv, data_robot.va, data_robot.x, data_robot.y)

    def sim_set_vel(self, v, w):
        """Input: Linear and angular velocity data.
        Description: Sends velocity data to simulator to move the robots.
        Output: None."""
        if self.face == 1:
            self.vR = v + 0.5 * self.L * w
            self.vL = v - 0.5 * self.L * w
        else:
            self.vL = -v - 0.5 * self.L * w
            self.vR = -v + 0.5 * self.L * w
        self.actuator.send(self.index, self.vL, self.vR)

    def sim_set_vel2(self, v1, v2):
        """Input: Wheels velocity data.
        Description: Sends velocity data to simulator to move the robots.
        Output: None."""
        self.actuator.send(self.index, v1, v2)

    def set_friends(self, friends):
        self.friends = friends
        for index, friend in enumerate(self.friends):
            if friend is self:
                friends.pop(index)
                return

    def set_enemies(self, enemies):
        self.enemies = enemies

    def get_friends(self):
        return self.friends.copy()

    def get_enemies(self):
        return self.enemies.copy()



# Isso não deveria estar aqui


'''
-------------------Descomentar quando atividade do Grid voltar
class Grid:
    def __init__(self):

        # criando um grid 5x6
        self.gridv = array([[17.5, 13],[42.5, 13], [67.5, 13],[92.5, 13], [117.5, 13],[142.5, 13],
                      [17.5, 39],[42.5, 39], [67.5, 39],[92.5, 39], [117.5, 39],[142.5, 39],
                      [17.5, 65],[42.5, 65], [67.5, 65],[92.5, 65], [117.5, 65],[142.5, 65],
                      [17.5, 91],[42.5, 91], [67.5, 91],[92.5, 91], [117.5, 91],[142.5, 91],
                      [17.5, 117],[42.5, 117], [67.5, 117],[92.5, 117], [117.5, 117],[142.5, 117] ])

        # definindo os angulos de cada grid
        self.AttitudeGrid = array([-pi/2, 0.47282204, 0.56910571, 0.70991061, 0.9279823, 1.27818735,
                             -pi/2, 0.29463669, 0.35945951, 0.46006287, 0.63557154, 1.0038244,
                             0.06148337, 0.07225452, 0.08759046, 0.11115443, 0.15188589, 0.23793116,
                             pi/2, -0.29463669, -0.35945951, -0.46006287, -0.63557154, -1.0038244,
                             pi/2,  -0.47282204, -0.56910571, -0.70991061, -0.9279823, -1.27818735])
        self.robotGridPos = zeros(3)
        self.ballGridPos = 0

    def update(self, robot0, robot1, robot2, ball):

        # encontrando o indice em que cada robo e a bola se encontra
        index0 = argmin(distance.cdist(self.gridv, [robot0.coordinates.X, robot0.coordinates.Y]))
        index1 = argmin(distance.cdist(self.gridv, [robot1.coordinates.X, robot1.coordinates.Y]))
        index2 = argmin(distance.cdist(self.gridv, [robot2.coordinates.X, robot2.coordinates.Y]))
        indexb = argmin(distance.cdist(self.gridv, [ball.coordinates.X, ball.coordinates.Y]))

        # Atualizando os valores
        self.robotGridPos = array([index0, index1, index2])
        self.ballGridPos = indexb

    def bestGridMov():

        # Posição dos robôs
        pos0 = self.gridv[index[0]]
        pos1 = self.gridv[index[1]]
        pos2 = self.gridv[index[2]]

        # Lista dos grids mais próximos de cada robô
        listAux0 = distance.cdist(self.gridv, self.gridv[pos0]) # calcula a distancia

        # Removendo o valor 0 da lista de distancias
        zeroId = where(listAux0 == 0)
        listAux0[zeroId] = 1000
        listAux0[zeroId] = listAux0.min()

        listId0 = where(list0Aux <= 37) # encontra o indice dos valores min
        # salva a posição dos valores min
        list0 = []
        for index in listId0[0]:
            list0.append(self.gridv[index])

        listAux1 = distance.cdist(self.gridv, self.gridv[pos1])

        zeroId = where(listAux1 == 0)
        listAux1[zeroId] = 1000
        listAux1[zeroId] = listAux1.min()

        listId1 = where(listAux1 <= 37)

        list1 = []
        for index in listId1[0]:
            list1.append(self.gridv[index])

        listAux2 = distance.cdist(self.gridv, self.gridv[pos2])

        zeroId = where(listAux2 == 0)
        listAux2[zeroId] = 1000
        listAux2[zeroId] = listAux2.min()

        listId2 = where(listAux2 <= 37)
        list2 = []
        for index in listId2[0]:
            list0.append(self.gridv[index])

        #Verifica se a posição que ele vai se mover já tem algum robô

        if self.robotGridPos[1] in listId0:
            listId0n = delete(listId0[0], where(listId0 == self.robotGridPos[1]))
            list0 = delete(list0, where(listId0 == self.robotGridPos[1]), axis = 0)
        if self.robotGridPos[2] in listId0:
            listId0 = delete(listId0[0], where(listId0 == self.robotGridPos[2]))
            list0 = delete(list0, where(listId0 == self.robotGridPos[2]), axis = 0)

        if self.robotGridPos[0] in listId1:
            listId1n = delete(listId1[0], where(listId1 == self.robotGridPos[0]))
            list1 = delete(list1, where(listId1 == self.robotGridPos[0]), axis = 0)
        if self.robotGridPos[2] in listId1:
            listId1 = delete(listId1[0], where(listId1 == self.robotGridPos[2]))
            list1 = delete(list1, where(listId1 == self.robotGridPos[2]), axis = 0)

        if self.robotGridPos[0] in listId2:
            listId2n = delete(listId2[0], where(listId2 == self.robotGridPos[0]))
            list2 = delete(list2, where(listId2 == self.robotGridPos[0]), axis = 0)
        if self.robotGridPos[1] in listId2:
            listId2 = delete(listId2[0], where(listId2 == self.robotGridPos[1]))
            list2 = delete(list2, where(listId2 == self.robotGridPos[1]), axis = 0)

        # Encontrando qual grid é o mais próximo da bola
        targetId0 = argmin(distance.cdist(list0, self.gridv[indexb]))
        target0 = self.gridv[listId0n[0][targetId0]]

        targetId1 = argmin(distance.cdist(list1, self.gridv[indexb]))
        target1 = self.gridv[listId1n[0][targetId1]]

        targetId2 = argmin(distance.cdist(list2, self.gridv[indexb]))
        target2 = self.gridv[listId2n[0][targetId2]]

    #def doInGrid():
'''
