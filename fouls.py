from numpy import arctan2,pi,sqrt,cos,sin,array,matmul,amin,where,zeros,delete,append,int32
from bridge import (Actuator, Replacer, Vision, Referee,NUM_BOTS, convert_angle, Entity)


def replacement_fouls(replacement, ref_data, mray):
    

    if ref_data["foul"] == 1:
        entidade0 = Entity(x=50, y=100,a=0, index=0)
        entidade1 = Entity(x=50, y=60,a=0, index=1)
        entidade2 = Entity(x=50, y=20,a=0, index=2)
        replacement.place_all([entidade0, entidade1, entidade2])

    elif ref_data["foul"] == 2:
        entidade0 = Entity(x=50, y=100,a=0, index=0)
        entidade1 = Entity(x=50, y=60,a=0, index=1)
        entidade2 = Entity(x=50, y=20,a=0, index=2)
        replacement.place_all([entidade0, entidade1, entidade2])

    elif ref_data["foul"] == 3:
        entidade0 = Entity(x=50, y=100,a=0, index=0)
        entidade1 = Entity(x=50, y=60,a=0, index=1)
        entidade2 = Entity(x=50, y=20,a=0, index=2)
        replacement.place_all([entidade0, entidade1, entidade2])

    elif ref_data["foul"] == 4:
        entidade0 = Entity(x=50, y=100,a=0, index=0)
        entidade1 = Entity(x=50, y=60,a=0, index=1)
        entidade2 = Entity(x=50, y=20,a=0, index=2)
        replacement.place_all([entidade0, entidade1, entidade2])

    elif ref_data["foul"] == 5:
        entidade0 = Entity(x=50, y=100,a=0, index=0)
        entidade1 = Entity(x=50, y=60,a=0, index=1)
        entidade2 = Entity(x=50, y=20,a=0, index=2)
        replacement.place_all([entidade0, entidade1, entidade2])

    elif ref_data["foul"] == 6:
        entidade0 = Entity(x=50, y=100,a=0, index=0)
        entidade1 = Entity(x=50, y=60,a=0, index=1)
        entidade2 = Entity(x=50, y=20,a=0, index=2)
        replacement.place_all([entidade0, entidade1, entidade2])

    elif ref_data["foul"] == 7:
        actuator.stop()
