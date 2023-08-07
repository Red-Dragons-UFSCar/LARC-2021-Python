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
                    rand = random.random()
                    if rand > 1/2:
                        entidade4 = Entity(x=190.5, y=90,a=335, index=4)
                    else:
                        entidade4 = Entity(x=189.5, y=90,a=25, index=4)
                    """r = random.uniform(0,1)
                    if r <0.5:
                        entidade4 = Entity(x=180, y=70,a=50, index=4)
                    else:
                        entidade4 = Entity(x=180, y=110,a=-50, index=4)"""
                replacement.place_all([entidade0, entidade1, entidade2, entidade3, entidade4])

        #TODO FOULS: Revisar as posições futuramente do goalKick
        #elif ref_data["foul"] == 2:
            #entidade0 = Entity(x=50, y=100,a=0, index=0)
            #entidade1 = Entity(x=50, y=60,a=0, index=1)
            #entidade2 = Entity(x=50, y=20,a=0, index=2)
            #replacement.place_all([entidade0, entidade1, entidade2])

        elif ref_data["foul"] == 3:
            if ref_data["quad"] == 1:
                entidade0 = Entity(x=125, y=45,a=90, index=0)
                entidade1 = Entity(x=46.51, y=95.54,a=-70.01, index=1)
                entidade2 = Entity(x=42.71, y=105.99,a=-70.01, index=2)
                entidade3 = Entity(x=155, y=150,a=0, index=3)
                entidade4 = Entity(x=175, y=80,a=0, index=4)
            elif ref_data["quad"] == 2:
                entidade0 = Entity(x=60, y=80,a=90, index=0)
                entidade1 = Entity(x=42.71, y=74.00,a=-109.98, index=1)
                entidade2 = Entity(x=46.51, y=84.45,a=-109.98, index=2)
                entidade3 = Entity(x=45, y=15600,a=0, index=3)
                entidade4 = Entity(x=175, y=90,a=0, index=4)
            elif ref_data["quad"] == 3:
                entidade0 = Entity(x=60, y=100,a=90, index=0)
                entidade1 = Entity(x=46.51, y=95.54,a=-70.01, index=1)
                entidade2 = Entity(x=42.71, y=105.99,a=-70.01, index=2)
                entidade3 = Entity(x=45, y=30,a=0, index=3)
                entidade4 = Entity(x=175, y=90,a=0, index=4)
            elif ref_data["quad"] == 4:
                entidade0 = Entity(x=80, y=150,a=90, index=0)
                entidade1 = Entity(x=42.71, y=74.00,a=-109.98, index=1)
                entidade2 = Entity(x=46.51, y=84.45,a=-109.98, index=2)
                entidade3 = Entity(x=155, y=30,a=0, index=3)
                entidade4 = Entity(x=175, y=100,a=0, index=4)
            replacement.place_all([entidade0, entidade1, entidade2, entidade3, entidade4])

        elif ref_data["foul"] == 4:
            if ref_data["yellow"] == False: # Ofensivo
                entidade0 = Entity(x=115, y=60,a=45, index=0)
                entidade1 = Entity(x=46.51, y=84.43,a=90, index=1)
                entidade2 = Entity(x=46.51, y=95.55,a=90, index=2)
                entidade3 = Entity(x=115, y=120,a=-45, index=3)
                entidade4 = Entity(x=115, y=90,a=0, index=4)
            else: # Defensivo
                entidade0 = Entity(x=90, y=110,a=-30, index=0)
                entidade1 = Entity(x=46.51, y=84.43,a=90, index=1)
                entidade2 = Entity(x=46.51, y=95.55,a=90, index=2)
                entidade3 = Entity(x=90, y=70,a=30, index=3)
                entidade4 = Entity(x=90, y=90,a=0, index=4)
            replacement.place_all([entidade0, entidade1, entidade2, entidade3, entidade4])


    if mray == True:
        if ref_data["foul"] == 1:
            if ref_data["yellow"] == True: # Ofensivo
                entidade0 = Entity(x=190, y=90,a=180, index=0)
                entidade1 = Entity(x=203.48, y=84.44,a=90, index=1)
                entidade2 = Entity(x=203.48, y=95.55,a=90, index=2)
                entidade3 = Entity(x=135, y=95,a=180, index=3)
                entidade4 = Entity(x=59.5, y=90,a=205, index=4)
                rand = random.random()
                if rand > 1/2:
                    entidade4 = Entity(x=59.5, y=90,a=205, index=4)
                else:
                    entidade4 = Entity(x=59.5, y=90,a=155, index=4)
                """r = random.uniform(0,1)
                if r <0.5:
                    entidade4 = Entity(x=70, y=70,a=130, index=4)
                else:
                    entidade4 = Entity(x=70, y=110,a=-130, index=4)"""
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
                entidade0 = Entity(x=190, y=80,a=90, index=0)
                entidade1 = Entity(x=203.48, y=84.45,a=289.98, index=1)
                entidade2 = Entity(x=207.28, y=74.00,a=289.98, index=2)
                entidade3 = Entity(x=205, y=150,a=0, index=3)
                entidade4 = Entity(x=75, y=90,a=0, index=4)
            elif ref_data["quad"] == 2:
                entidade0 = Entity(x=125, y=45,a=90, index=0)
                entidade1 = Entity(x=207.28, y=105.99,a=250.01, index=1)
                entidade2 = Entity(x=203.48, y=95.54,a=250.01, index=2)
                entidade3 = Entity(x=95, y=150,a=180, index=3)
                entidade4 = Entity(x=75, y=80,a=205, index=4)
            elif ref_data["quad"] == 3:
                entidade0 = Entity(x=125, y=135,a=90, index=0)
                entidade1 = Entity(x=203.48, y=84.45,a=289.98, index=1)
                entidade2 = Entity(x=207.28, y=74.00,a=289.98, index=2)
                entidade3 = Entity(x=95, y=30,a=0, index=3)
                entidade4 = Entity(x=75, y=100,a=155, index=4)
            elif ref_data["quad"] == 4:
                entidade0 = Entity(x=190, y=100,a=90, index=0)
                entidade1 = Entity(x=207.28, y=105.99,a=250.01, index=1)
                entidade2 = Entity(x=203.48, y=95.54,a=250.01, index=2)
                entidade3 = Entity(x=205, y=30,a=0, index=3)
                entidade4 = Entity(x=75, y=90,a=180, index=4)
            replacement.place_all([entidade0, entidade1, entidade2, entidade3, entidade4])


        elif ref_data["foul"] == 4:
            if ref_data["yellow"] == False: # Defensivo
                entidade0 = Entity(x=160, y=110,a=210, index=0)
                entidade1 = Entity(x=203.48, y=84.44,a=90, index=1)
                entidade2 = Entity(x=203.48, y=95.55,a=90, index=2)
                entidade3 = Entity(x=160, y=70,a=150, index=3)
                entidade4 = Entity(x=160, y=90,a=0, index=4)
            else: # Ofensivo
                entidade0 = Entity(x=190, y=90,a=0, index=0)
                entidade1 = Entity(x=203.48, y=84.44,a=90, index=1)
                entidade2 = Entity(x=203.48, y=95.55,a=90, index=2)
                entidade3 = Entity(x=130, y=120,a=180, index=3)
                entidade4 = Entity(x=135, y=80,a=135, index=4)
            replacement.place_all([entidade0, entidade1, entidade2, entidade3, entidade4])