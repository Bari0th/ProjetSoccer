from .lib.strategies import AutoBehavior, createStrategy
import soccersimulator as soc

def get_team ( nb_players ):
	team = soc.SoccerTeam ( name = " Nicolas / Téo ")
	if nb_players == 1:
		team.add ( " Auto " , createStrategy(AutoBehavior()))
	if nb_players == 2:
		team.add ( " Auto 1 " , createStrategy(AutoBehavior()))
		team.add ( " Auto 2 " , createStrategy(AutoBehavior()))
	return team