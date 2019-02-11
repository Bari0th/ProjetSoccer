from soccersimulator import SoccerTeam
from module_teo_nicolas import lib.action
from module_teo_nicolas import lib.strategy_encapsulator

def get_team ( nb_players ):
	team = SoccerTeam ( name = " Nicolas / Téo ")
	if nb_players == 1:
		team.add ( " goal " , SimpleStrategy(GoalBehavior()))
	if nb_players == 2:
		team.add ( " fonceur bis" , SimpleStrategy(FonceurBehavior()))
		team.add ( " gaul " , SimpleStrategy(GoalBehavior()))
	return team

if __name__ == '__main__':
	team1 = get_team(1)
	team2 = SoccerTeam("equipe 1", [Player("FonceurBis", FonceurBehavior())])
	match = Simulation(team1, team2, 2000)
	match.start()
	show_simu(match)
	team1 = get_team(2)
	team2 = SoccerTeam("equipe 1", [Player("Fonceur", FonceurBehavior()), Player("FonceurBis", FonceurBehavior())])
	match = Simulation(team1, team2, 2000)
	match.start()
	show_simu(match)
