from .lib.strategies import GoalBehaviorAlone, createStrategy, GoalBehaviorTeam, AttaquantBehavior, AutoBehavior
import soccersimulator as soc

def get_team ( nb_players ):
	team = soc.SoccerTeam ( name = " Inazuma {} ".format(nb_players))
	if nb_players == 1:
		team.add ( " Lone Wolf " , createStrategy(GoalBehaviorAlone()))
	if nb_players == 2:
		team.add ( " SNK " , createStrategy(AttaquantBehavior()))
		team.add ( " Mark Evans " , createStrategy(GoalBehaviorTeam()))
	if nb_players == 4:
		team.add ( " SNK " , createStrategy(AttaquantBehavior()))
		team.add ( " Mark Evans " , createStrategy(GoalBehaviorTeam()))
		team.add ( " Mark Evans " , createStrategy(AttaquantBehavior()))
		team.add ( " Mark Evans " , createStrategy(AutoBehavior()))
	return team