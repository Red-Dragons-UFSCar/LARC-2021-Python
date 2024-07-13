from numpy import (
    arctan2,
    pi,
    sqrt,
    cos,
    sin,
    array,
    matmul,
    amin,
    where,
    zeros,
    delete,
    append,
    int32,
    deg2rad,
)
from bridge import Actuator, Replacer, Vision, Referee, NUM_BOTS, convert_angle, Entity
import random


def replacement_fouls(replacement, ref_data, mray):
    """
    FREE_KICK = 0
    PENALTY_KICK = 1
    GOAL_KICK = 2
    FREE_BALL = 3
    KICKOFF = 4
    STOP = 5
    GAME_ON = 6
    HALT = 7
    """
    if mray == False:
        if ref_data["foul"] == 1:
            if ref_data["yellow"] == True:  # Defensivo
                entidade0 = Entity(x=18.75, y=90, a=0, index=0)
                entidade1 = Entity(x=130, y=115, a=180, index=1)
                entidade2 = Entity(x=130, y=50, a=180, index=2)
                entidade3 = Entity(x=130, y=130, a=180, index=3)
                entidade4 = Entity(x=155, y=90, a=180, index=4)
            else:  # Ofensivo
                entidade0 = Entity(x=22, y=90, a=0, index=0)
                entidade1 = Entity(x=60, y=90, a=0, index=1)
                entidade2 = Entity(x=120, y=50, a=0, index=2)
                entidade3 = Entity(x=120, y=140, a=0, index=3)
                # Reto
                """rand = random.random()
                    if rand > 1/2:
                        entidade4 = Entity(x=190.5, y=90,a=335, index=4)
                    else:
                        entidade4 = Entity(x=189.5, y=90,a=25, index=4)
                    """
                # Spin
                """
                    r = random.uniform(0,1)
                    if r <0.5:
                        entidade4 = Entity(x=180, y=70,a=50, index=4)
                    else:
                        entidade4 = Entity(x=180, y=110,a=-50, index=4)
                    """
                # Spin novo
                # Tirar 2.2 em x, 6 em y
                entidade4 = Entity(x=195.3, y=84, a=90, index=4)
            replacement.place_all(
                [entidade0, entidade1, entidade2, entidade3, entidade4]
            )

        elif ref_data["foul"] == 2:
            entidade0 = Entity(x=23, y=87, a=45, index=0)
            entidade1 = Entity(x=70, y=90, a=0, index=1)
            entidade2 = Entity(x=70, y=30, a=0, index=2)
            entidade3 = Entity(x=70, y=150, a=0, index=3)
            entidade4 = Entity(x=150, y=90, a=0, index=4)
            replacement.place_all(
                [entidade0, entidade1, entidade2, entidade3, entidade4]
            )

        elif ref_data["foul"] == 3:
            if ref_data["quad"] == 1:
                entidade0 = Entity(x=46.51, y=95.54, a=-70.01, index=0)
                entidade1 = Entity(x=42.71, y=105.99, a=-70.01, index=1)
                entidade2 = Entity(x=200, y=30, a=0, index=2)
                entidade3 = Entity(x=155, y=150, a=0, index=3)
                entidade4 = Entity(x=195, y=80, a=0, index=4)
            elif ref_data["quad"] == 2:
                entidade0 = Entity(x=42.71, y=74.00, a=-109.98, index=0)
                entidade1 = Entity(x=46.51, y=84.45, a=-109.98, index=1)
                entidade2 = Entity(x=95, y=40, a=0, index=2)
                entidade3 = Entity(x=45, y=148, a=0, index=3)
                entidade4 = Entity(x=73, y=85, a=90, index=4)
            elif ref_data["quad"] == 3:
                entidade0 = Entity(x=46.51, y=95.54, a=-70.01, index=0)
                entidade1 = Entity(x=42.71, y=105.99, a=-70.01, index=1)
                entidade2 = Entity(x=45, y=30, a=0, index=2)
                entidade3 = Entity(x=95, y=140, a=0, index=3)
                entidade4 = Entity(x=73, y=95, a=-90, index=4)
            elif ref_data["quad"] == 4:
                entidade0 = Entity(x=42.71, y=74.00, a=-109.98, index=0)
                entidade1 = Entity(x=46.51, y=84.45, a=-109.98, index=1)
                entidade2 = Entity(x=155, y=30, a=0, index=2)
                entidade3 = Entity(x=200, y=150, a=0, index=3)
                entidade4 = Entity(x=195, y=100, a=0, index=4)
            replacement.place_all(
                [entidade0, entidade1, entidade2, entidade3, entidade4]
            )

        elif ref_data["foul"] == 4:
            if ref_data["yellow"] == False:  # Ofensivo
                entidade0 = Entity(x=46.51, y=84.43, a=90, index=0)
                entidade1 = Entity(x=46.51, y=95.55, a=90, index=1)
                entidade2 = Entity(x=80, y=110, a=0, index=2)
                entidade3 = Entity(x=120, y=120, a=0, index=3)
                entidade4 = Entity(x=115, y=80, a=45, index=4)
            else:  # Defensivo
                entidade0 = Entity(x=46.51, y=84.43, a=90, index=0)
                entidade1 = Entity(x=46.51, y=95.55, a=90, index=1)
                entidade2 = Entity(x=100, y=75, a=30, index=2)
                entidade3 = Entity(x=100, y=105, a=-30, index=3)
                entidade4 = Entity(x=95, y=90, a=0, index=4)
            replacement.place_all(
                [entidade0, entidade1, entidade2, entidade3, entidade4]
            )

    if mray == True:
        if ref_data["foul"] == 1:
            if ref_data["yellow"] == True:  # Ofensivo

                entidade0 = Entity(x=228, y=90, a=180, index=0)
                entidade1 = Entity(x=190, y=90, a=180, index=1)
                entidade2 = Entity(x=130, y=60, a=0, index=2)
                entidade3 = Entity(x=130, y=130, a=0, index=3)
                # Reto
                """rand = random.random()
                if rand > 1/2:
                    entidade4 = Entity(x=59.5, y=90,a=205, index=4)
                else:
                    entidade4 = Entity(x=59.5, y=90,a=155, index=4)"""
                # Spin
                """
                r = random.uniform(0,1)
                if r <0.5:
                    entidade4 = Entity(x=70, y=70,a=130, index=4)
                else:
                    entidade4 = Entity(x=70, y=110,a=-130, index=4)
                """
                # New-spin
                entidade4 = Entity(x=54.7, y=84, a=90, index=4)
            else:  # Defensivo
                entidade0 = Entity(x=231, y=90, a=180, index=0)
                entidade1 = Entity(x=85, y=90, a=0, index=1)
                entidade2 = Entity(x=120, y=50, a=0, index=2)
                entidade3 = Entity(x=120, y=130, a=0, index=3)
                entidade4 = Entity(x=120, y=115, a=0, index=4)

            replacement.place_all(
                [entidade0, entidade1, entidade2, entidade3, entidade4]
            )

        elif ref_data["foul"] == 2:
            entidade0 = Entity(x=227, y=87, a=135, index=0)
            entidade1 = Entity(x=180, y=90, a=180, index=1)
            entidade2 = Entity(x=180, y=30, a=180, index=2)
            entidade3 = Entity(x=180, y=150, a=180, index=3)
            entidade4 = Entity(x=100, y=100, a=180, index=4)
            replacement.place_all(
                [entidade0, entidade1, entidade2, entidade3, entidade4]
            )

        elif ref_data["foul"] == 3:
            if ref_data["quad"] == 1:
                entidade0 = Entity(x=203.48, y=84.45, a=289.98, index=0)
                entidade1 = Entity(x=207.28, y=74.00, a=289.98, index=1)
                entidade2 = Entity(x=155, y=40, a=0, index=2)
                entidade3 = Entity(x=205, y=148, a=180, index=3)
                entidade4 = Entity(x=180, y=85, a=90, index=4)

            elif ref_data["quad"] == 2:
                entidade0 = Entity(x=207.28, y=105.99, a=250.01, index=0)
                entidade1 = Entity(x=203.48, y=95.54, a=250.01, index=1)
                entidade2 = Entity(x=55, y=30, a=180, index=2)
                entidade3 = Entity(x=95, y=150, a=180, index=3)
                entidade4 = Entity(x=60, y=80, a=180, index=4)
            elif ref_data["quad"] == 3:
                entidade0 = Entity(x=203.48, y=84.45, a=289.98, index=0)
                entidade1 = Entity(x=207.28, y=74.00, a=289.98, index=1)
                entidade2 = Entity(x=95, y=30, a=0, index=2)
                entidade3 = Entity(x=55, y=150, a=180, index=3)
                entidade4 = Entity(x=60, y=100, a=0, index=4)
            elif ref_data["quad"] == 4:
                entidade0 = Entity(x=207.28, y=105.99, a=250.01, index=0)
                entidade1 = Entity(x=203.48, y=95.54, a=250.01, index=1)
                entidade2 = Entity(x=205, y=32, a=180, index=2)
                entidade3 = Entity(x=155, y=140, a=180, index=3)
                entidade4 = Entity(x=180, y=95, a=-90, index=4)
            replacement.place_all(
                [entidade0, entidade1, entidade2, entidade3, entidade4]
            )

        elif ref_data["foul"] == 4:
            if ref_data["yellow"] == False:  # Defensivo
                entidade0 = Entity(x=203.48, y=84.44, a=90, index=0)
                entidade1 = Entity(x=203.48, y=94.55, a=90, index=1)
                entidade2 = Entity(x=150, y=75, a=150, index=2)
                entidade3 = Entity(x=150, y=105, a=-150, index=3)
                entidade4 = Entity(x=155, y=90, a=180, index=4)
            else:  # Ofensivo
                entidade0 = Entity(x=203.48, y=84.44, a=90, index=0)
                entidade1 = Entity(x=203.48, y=94.55, a=90, index=1)
                entidade2 = Entity(x=170, y=70, a=180, index=2)
                entidade3 = Entity(x=130, y=120, a=180, index=3)
                entidade4 = Entity(x=135, y=80, a=135, index=4)
            replacement.place_all(
                [entidade0, entidade1, entidade2, entidade3, entidade4]
            )
