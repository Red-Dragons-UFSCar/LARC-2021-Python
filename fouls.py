import random
from simClasses import Ball
from bridge import (Entity)


# % ID of each foul

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

'''
Input: Replacer client, data from referee, team color (True = Yellow, False = Blue) and foul ID.
Description: Our robots are replaced in diferents places of the field according to the fouls
(using position on X, Y, angle and index of each robot).
Output: Entity objects.
'''

def replacement_fouls(replacement, ref_data, mray, op, dp):
    ball = Ball()

    if not mray: # Blue side
        if ref_data["foul"] == 1: # Penalty kick
            if ref_data["yellow"]:  # Defensive
                if dp == "direct":
                    angle = 0
                elif dp == "spin" or dp == "spin-v":
                    angle = 90
                entidade0 = Entity(x=14, y=65, a=angle, index=0) # Goalkeeper
                entidade1 = Entity(x=90, y=40, a=180, index=1) # Center back
                entidade2 = Entity(x=90, y=90, a=0, index=2) # Striker

            else:  # Ofensive
                entidade0 = Entity(x=17.5, y=65, a=0, index=0)
                if op == "direct" or op == "switch":
                    entidade1 = Entity(x=80, y=70, a=0, index=1)
                    entidade2 = Entity(x=117.5, y=65-1.7-2, a=22, index=2)
                elif op == "spin":
                    r = random.uniform(0, 1) # Generate random number between 0 and 1
                    if r < 0.001: # 0.5 is default value
                        entidade1 = Entity(x=80, y=60, a=0, index=1)
                        entidade2 = Entity(x=105, y=85, a=-50, index=2)
                    else:
                        entidade1 = Entity(x=80, y=70, a=0, index=1)
                        entidade2 = Entity(x=105, y=45, a=50, index=2)
            '''
            else:  # Ofensive
                r = random.uniform(0, 1) # Generate random number between 0 and 1
                if r < 0.5:
                    entidade0 = Entity(x=17.5, y=65, a=0, index=0)
                    entidade1 = Entity(x=80, y=60, a=0, index=1)
                    # entidade2 = Entity(x=115, y=68,a=-15, index=2) # Uncoment to use default penalty
                    entidade2 = Entity(x=105, y=85, a=-50, index=2)
                else:
                    entidade0 = Entity(x=17.5, y=65, a=0, index=0)
                    entidade1 = Entity(x=80, y=70, a=0, index=1)
                    # entidade2 = Entity(x=115, y=62,a=15, index=2) # Uncoment to use default penalty
                    entidade2 = Entity(x=105, y=45, a=50, index=2)
            '''
            replacement.place_all([entidade0, entidade1, entidade2]) # Replace each robot

        # TODO FOULS: Revisar as posições futuramente do goalKick
        elif ref_data["foul"] == 2:
            if not ref_data["yellow"]:
                entidade0 = Entity(x=15, y=58,a=0, index=0)
                entidade1 = Entity(x=15, y=20,a=30, index=1)
                entidade2 = Entity(x=47.5, y=66,a=0, index=2)
            else:
                entidade0 = Entity(x=17.5, y=65, a=0, index=0)
                entidade1 = Entity(x=85, y=85,a=0, index=1)
                #if ball.yPos < 65:
                entidade2 = Entity(x=85, y=45,a=180, index=2)
            replacement.place_all([entidade0, entidade1, entidade2])

        elif ref_data["foul"] == 3: # Freeball
            if ref_data["quad"] == 1: # First quadrant
                entidade0 = Entity(x=17.5, y=65, a=0, index=0)
                entidade1 = Entity(x=80, y=90, a=0, index=1)
                entidade2 = Entity(x=104.5, y=107, a=0, index=2)
            elif ref_data["quad"] == 2: # Second quadrant
                entidade0 = Entity(x=17.5, y=72.5, a=0, index=0)
                entidade1 = Entity(x=27.5, y=101, a=0, index=1)
                entidade2 = Entity(x=30, y=60, a=0, index=2)
            elif ref_data["quad"] == 3: # Third quadrant
                entidade0 = Entity(x=17.5, y=57.5, a=0, index=0)
                entidade1 = Entity(x=27.5, y=24, a=0, index=1)
                entidade2 = Entity(x=30, y=70, a=0, index=2)
            elif ref_data["quad"] == 4: # Fourth quadrant
                entidade0 = Entity(x=17.5, y=65, a=0, index=0)
                entidade1 = Entity(x=80, y=40, a=180, index=1)
                entidade2 = Entity(x=102.5, y=22, a=0, index=2)
            replacement.place_all([entidade0, entidade1, entidade2]) # Replace each robot

        elif ref_data["foul"] == 4: #Kickoff
            if ref_data["yellow"]: # Defensive
                entidade0 = Entity(x=17.5, y=65, a=0, index=0)
                entidade1 = Entity(x=69, y=85, a=330, index=1)
                entidade2 = Entity(x=61, y=65, a=0, index=2)
            else: # Ofensive
                entidade0 = Entity(x=17.5, y=65, a=0, index=0)
                # Kickoff normal - Transformar em estrategia selecionavel?
                entidade1 = Entity(x=73, y=88, a=330, index=1)
                entidade2 = Entity(x=75, y=58, a=25, index=2)

                #entidade1 = Entity(x=73.5, y=110.3, a=328, index=1)
                #entidade2 = Entity(x=79, y=63, a=25, index=2)
            replacement.place_all([entidade0, entidade1, entidade2]) # Replace each robot

    if mray: # Yellow side
        if ref_data["foul"] == 1:
            if not ref_data["yellow"]: # Defensive
                if dp == "direct":
                    angle = 0
                elif dp == "spin" or dp == "spin-v":
                    angle = 90
                entidade0 = Entity(x=156, y=65, a=angle, index=0)
                entidade1 = Entity(x=80, y=90, a=180, index=1)
                entidade2 = Entity(x=80, y=40, a=180, index=2)
            else:  # Ofensive
                entidade0 = Entity(x=152.5, y=65, a=180, index=0)
                if op == "direct" or op == "switch":
                    entidade1 = Entity(x=90, y=70, a=0, index=1)
                    entidade2 = Entity(x=52.5, y=61.3, a=158, index=2)
                elif op == "spin":
                    if random.uniform(0, 1) < 0.999: # Generate random number between 0 and 1
                        entidade1 = Entity(x=90, y=60, a=0, index=1)
                        entidade2 = Entity(x=65, y=85, a=-130, index=2)
                    else:
                        entidade1 = Entity(x=90, y=70, a=0, index=1)
                        entidade2 = Entity(x=65, y=45, a=130, index=2)
            replacement.place_all([entidade0, entidade1, entidade2]) # Replace each robot

        elif ref_data["foul"] == 2:
            if ref_data["yellow"]:
                entidade0 = Entity(x=152.5, y=58, a=180, index=0)
                entidade1 = Entity(x=153, y=22,a=150, index=1)
                entidade2 = Entity(x=122, y=63,a=0, index=2)
            else:
                entidade0 = Entity(x=152.5, y=65, a=180, index=0)
                entidade1 = Entity(x=85, y=85,a=180, index=1)
                #ball = Ball()
                #if ball.yPos < 65:
                entidade2 = Entity(x=85, y=45,a=180, index=2)
            replacement.place_all([entidade0, entidade1, entidade2])

        elif ref_data["foul"] == 3: # Freeball
            if ref_data["quad"] == 1: # First quadrant
                entidade0 = Entity(x=152.5, y=72.5, a=180, index=0)
                entidade1 = Entity(x=142.5, y=101, a=180, index=1)
                entidade2 = Entity(x=135, y=60, a=180, index=2)
            elif ref_data["quad"] == 2: # Second quadrant
                entidade0 = Entity(x=152.5, y=65, a=180, index=0)
                entidade1 = Entity(x=90, y=90, a=180, index=1)
                entidade2 = Entity(x=67.5, y=107, a=180, index=2)
            elif ref_data["quad"] == 3: # Third quadrant
                entidade0 = Entity(x=152.5, y=65, a=180, index=0)
                entidade1 = Entity(x=90, y=40, a=180, index=1)
                entidade2 = Entity(x=67.5, y=22, a=180, index=2)
            elif ref_data["quad"] == 4: # Fourth quadrant
                entidade0 = Entity(x=152, y=57.5, a=180, index=0)
                entidade1 = Entity(x=142, y=28, a=180, index=1)
                entidade2 = Entity(x=135, y=70, a=180, index=2)
            replacement.place_all([entidade0, entidade1, entidade2]) # Replace each robot

        elif ref_data["foul"] == 4: # Kickoff
            if not ref_data["yellow"]: # Defensive
                entidade0 = Entity(x=152, y=65, a=180, index=0)
                entidade1 = Entity(x=91, y=89, a=240, index=1)
                entidade2 = Entity(x=109, y=65, a=180, index=2)
            else: # Ofensive
                # Kickoff normal - Transformar em estrategia selecionavel?
                #entidade0 = Entity(x=152, y=65, a=180, index=0)
                #entidade1 = Entity(x=93, y=88, a=210, index=1)
                #entidade2 = Entity(x=95, y=58, a=155, index=2)

                entidade0 = Entity(x=152, y=65, a=180, index=0)
                entidade1 = Entity(x=96.5, y=110.3, a=212, index=1)
                entidade2 = Entity(x=91, y=63, a=155, index=2)

            replacement.place_all([entidade0, entidade1, entidade2]) # Replace each robot