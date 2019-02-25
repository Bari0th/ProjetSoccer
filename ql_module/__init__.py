from . import strategies as strat
import soccersimulator as soc

def get_team ( nb_players ):
	team = soc.SoccerTeam ( name = " Nicolas / Téo ")
	if nb_players == 1:
		team.add ( " Goal " , strat.createStrategy(strat.GoalBehavior()))
	if nb_players == 2:
		team.add ( " Attaquant " , strat.createStrategy(strat.FonceurBehavior()))
		team.add ( " Gaul " , strat.createStrategy(strat.GoalBehavior()))
	return team