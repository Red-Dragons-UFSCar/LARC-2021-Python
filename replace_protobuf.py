import socket
import packet_pb2
import time
import numpy as np

def convert_position(x, y, theta):
    x = np.array(x)
    y = np.array(y)
    x = (x - 85)/100
    y = (y - 65)/100
    theta = np.deg2rad(theta)
    return x, y, theta

def replacer_all(x_blue, y_blue, theta_blue, x_yellow, y_yellow, theta_yellow, x_ball, y_ball):
    replacer = packet_pb2.Packet()

    if x_yellow is None:
        x_yellow = [1000, 1000, 1000]
        y_yellow = [0, 500, 1000]
        theta_yellow = [0, 0, 0]

    if x_blue is None:
        x_blue = [1000, 1000, 1000]
        y_blue = [0, 500, 1000]
        theta_blue = [0, 0, 0]

    x_blue, y_blue, theta_blue = convert_position(x_blue, y_blue, theta_blue)
    x_yellow, y_yellow, theta_yellow = convert_position(x_yellow, y_yellow, theta_yellow)
    x_ball, y_ball, _ = convert_position(x_ball, y_ball, 0)

    for i in range(3):
        robot = replacer.replace.robots.add()
        robot.yellowteam = False
        robot.position.robot_id = i
        robot.position.x = x_blue[i]
        robot.position.y = y_blue[i]
        robot.position.orientation = theta_blue[i]
        robot.turnon = True

    for i in range(3):
        robot = replacer.replace.robots.add()
        robot.yellowteam = True
        robot.position.robot_id = i
        robot.position.x = x_yellow[i]
        robot.position.y = y_yellow[i]
        robot.position.orientation = theta_yellow[i]
        robot.turnon = True

    replacer.replace.ball.x = x_ball
    replacer.replace.ball.y = y_ball

    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 20011  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
        s.connect((HOST, PORT))
        s.sendto(replacer.SerializeToString(), (HOST, PORT))
        #s.sendall(b"Hello, world")
