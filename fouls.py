from numpy import arctan2,pi,sqrt,cos,sin,array,matmul,amin,where,zeros,delete,append,int32
from bridge import (Actuator, Replacer, Vision, Referee,NUM_BOTS, convert_angle, Entity)


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
                entidade0 = Entity(x=13.75, y=65,a=0, index=0)
                entidade1 = Entity(x=96, y=25,a=180, index=1)
                entidade2 = Entity(x=96, y=90,a=0, index=2)
            else: # Ofensivo
                entidade0 = Entity(x=17.5, y=65,a=0, index=0)
                entidade1 = Entity(x=73.75, y=105,a=0, index=1)
                entidade2 = Entity(x=107.5, y=65,a=0, index=2)
            replacement.place_all([entidade0, entidade1, entidade2])

        #TODO FOULS: Revisar as posições futuramente do goalKick
        #elif ref_data["foul"] == 2:
            #entidade0 = Entity(x=50, y=100,a=0, index=0)
            #entidade1 = Entity(x=50, y=60,a=0, index=1)
            #entidade2 = Entity(x=50, y=20,a=0, index=2)
            #replacement.place_all([entidade0, entidade1, entidade2])

        elif ref_data["foul"] == 3:
            if ref_data["quad"] == 1:
                entidade0 = Entity(x=17.5, y=65,a=0, index=0)
                entidade1 = Entity(x=95, y=45,a=0, index=1)
                entidade2 = Entity(x=102.5, y=105,a=0, index=2)
            elif ref_data["quad"] == 2:
                entidade0 = Entity(x=17.5, y=72.5,a=0, index=0)
                entidade1 = Entity(x=27.5, y=105,a=0, index=1)
                entidade2 = Entity(x=55, y=55,a=0, index=2)
            elif ref_data["quad"] == 3:
                entidade0 = Entity(x=17.5, y=57.5,a=0, index=0)
                entidade1 = Entity(x=27.5, y=25,a=0, index=1)
                entidade2 = Entity(x=55, y=75,a=0, index=2)
            elif ref_data["quad"] == 4:
                entidade0 = Entity(x=17.5, y=65,a=0, index=0)
                entidade1 = Entity(x=95, y=85,a=180, index=1)
                entidade2 = Entity(x=102.5, y=25,a=0, index=2)
            replacement.place_all([entidade0, entidade1, entidade2])

        elif ref_data["foul"] == 4:
            entidade0 = Entity(x=17.5, y=65,a=0, index=0)
            entidade1 = Entity(x=45, y=65,a=0, index=1)
            entidade2 = Entity(x=65, y=65,a=0, index=2)
            replacement.place_all([entidade0, entidade1, entidade2])

    if mray == True:
        if ref_data["foul"] == 1:
            if ref_data["yellow"] == True:
                entidade0 = Entity(x=152.5, y=65,a=180, index=0)
                entidade1 = Entity(x=96, y=105,a=180, index=1)
                entidade2 = Entity(x=62.5, y=65,a=180, index=2)
            else:
                entidade0 = Entity(x=152.5, y=65,a=180, index=0)
                entidade1 = Entity(x=73.75, y=25,a=0, index=1)
                entidade2 = Entity(x=62.5, y=65,a=180, index=2)
            replacement.place_all([entidade0, entidade1, entidade2])

        #elif ref_data["foul"] == 2:
            #entidade0 = Entity(x=50, y=100,a=0, index=0)
            #entidade1 = Entity(x=50, y=60,a=0, index=1)
            #entidade2 = Entity(x=50, y=20,a=0, index=2)
            #replacement.place_all([entidade0, entidade1, entidade2])

        elif ref_data["foul"] == 3:
            if ref_data["quad"] == 1:
                entidade0 = Entity(x=152.5, y=72.5,a=180, index=0)
                entidade1 = Entity(x=142.5, y=105,a=180, index=1)
                entidade2 = Entity(x=115, y=55,a=180, index=2)
            elif ref_data["quad"] == 2:
                entidade0 = Entity(x=152.5, y=65,a=180, index=0)
                entidade1 = Entity(x=100, y=65,a=180, index=1)
                entidade2 = Entity(x=67.5, y=105,a=180, index=2)
            elif ref_data["quad"] == 3:
                entidade0 = Entity(x=152.5, y=65,a=180, index=0)
                entidade1 = Entity(x=100, y=65,a=180, index=1)
                entidade2 = Entity(x=67.5, y=25,a=180, index=2)
            elif ref_data["quad"] == 4:
                entidade0 = Entity(x=152, y=57.5,a=180, index=0)
                entidade1 = Entity(x=142, y=25,a=180, index=1)
                entidade2 = Entity(x=115, y=75,a=180, index=2)
            replacement.place_all([entidade0, entidade1, entidade2])

        elif ref_data["foul"] == 4:
            entidade0 = Entity(x=152, y=65,a=180, index=0)
            entidade1 = Entity(x=125, y=65,a=180, index=1)
            entidade2 = Entity(x=100, y=65,a=180, index=2)
            replacement.place_all([entidade0, entidade1, entidade2])
