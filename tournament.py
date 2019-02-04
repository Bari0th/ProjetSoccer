from soccersimulator import SoccerTeam
from module_teo_nicolas import *

def get_team ( nb_players ):
    team = SoccerTeam ( name = " Nicolas / Téo ")
    if nb_players == 1:
        team.add ( " fonceur " , StrategyFonceur())
    if nb_players == 2:
        team.add ( " fonceur " , StrategyFonceur())
        team.add ( " gaul " , StrategyGoal())
    return team