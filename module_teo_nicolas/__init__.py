from . import strategies as strat
import soccersimulator as soc

def get_team ( nb_players ):
	team = soc.SoccerTeam ( name = " Nicolas / Téo ")
	if nb_players == 1:
		team.add ( " Goal " , strat.createStrategy(strat.GoalBehaviorAlone()))
	if nb_players == 2:
		team.add ( " Attaquant " , strat.createStrategy(strat.AttaquantBehavior()))
		team.add ( " Goal " , strat.createStrategy(strat.newGoalBehaviorTeam()))
	return team