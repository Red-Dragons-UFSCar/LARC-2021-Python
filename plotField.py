import numpy as np
import matplotlib.pyplot as plt
import behaviours
from simClasses import Robot


robo = Robot(0, "nada")                                                         # Criação de um objeto "robô"
robo_obstaculo = Robot(1, "naada tmb")                                          # Criação de outro objeto "robô" para obstaculo
robo_obstaculo.xPos = 20                                                        # Coordenadas do obstaculo
robo_obstaculo.yPos = 40
robo_obstaculo.theta = 0

robo.target.update(75, 60, np.pi/2)                                             # Update do alvo desejado pelo robô
robo.obst.update(robo, robo_obstaculo, robo_obstaculo)

V = []

#x_pos = range(55, 95, 1)                                                       # Plot de uma região do campo
#y_pos = range(40, 80, 1)

x_pos = range(1, 150, 3)                                                        # Plot do campo inteiro
y_pos = range(1, 150, 3)

x_plot = []
y_plot = []
xCoord = []
yCoord = []

univec = behaviours.Univector()                                                 # Objeto univector

#''' #(Trocar impressão, decomentar essa linha)
for i in x_pos:
    for j in y_pos:
        robo.xPos = i                                                           # Variação da posição do robô
        robo.yPos = j
        theta = univec.univecField_H(robo, robo.target, robo.obst)              # Calculo do angulo desejado pelo campo hiperbólico

        theta.astype(np.float64)                                                # Adequações
        print(type(theta))
        if type(theta) == type(np.array([])):
            theta = theta[0]

        matrix = univec.rotMatrix(theta)                                        # Criando vetores unitarios com o angulo retornado
        vetPos = np.dot(matrix,np.array([[1], [0]]))
        V.append([list(vetPos[0])[0], list(vetPos[1])[0]])
        x_plot.append(i)
        y_plot.append(j)


V = np.array(V)
origin = np.array([x_plot,y_plot])

'''
robo.target.update(75, 60, np.pi/2)             # Teste em posição unica (Descomentar linha 31)
robo.xPos = 75
robo.yPos = 80
print(univec.hipVecField(robo, robo.target))
'''

plt.figure(figsize=(6,6))                                                       # Plot do campo gerado
plt.quiver(*origin, V[:,0], V[:,1])
plt.show()
#'''
