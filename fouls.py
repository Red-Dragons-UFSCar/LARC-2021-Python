import random

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

def replacement_fouls(replacement, ref_data, mray):
    

    if not mray: # Blue side
        if ref_data["foul"] == 1: # Penalty kick
            if ref_data["yellow"]:  # Defensive
                entidade0 = Entity(x=13.75, y=65, a=0, index=0) # Goalkeeper
                entidade1 = Entity(x=96, y=25, a=180, index=1) # Center back
                entidade2 = Entity(x=96, y=90, a=0, index=2) # Striker
            else:  # Ofensive
                r = random.uniform(0, 1) # Generate random number between 0 and 1
                if r < 0.5:
                    entidade0 = Entity(x=17.5, y=65, a=0, index=0)
                    entidade1 = Entity(x=73.75, y=105, a=0, index=1)
                    # entidade2 = Entity(x=115, y=68,a=-15, index=2) # Uncoment to use default penalty
                    entidade2 = Entity(x=105, y=85, a=-50, index=2)
                else:
                    entidade0 = Entity(x=17.5, y=65, a=0, index=0)
                    entidade1 = Entity(x=73.75, y=105, a=0, index=1)
                    # entidade2 = Entity(x=115, y=62,a=15, index=2) # Uncoment to use default penalty
                    entidade2 = Entity(x=105, y=45, a=50, index=2)
                replacement.place_all([entidade0, entidade1, entidade2]) # Replace each robot

        # TODO FOULS: Revisar as posições futuramente do goalKick
        # elif ref_data["foul"] == 2:
        # entidade0 = Entity(x=50, y=100,a=0, index=0)
        # entidade1 = Entity(x=50, y=60,a=0, index=1)
        # entidade2 = Entity(x=50, y=20,a=0, index=2)
        # replacement.place_all([entidade0, entidade1, entidade2])

        elif ref_data["foul"] == 3: # Freeball
            if ref_data["quad"] == 1: # First quadrant
                entidade0 = Entity(x=17.5, y=65, a=0, index=0)
                entidade1 = Entity(x=95, y=45, a=0, index=1)
                entidade2 = Entity(x=102.5, y=105, a=0, index=2)
            elif ref_data["quad"] == 2: # Second quadrant
                entidade0 = Entity(x=17.5, y=72.5, a=0, index=0)
                entidade1 = Entity(x=27.5, y=105, a=0, index=1)
                entidade2 = Entity(x=55, y=55, a=0, index=2)
            elif ref_data["quad"] == 3: # Third quadrant
                entidade0 = Entity(x=17.5, y=57.5, a=0, index=0)
                entidade1 = Entity(x=27.5, y=25, a=0, index=1)
                entidade2 = Entity(x=55, y=75, a=0, index=2)
            elif ref_data["quad"] == 4: # Fourth quadrant
                entidade0 = Entity(x=17.5, y=65, a=0, index=0)
                entidade1 = Entity(x=95, y=85, a=180, index=1)
                entidade2 = Entity(x=102.5, y=25, a=0, index=2)
            replacement.place_all([entidade0, entidade1, entidade2]) # Replace each robot

        elif ref_data["foul"] == 4: #Kickoff
            entidade0 = Entity(x=17.5, y=65, a=0, index=0)
            entidade1 = Entity(x=45, y=65, a=0, index=1)
            entidade2 = Entity(x=61, y=65, a=0, index=2)
            replacement.place_all([entidade0, entidade1, entidade2]) # Replace each robot

    if mray: # Yellow side
        if ref_data["foul"] == 1:  # Defensive
            if not ref_data["yellow"]: # Generate random number between 0 and 1
                entidade0 = Entity(x=156, y=65, a=180, index=0)
                entidade1 = Entity(x=65, y=80, a=180, index=1)
                entidade2 = Entity(x=62.5, y=65, a=180, index=2)
            else:  # Ofensive
                if random.uniform(0, 1) < 0.5:
                    entidade0 = Entity(x=152.5, y=65, a=180, index=0)
                    entidade1 = Entity(x=90, y=65, a=0, index=1)
                    # entidade2 = Entity(x=55, y=68,a=-165, index=2) # Uncoment to use default penalty
                    entidade2 = Entity(x=65, y=85, a=-130, index=2)
                else:
                    entidade0 = Entity(x=152.5, y=65, a=180, index=0)
                    entidade1 = Entity(x=90, y=65, a=0, index=1)
                    # entidade2 = Entity(x=55, y=62,a=165, index=2) # Uncoment to use default penalty
                    entidade2 = Entity(x=65, y=45, a=130, index=2)
            replacement.place_all([entidade0, entidade1, entidade2]) # Replace each robot

        # elif ref_data["foul"] == 2:
        # entidade0 = Entity(x=50, y=100,a=0, index=0)
        # entidade1 = Entity(x=50, y=60,a=0, index=1)
        # entidade2 = Entity(x=50, y=20,a=0, index=2)
        # replacement.place_all([entidade0, entidade1, entidade2])

        elif ref_data["foul"] == 3: # Freeball
            if ref_data["quad"] == 1: # First quadrant
                entidade0 = Entity(x=152.5, y=72.5, a=180, index=0)
                entidade1 = Entity(x=142.5, y=105, a=180, index=1)
                entidade2 = Entity(x=115, y=55, a=180, index=2)
            elif ref_data["quad"] == 2: # Second quadrant
                entidade0 = Entity(x=152.5, y=65, a=180, index=0)
                entidade1 = Entity(x=100, y=65, a=180, index=1)
                entidade2 = Entity(x=67.5, y=105, a=180, index=2)
            elif ref_data["quad"] == 3: # Third quadrant
                entidade0 = Entity(x=152.5, y=65, a=180, index=0)
                entidade1 = Entity(x=100, y=65, a=180, index=1)
                entidade2 = Entity(x=67.5, y=25, a=180, index=2)
            elif ref_data["quad"] == 4: # Fourth quadrant
                entidade0 = Entity(x=152, y=57.5, a=180, index=0)
                entidade1 = Entity(x=142, y=25, a=180, index=1)
                entidade2 = Entity(x=115, y=75, a=180, index=2)
            replacement.place_all([entidade0, entidade1, entidade2]) # Replace each robot

        elif ref_data["foul"] == 4: # Kickoff
            entidade0 = Entity(x=152, y=65, a=180, index=0)
            entidade1 = Entity(x=125, y=65, a=180, index=1)
            entidade2 = Entity(x=109, y=65, a=180, index=2)
            replacement.place_all([entidade0, entidade1, entidade2]) # Replace each robot
