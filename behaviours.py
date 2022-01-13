from numpy import array, arctan2, cos, sin, pi, sqrt, matmul, exp


class Univector:
    '''
        These functions are needed to develop the univector field, and can be found at the paper:
        "Evolutionary Univector Field-based Navigation with Collision Avoidance for Mobile Robot"
    '''

    def __init__(self):
        self.d_e = 6        # Predefined radius that decides the size of the spiral.
        self.k_r = 3        # Smoothing constant for vector field
        self.delta = 3.5    # Variance gaussian parameter
        self.k_o = 0.5      # Proportional constant of obstacle velocity
        self.d_min = 3.5    # Minimum distance what the field becomes pure


    '''
    Input: Desired rotation angle alpha
    Description: Creates a rotation matrix with angle alpha
    Output: Rotation matrix 2x2 (float)
    '''
    def rot_matrix(self, alpha):
        return array(((cos(alpha), -sin(alpha)), (sin(alpha), cos(alpha))))


    '''
    Input: x Position, y Position, x center hyperbolic spiral, y center hyperbolic spiral
    Description: Calculates the desired angle phi of a clockwise hyperbolic spiral univector field
    Output: phi -> Field angle at position (x, y)  (float)
    '''
    def phi_h_cw(self, x, y, xg, yg):
        rho = sqrt((x - xg) ** 2 + (y - yg) ** 2)   # Distance from spiral center
        theta = arctan2(y - yg, x - xg)             # Angle from spiral center

        # Implementation of Equation (2)
        if rho > self.d_e:
            phi = theta - 0.5 * pi * (2 - ((self.d_e + self.k_r) / (rho + self.k_r)))

        else:
            phi = theta - 0.5 * pi * sqrt(rho / self.d_e)

        phi = arctan2(sin(phi), cos(phi))  # Trick to mantain phi between [-pi,pi]

        return phi


    '''
    Input: x Position, y Position, x center hyperbolic spiral, y center hyperbolic spiral
    Description: Calculates the desired angle phi of a counter-clockwise hyperbolic spiral univector field
    Output: phi -> Field angle at position (x, y)  (float)
    '''
    def phi_h_ccw(self, x, y, xg, yg):
        rho = sqrt((x - xg) ** 2 + (y - yg) ** 2)   # Distance from spiral center
        theta = arctan2(y - yg, x - xg)             # Angle from spiral center

        # Implementation of Equation (2)
        if rho > self.d_e:
            phi = theta + 0.5 * pi * (2 - ((self.d_e + self.k_r) / (rho + self.k_r)))
        else:
            phi = theta + 0.5 * pi * sqrt(rho / self.d_e)

        phi = arctan2(sin(phi), cos(phi))  # Trick to mantain phi between [-pi,pi]

        return phi


    '''
    Input: Angle phi
    Description: Calculates a column vector with cos(phi) and sin(phi)
    Output: Column vector (2x1)  (float)
    '''
    def n_h(self, phi):
        return array([[cos(phi)], [sin(phi)]])


    '''
    Input: Distance r
    Description: Calculates a gaussian distribution with average r and variance self.delta
    Output: Resulting value of gaussian distribution (float)
    '''
    def gaussian_func(self, r):
        return exp(-0.5 * (r / self.delta) ** 2)


    '''
    Input: Robot object, Target object
    Description:  Calculates the angle of hyperbolic vector field which yields us to the target position
                  with the desired posture without avoiding any obstacle
    Output: phi -> Univector field angle (float)
    '''
    def hip_vec_field(self, robot, target):
        # Two rotation matrix needed for field rotation
        matrix = self.rot_matrix(-target.theta)
        matrix2 = self.rot_matrix(target.theta)

        # Position vectors
        vet_pos = [[robot.xPos], [robot.yPos]]
        target_pos = [[target.xPos], [target.yPos]]

        vet_pos = array(vet_pos) - array(target_pos)    # Coordinate system translation
        vet_pos = matmul(matrix, vet_pos)               # Coordinate system rotation

        # Position (x, y) in new coordinate system
        x = vet_pos[0]
        y = vet_pos[1]
        y = y[0]
        x = x[0]

        # Equation (4)

        # Values of yl and yr
        yl = y + self.d_e
        yr = y - self.d_e

        # Calculation of the two hyperbolic spirals, clockwise and counter-clockwise
        n_cw = self.n_h(self.phi_h_cw(x, y + self.d_e, 0, 0))
        n_ccw = self.n_h(self.phi_h_ccw(x, y - self.d_e, 0, 0))
        n_cw = [[n_cw[0]], [n_cw[1][0]]]
        n_ccw = [[n_ccw[0][0]], [n_ccw[1][0]]]

        # Composition of the two hyperbolic spirals
        if -self.d_e <= y < self.d_e:
            x_phi = 0.5 * (abs(yl) * n_ccw[0][0] + abs(yr) ** 2 * n_cw[0][0]) / self.d_e
            y_phi = 0.5 * (abs(yl) * n_ccw[1][0] + abs(yr) ** 2 * n_cw[1][0]) / self.d_e
            phi = arctan2(y_phi, x_phi)
            phi = phi[0]
        elif y < -self.d_e:
            phi = self.phi_h_cw(x, y + self.d_e, 0, 0)
        else:
            phi = self.phi_h_ccw(x, y - self.d_e, 0, 0)

        # Rotation to return a original coordinate
        # The vector in function matmul is a univector formed with angle phi in new coordinate system
        vec_phi = matmul(matrix2, [[cos(phi)], [sin(phi)]])

        # Angle calculation
        phi = arctan2(vec_phi[1], vec_phi[0])

        return phi


    '''
    Input: Robot object, Target object, Constant n, Constant d, flag Have_face (why this flag is not used?)
    Description:  Calculates the angle of 'N_Posture' vector field, which yields us to the target position
                  with the desired posture without avoiding any obstacle. This univector field is explained
                  in book Soccer Robotics, in section 4.6.2. This function is not the principal
                  (main function above)
    Output: phi -> Univector field angle (float)
    '''
    def n_vec_field(self, robot, target, n=8, d=2, have_face=False):
        rx = target.xPos + d * cos(target.theta)
        ry = target.yPos + d * sin(target.theta)
        pg_ang = arctan2(target.yPos - robot.yPos, target.xPos - robot.xPos)
        pr_ang = arctan2(ry - robot.yPos, rx - robot.xPos)
        alpha = arctan2(sin(pr_ang - pg_ang), cos(pr_ang - pg_ang))
        phi = arctan2(sin(pg_ang - n * alpha), cos(pg_ang - n * alpha))
        return phi


    '''
    Input: Robot object, Obstacle object
    Description: Calculates the angle of moving obstacle avoidance vector field
    Output: phi -> Univector field angle (float)
    '''
    def ao_vec_field(self, robot, obst):
        # Components of the shifting vector, where S=k_o*(V_obst-V_robot)
        sx = self.k_o * (obst.v * cos(obst.theta) - robot.v * cos(robot.theta))
        sy = self.k_o * (obst.v * sin(obst.theta) - robot.v * sin(robot.theta))

        s = sqrt(sx ** 2 + sy ** 2) # Module of shifting vector
        d = robot.dist(obst)        # Distance of obstacle

        # Equation (5)

        if d >= s:
            px = obst.xPos + sx
            py = obst.yPos + sy
        else:
            px = obst.xPos + (d / s) * sx
            py = obst.yPos + (d / s) * sy
        phi = arctan2(robot.yPos - py, robot.xPos - px)

        return phi


    '''
    Input: Robot object, Target object, Obstacle object
    Description: Calculates the angle of composed vector field, which mix both move-to-target (hyperbolic)
                 and avoid-obstacle vector field using a gaussian function
    Output: phi -> Univector field angle (float)
    '''
    def univec_field_h(self, robot, target, obst):
        d = robot.dist(obst)    # Robot distance

        # Equation (6)

        if d <= self.d_min:
            phi = self.ao_vec_field(robot, obst)
        else:
            phi = self.gaussian_func(d - self.d_min) * self.ao_vec_field(robot, obst)
            phi += (1 - self.gaussian_func(d - self.d_min)) * self.hip_vec_field(robot, target)

        return phi

    '''
    Input: Robot object, Target object, Obstacle object
    Description: Calculates the angle of composed vector field, which mix both move-to-target (N_Posture)
                 and avoid-obstacle vector field using a gaussian function. This function is not the main
                 (main function above)
    Output: phi -> Univector field angle (float)
    '''
    def univec_field_n(self, robot, target, obst, n=8, d=2):
        if robot.dist(obst) <= self.d_min:
            robot.flagTrocaFace = True
            phi = self.ao_vec_field(robot, obst)
        else:
            robot.flagTrocaFace = False
            phi = self.gaussian_func(robot.dist(obst) - self.d_min) * self.ao_vec_field(robot, obst)
            phi += (1 - self.gaussian_func(robot.dist(obst) - self.d_min)) * self.n_vec_field(robot, target, n, d,
                                                                                              have_face=False)
        return phi
