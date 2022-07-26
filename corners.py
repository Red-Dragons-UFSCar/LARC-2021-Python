from numpy import arctan2, pi, deg2rad
import simClasses


def handle_edge_behaviour(robot: simClasses.Robot):
    """Handles the robot's behaviour when it is on an edge"""
    edge = detect_edge(robot)
    if edge != -1:
        correct_edge_navigation(robot, edge)
        correct_on_edge_arrival_angle(robot, edge)
    else:
        robot.spin = False


def detect_edge(robot: simClasses.Robot) -> int:
    """Determines the edge of the field the robot object is in"""
    robot_coordinates = robot.get_coordinates()
    edge = -1

    if robot_coordinates.X < 20:
        edge = 1

    if robot_coordinates.X > 150:
        edge = 3

    if robot_coordinates.Y < 10:
        edge = 2

    if robot_coordinates.Y > 120:
        edge = 4

    return edge


def correct_edge_navigation(robot: simClasses.Robot, edge):
    """Changes robot's target coordinates correcting for the edges so the robot doesn't get stuck"""
    target = robot.get_target()
    target_coordinates = target.get_coordinates()
    x_correction = 0
    y_correction = 0
    match edge:
        case 1:
            x_correction = 3 if target_coordinates.X < 5 else 1.5
        case 2:
            x_correction = 3 if target_coordinates.X > 155 else 1.5
        case 3:
            y_correction = 3 if target_coordinates.Y < 5 else 1.5
        case 4:
            y_correction = 3 if target_coordinates.Y > 125 else 1.5
        case _:
            robot.spin = False
            return
    robot.spin = True
    target.set_coordinates(target_coordinates.X + x_correction, target_coordinates.Y + y_correction,
                           target_coordinates.rotation)


def correct_on_edge_arrival_angle(robot: simClasses.Robot, edge):
    """Corrects robot's arrival angle when it is on an edge"""
    target = robot.get_target()
    target_coordinates = target.get_coordinates()
    distance_to_target = robot.calculate_distance(target)
    robot_coordinates = robot.get_coordinates()
    x_rotation_base = 160 if not robot.teamYellow else 10
    pi_rotation = pi if not robot.teamYellow else -pi
    match edge:
        case 2 | 4:
            if distance_to_target < 6:
                if robot_coordinates.Y < 75:
                    rotation_offset = arctan2(75, x_rotation_base - robot_coordinates.X)
                else:
                    rotation_offset = arctan2(-75, x_rotation_base - robot_coordinates.X)
                target.set_coordinates(target_coordinates.X, target_coordinates.Y, rotation_offset)

                if target_coordinates.Y > 65 and robot.teamYellow:
                    target.set_coordinates(target_coordinates.X, target_coordinates.Y, -pi + deg2rad(10))
                else:
                    target.set_coordinates(target_coordinates.X, target_coordinates.Y, pi - deg2rad(10))
        case 1:
            if robot_coordinates.Y > 110:
                target.set_coordinates(target_coordinates.X, target_coordinates.Y, pi_rotation / 2)
            elif robot_coordinates.Y < 40:
                target.set_coordinates(target_coordinates.X, target_coordinates.Y, -pi_rotation / 2)
        case 3:
            if robot_coordinates.Y > 110:
                target.set_coordinates(target_coordinates.X, target_coordinates.Y, -pi_rotation / 2)
            elif robot_coordinates.Y < 40:
                target.set_coordinates(target_coordinates.X, target_coordinates.Y, pi_rotation / 2)

                target.set_coordinates(target_coordinates.X, target_coordinates.Y, pi / 2)
