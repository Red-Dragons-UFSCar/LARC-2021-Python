from numpy import arctan2, sqrt, pi, deg2rad


'''
Input: Robot object, target object
Description: These functions are used to change the execution of the player's strategies in the corner, 
            in order to prevent it from getting stuck.
Output: flag_corner: robot was detected on one side of the field
        corner: integer that says which corner it is in = 1- left side, 2-bottom, 3- right side, 4-top
'''
def target_in_corner(target, robot):
    corner = 0
    flag_corner = False
    if not robot.teamYellow: #detects in which team the robot is
        if target.coordinates.X < 20: #updates target if x position is less than 20

            flag_corner = True
            corner = 1
            if target.coordinates.X < 5:
                target.coordinates.update(target.coordinates.X + 3, target.coordinates.Y, target.coordinates.rotation)
            else:
                target.coordinates.update(target.coordinates.X + 1.5, target.coordinates.Y, target.coordinates.rotation)
        elif target.coordinates.X > 150: #updates target if x position is bigger than 150

            flag_corner = True
            corner = 3
            if target.coordinates.X > 155:
                target.coordinates.update(target.coordinates.X - 3, target.coordinates.Y, target.coordinates.rotation)
            else:
                target.coordinates.update(target.coordinates.X - 1.5, target.coordinates.Y, target.coordinates.rotation)
        if target.coordinates.Y < 10: #updates target if y position is less than 10

            flag_corner = True
            corner = 2
            if target.coordinates.Y < 5:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y + 3, target.coordinates.rotation)
            else:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y + 1.5, target.coordinates.rotation)
        elif target.coordinates.Y > 120: #updates target if y position is bigger than 120

            flag_corner = True
            corner = 4
            if target.coordinates.Y > 125:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y - 3, target.coordinates.rotation)
            else:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y - 1.5, target.coordinates.rotation)
    else: #other team
        if target.coordinates.X < 20: #updates target if x position is less than 120

            flag_corner = True
            corner = 1
            if target.coordinates.X < 15:
                target.coordinates.update(target.coordinates.X + 3, target.coordinates.Y, target.coordinates.rotation)
            else:
                target.coordinates.update(target.coordinates.X + 1.5, target.coordinates.Y, target.coordinates.rotation)
        elif target.coordinates.X > 150: #updates target if x position is bigger than 150

            flag_corner = True
            corner = 3
            if target.coordinates.X > 155:
                target.coordinates.update(target.coordinates.X - 3, target.coordinates.Y, target.coordinates.rotation)
            else:
                target.coordinates.update(target.coordinates.X - 1.5, target.coordinates.Y, target.coordinates.rotation)
        if target.coordinates.Y < 10: #updates target if y position is less than 10

            flag_corner = True
            corner = 2
            if target.coordinates.Y < 5:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y + 3, target.coordinates.rotation)
            else:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y + 1.5, target.coordinates.rotation)
        elif target.coordinates.Y > 120: #updates target if y position is bigger than 120

            flag_corner = True
            corner = 4
            if target.coordinates.Y > 125:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y - 3, target.coordinates.rotation)
            else:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y - 1.5, target.coordinates.rotation)

    robot.spin = False
    if flag_corner:
        robot.spin = True
        coordinates_rotation(robot, target, corner)

    return flag_corner, corner

