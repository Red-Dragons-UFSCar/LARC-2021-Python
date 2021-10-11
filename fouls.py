from numpy import arctan2,pi,sqrt,cos,sin,array,matmul,amin,where,zeros,delete,append,int32,deg2rad
from bridge import (Actuator, Replacer, Vision, Referee,NUM_BOTS, convert_angle, Entity)
import random

def replacement_fouls(replacement, ref_data, mray):
    '''
    FREE_KICK = 0
    PENALTY_KICK = 1
    GOAL_KICK = 2
    FREE_BALL = 3
    KICKOFF = 4
    STOP = 5
    GAME_ON = 6
    HALT = 7
    '''
    if mray == False:
        if ref_data["foul"] == 1:
            if ref_data["yellow"] == True: # Defensivo
                entidade0 = Entity(x=18.75, y=90,a=0, index=0)
                entidade1 = Entity(x=130, y=115,a=180, index=1)
                entidade2 = Entity(x=130, y=65,a=180, index=2)
                entidade3 = Entity(x=155, y=70,a=180, index=3)
                entidade4 = Entity(x=155, y=120,a=180, index=4)
            else: # Ofensivo
                entidade0 = Entity(x=22, y=90,a=0, index=0)
                entidade1 = Entity(x=95, y=45,a=0, index=1)
                entidade2 = Entity(x=95, y=145,a=0, index=2)
                entidade3 = Entity(x=110, y=95,a=0, index=3)
                #entidade4 = Entity(x=185, y=90,a=0, index=4)
                r = random.uniform(0,1)
                if r <0.5:
                    entidade4 = Entity(x=180, y=70,a=50, index=4)
                else:
                    entidade4 = Entity(x=180, y=110,a=-50, index=4)
            replacement.place_all([entidade0, entidade1, entidade2, entidade3, entidade4])

        #TODO FOULS: Revisar as posições futuramente do goalKick
        #elif ref_data["foul"] == 2:
            #entidade0 = Entity(x=50, y=100,a=0, index=0)
            #entidade1 = Entity(x=50, y=60,a=0, index=1)
            #entidade2 = Entity(x=50, y=20,a=0, index=2)
            #replacement.place_all([entidade0, entidade1, entidade2])

        elif ref_data["foul"] == 3:
            if ref_data["quad"] == 1:
                entidade0 = Entity(x=22, y=90,a=0, index=0)
                entidade1 = Entity(x=85, y=30,a=0, index=1)
                entidade2 = Entity(x=85, y=150,a=0, index=2)
                entidade3 = Entity(x=155, y=150,a=0, index=3)
                entidade4 = Entity(x=195, y=80,a=0, index=4)
            elif ref_data["quad"] == 2:
                entidade0 = Entity(x=22, y=90,a=0, index=0)
                entidade1 = Entity(x=45, y=150,a=0, index=1)
                entidade2 = Entity(x=85, y=80,a=0, index=2)
                entidade3 = Entity(x=95, y=40,a=0, index=3)
                entidade4 = Entity(x=165, y=90,a=0, index=4)
            elif ref_data["quad"] == 3:
                entidade0 = Entity(x=22, y=90,a=0, index=0)
                entidade1 = Entity(x=45, y=30,a=0, index=1)
                entidade2 = Entity(x=85, y=100,a=0, index=2)
                entidade3 = Entity(x=95, y=140,a=0, index=3)
                entidade4 = Entity(x=164, y=90,a=0, index=4)
            elif ref_data["quad"] == 4:
                entidade0 = Entity(x=22, y=90,a=0, index=0)
                entidade1 = Entity(x=85, y=30,a=0, index=1)
                entidade2 = Entity(x=85, y=150,a=0, index=2)
                entidade3 = Entity(x=155, y=30,a=0, index=3)
                entidade4 = Entity(x=195, y=100,a=0, index=4)
            replacement.place_all([entidade0, entidade1, entidade2, entidade3, entidade4])

        elif ref_data["foul"] == 4:
            if ref_data["yellow"] == False: # Ofensivo
                entidade0 = Entity(x=15, y=90,a=0, index=0)
                entidade1 = Entity(x=80, y=70,a=0, index=1)
                entidade2 = Entity(x=80, y=110,a=0, index=2)
                entidade3 = Entity(x=120, y=120,a=0, index=3)
                entidade4 = Entity(x=115, y=80,a=45, index=4)
            else: # Defensivo
                entidade0 = Entity(x=15, y=90,a=0, index=0)
                entidade1 = Entity(x=60, y=70,a=0, index=1)
                entidade2 = Entity(x=60, y=110,a=0, index=2)
                entidade3 = Entity(x=90, y=70,a=30, index=3)
                entidade4 = Entity(x=90, y=110,a=-30, index=4)
            replacement.place_all([entidade0, entidade1, entidade2, entidade3, entidade4])


    if mray == True:
        if ref_data["foul"] == 1:
            if ref_data["yellow"] == True: # Ofensivo
                entidade0 = Entity(x=228, y=90,a=180, index=0)
                entidade1 = Entity(x=155, y=45,a=180, index=1)
                entidade2 = Entity(x=155, y=145,a=180, index=2)
                entidade3 = Entity(x=135, y=95,a=180, index=3)
                #entidade4 = Entity(x=65, y=90,a=180, index=4)
                r = random.uniform(0,1)
                if r <0.5:
                    entidade4 = Entity(x=70, y=70,a=130, index=4)
                else:
                    entidade4 = Entity(x=70, y=110,a=-130, index=4)
            else: # Defensivo
                entidade0 = Entity(x=231, y=90,a=180, index=0)
                entidade1 = Entity(x=120, y=65,a=0, index=1)
                entidade2 = Entity(x=120, y=115,a=0, index=2)
                entidade3 = Entity(x=95, y=70,a=0, index=3)
                entidade4 = Entity(x=95, y=120,a=0, index=4)
            replacement.place_all([entidade0, entidade1, entidade2, entidade3, entidade4])

        #elif ref_data["foul"] == 2:
            #entidade0 = Entity(x=50, y=100,a=0, index=0)
            #entidade1 = Entity(x=50, y=60,a=0, index=1)
            #entidade2 = Entity(x=50, y=20,a=0, index=2)
            #replacement.place_all([entidade0, entidade1, entidade2])

        elif ref_data["foul"] == 3:
            if ref_data["quad"] == 1:
                entidade0 = Entity(x=228, y=90,a=0, index=0)
                entidade1 = Entity(x=205, y=150,a=180, index=1)
                entidade2 = Entity(x=165, y=80,a=0, index=2)
                entidade3 = Entity(x=85, y=90,a=0, index=3)
                entidade4 = Entity(x=155, y=40,a=0, index=4)
            elif ref_data["quad"] == 2:
                entidade0 = Entity(x=228, y=90,a=0, index=0)
                entidade1 = Entity(x=165, y=30,a=180, index=1)
                entidade2 = Entity(x=165, y=150,a=180, index=2)
                entidade3 = Entity(x=95, y=150,a=180, index=3)
                entidade4 = Entity(x=55, y=80,a=180, index=4)
            elif ref_data["quad"] == 3:
                entidade0 = Entity(x=228, y=90,a=0, index=0)
                entidade1 = Entity(x=165, y=30,a=180, index=1)
                entidade2 = Entity(x=165, y=150,a=180, index=2)
                entidade3 = Entity(x=95, y=30,a=0, index=3)
                entidade4 = Entity(x=55, y=100,a=0, index=4)
            elif ref_data["quad"] == 4:
                entidade0 = Entity(x=228, y=90,a=0, index=0)
                entidade1 = Entity(x=205, y=30,a=180, index=1)
                entidade2 = Entity(x=165, y=100,a=180, index=2)
                entidade3 = Entity(x=155, y=140,a=180, index=3)
                entidade4 = Entity(x=85, y=90,a=180, index=4)
            replacement.place_all([entidade0, entidade1, entidade2, entidade3, entidade4])


        elif ref_data["foul"] == 4:
            if ref_data["yellow"] == False: # Defensivo
                entidade0 = Entity(x=235, y=90,a=0, index=0)
                entidade1 = Entity(x=175, y=70,a=0, index=1)
                entidade2 = Entity(x=175, y=110,a=0, index=2)
                entidade3 = Entity(x=145, y=70,a=150, index=3)
                entidade4 = Entity(x=145, y=110,a=-150, index=4)
            else: # Ofensivo
                entidade0 = Entity(x=235, y=90,a=0, index=0)
                entidade1 = Entity(x=175, y=70,a=0, index=1)
                entidade2 = Entity(x=175, y=110,a=0, index=2)
                entidade3 = Entity(x=130, y=120,a=180, index=3)
                entidade4 = Entity(x=135, y=80,a=135, index=4)
            replacement.place_all([entidade0, entidade1, entidade2, entidade3, entidade4])
