from .lib.strategies import GoalBehaviorAlone, createStrategy, GoalBehaviorTeam, AttaquantBehavior
import soccersimulator as soc

def get_team ( nb_players ):
	team = soc.SoccerTeam ( name = " Inazuma {} ".format(nb_players))
	if nb_players == 1:
		team.add ( " Lone Wolf " , createStrategy(GoalBehaviorAlone()))
	if nb_players == 2:
		team.add ( " SNK " , createStrategy(AttaquantBehavior()))
		team.add ( " Mark Evans " , createStrategy(GoalBehaviorTeam()))
	return team