'''
Input: Robot object, target object, corner variable
Description: Changes the robot's arrival angle when it is in one of the corners. If the target is in our field 
            it will repel the ball and otherwise it will push it into the goal.
Output: None
'''
def coordinates_rotation(robot, target, corner):
    dist = sqrt((robot.coordinates.X - target.coordinates.X) ** 2 + (robot.coordinates.Y - target.coordinates.Y) ** 2)

    if not robot.teamYellow: #detects in which team the robot is
        if corner == 2 or corner == 4: #verifies if the corner is equal to the bottom or to the top
            if dist < 6:
                if robot.coordinates.Y < 75:
                    rotation_gol = arctan2(75, 160 - robot.coordinates.X)

                else:
                    rotation_gol = arctan2(-75, 160 - robot.coordinates.X) #-75 for being at the bottom
                target.coordinates.update(target.coordinates.X, target.coordinates.Y, rotation_gol)
            else:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y, 0)

        elif robot.coordinates.Y > 110:
            if corner == 1:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y, pi / 2)
            elif corner == 3:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y, -pi / 2)
        elif robot.coordinates.Y < 40:
            if corner == 1:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y, -pi / 2)
            elif corner == 3:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y, pi / 2)
    else:
        if corner == 2 or corner == 4:
            if dist < 6:
                if robot.coordinates.Y < 75:
                    rotation_gol = arctan2(75, 10 - robot.coordinates.X)

                else:
                    rotation_gol = arctan2(-75, 10 - robot.coordinates.X)
                target.coordinates.update(target.coordinates.X, target.coordinates.Y, rotation_gol)
            else:
                if target.coordinates.Y > 65:
                    target.coordinates.update(target.coordinates.X, target.coordinates.Y, -pi + deg2rad(10))
                else:
                    target.coordinates.update(target.coordinates.X, target.coordinates.Y, pi - deg2rad(10))

        elif robot.coordinates.Y > 110:
            if corner == 1:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y, -pi / 2)
            elif corner == 3:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y, pi / 2)
        elif robot.coordinates.Y < 40:
            if corner == 1:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y, pi / 2)
            elif corner == 3:
                target.coordinates.update(target.coordinates.X, target.coordinates.Y, -pi / 2)

    return None

'''
Input: Target object, robot object
Description: Detects when the robot has a high possibility of being stuck in one of the corners
             (robot being very close to the corner and looking at it).
Output: flag_locked: robot was detected stuck in one of the corners
        corner: integer that says which corner it is in = 1 - left side, 2- bottom, 3- right side, 4- top
'''

def robot_locked_corner(target, robot):
    corner = 0
    flag_locked = False
    if robot.coordinates.X < 3 and (robot.coordinates.Y > 110 or robot.coordinates.Y < 40):
        if abs(robot.coordinates.rotation) < 0.35 or abs(robot.coordinates.rotation - pi) < 0.35:  #abs returns the absolute value of the angle
            flag_locked = True
            corner = 1
    elif robot.coordinates.X > 147 and (robot.coordinates.Y > 110 or robot.coordinates.Y < 40):
        if abs(robot.coordinates.rotation) < 0.35 or abs(robot.coordinates.rotation - pi) < 0.35:
            flag_locked = True
            corner = 3
    if robot.coordinates.Y < 5:
        if (abs(robot.coordinates.rotation) < ((pi / 2) + 0.35)) and (abs(robot.coordinates.rotation) > ((pi / 2) - 0.35)):
            flag_locked = True
            corner = 2
    elif robot.coordinates.Y > 125:
        if (abs(robot.coordinates.rotation) < ((pi / 2) + 0.35)) and (abs(robot.coordinates.rotation) < ((pi / 2) - 0.35)):
            flag_locked = True
            corner = 4

    if flag_locked: #calls the function change_target_pos
        change_target_pos(robot, target, corner)

    return flag_locked, corner

'''
Input: Robot object, target object, corner variable
Description: Projects the robot's position on the opposite side to which it is attached
             to perform a reverse movement.
Output: None
'''

def change_target_pos(robot, target, corner): #update the target with the intention of making the robot perform a reverse movement not to get stuck
    if corner == 1:
        target.coordinates.update(robot.coordinates.X + 100, robot.coordinates.Y, 0)
    if corner == 2:
        target.coordinates.update(robot.coordinates.X, robot.coordinates.Y + 100, pi / 2)
    if corner == 3:
        target.coordinates.update(robot.coordinates.X - 100, robot.coordinates.Y, 0)
    if corner == 4:
        target.coordinates.update(robot.coordinates.X, robot.coordinates.Y - 100, -pi / 2)
    return None
