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
        if target.xPos < 20: #updates target if x position is less than 20

            flag_corner = True
            corner = 1
            if target.xPos < 5:
                target.update(target.xPos + 3, target.yPos, target.theta)
            else:
                target.update(target.xPos + 1.5, target.yPos, target.theta)
        elif target.xPos > 150: #updates target if x position is bigger than 150

            flag_corner = True
            corner = 3
            if target.xPos > 155:
                target.update(target.xPos - 3, target.yPos, target.theta)
            else:
                target.update(target.xPos - 1.5, target.yPos, target.theta)
        if target.yPos < 10: #updates target if y position is less than 10

            flag_corner = True
            corner = 2
            if target.yPos < 5:
                target.update(target.xPos, target.yPos + 3, target.theta)
            else:
                target.update(target.xPos, target.yPos + 1.5, target.theta)
        elif target.yPos > 120: #updates target if y position is bigger than 120

            flag_corner = True
            corner = 4
            if target.yPos > 125:
                target.update(target.xPos, target.yPos - 3, target.theta)
            else:
                target.update(target.xPos, target.yPos - 1.5, target.theta)
    else: #other team
        if target.xPos < 20: #updates target if x position is less than 120

            flag_corner = True
            corner = 1
            if target.xPos < 15:
                target.update(target.xPos + 3, target.yPos, target.theta)
            else:
                target.update(target.xPos + 1.5, target.yPos, target.theta)
        elif target.xPos > 150: #updates target if x position is bigger than 150

            flag_corner = True
            corner = 3
            if target.xPos > 155:
                target.update(target.xPos - 3, target.yPos, target.theta)
            else:
                target.update(target.xPos - 1.5, target.yPos, target.theta)
        if target.yPos < 10: #updates target if y position is less than 10

            flag_corner = True
            corner = 2
            if target.yPos < 5:
                target.update(target.xPos, target.yPos + 3, target.theta)
            else:
                target.update(target.xPos, target.yPos + 1.5, target.theta)
        elif target.yPos > 120: #updates target if y position is bigger than 120

            flag_corner = True
            corner = 4
            if target.yPos > 125:
                target.update(target.xPos, target.yPos - 3, target.theta)
            else:
                target.update(target.xPos, target.yPos - 1.5, target.theta)

    robot.spin = False
    if flag_corner:
        robot.spin = True
        change_target_theta(robot, target, corner)

    return flag_corner, corner

'''
Input: Robot object, target object, corner variable
Description: Changes the robot's arrival angle when it is in one of the corners. If the target is in our field 
            it will repel the ball and otherwise it will push it into the goal.
Output: None
'''
def change_target_theta(robot, target, corner):
    dist = sqrt((robot.xPos - target.xPos) ** 2 + (robot.yPos - target.yPos) ** 2)

    if not robot.teamYellow: #detects in which team the robot is
        if corner == 2 or corner == 4: #verifies if the corner is equal to the bottom or to the top
            if dist < 6:
                if robot.yPos < 75:
                    theta_gol = arctan2(75, 160 - robot.xPos)

                else:
                    theta_gol = arctan2(-75, 160 - robot.xPos) #-75 for being at the bottom
                target.update(target.xPos, target.yPos, theta_gol)
            else:
                target.update(target.xPos, target.yPos, 0)

        elif robot.yPos > 110:
            if corner == 1:
                target.update(target.xPos, target.yPos, pi / 2)
            elif corner == 3:
                target.update(target.xPos, target.yPos, -pi / 2)
        elif robot.yPos < 40:
            if corner == 1:
                target.update(target.xPos, target.yPos, -pi / 2)
            elif corner == 3:
                target.update(target.xPos, target.yPos, pi / 2)
    else:
        if corner == 2 or corner == 4:
            if dist < 6:
                if robot.yPos < 75:
                    theta_gol = arctan2(75, 10 - robot.xPos)

                else:
                    theta_gol = arctan2(-75, 10 - robot.xPos)
                target.update(target.xPos, target.yPos, theta_gol)
            else:
                if target.yPos > 65:
                    target.update(target.xPos, target.yPos, -pi + deg2rad(10))
                else:
                    target.update(target.xPos, target.yPos, pi - deg2rad(10))

        elif robot.yPos > 110:
            if corner == 1:
                target.update(target.xPos, target.yPos, -pi / 2)
            elif corner == 3:
                target.update(target.xPos, target.yPos, pi / 2)
        elif robot.yPos < 40:
            if corner == 1:
                target.update(target.xPos, target.yPos, pi / 2)
            elif corner == 3:
                target.update(target.xPos, target.yPos, -pi / 2)

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
    if robot.xPos < 3 and (robot.yPos > 110 or robot.yPos < 40):
        if abs(robot.theta) < 0.35 or abs(robot.theta - pi) < 0.35:  #abs returns the absolute value of the angle
            flag_locked = True
            corner = 1
    elif robot.xPos > 147 and (robot.yPos > 110 or robot.yPos < 40):
        if abs(robot.theta) < 0.35 or abs(robot.theta - pi) < 0.35:
            flag_locked = True
            corner = 3
    if robot.yPos < 5:
        if (abs(robot.theta) < ((pi / 2) + 0.35)) and (abs(robot.theta) > ((pi / 2) - 0.35)):
            flag_locked = True
            corner = 2
    elif robot.yPos > 125:
        if (abs(robot.theta) < ((pi / 2) + 0.35)) and (abs(robot.theta) < ((pi / 2) - 0.35)):
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
        target.update(robot.xPos + 100, robot.yPos, 0)
    if corner == 2:
        target.update(robot.xPos, robot.yPos + 100, pi / 2)
    if corner == 3:
        target.update(robot.xPos - 100, robot.yPos, 0)
    if corner == 4:
        target.update(robot.xPos, robot.yPos - 100, -pi / 2)
    return None
