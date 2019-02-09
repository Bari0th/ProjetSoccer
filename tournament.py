from soccersimulator import SoccerTeam
from module_teo_nicolas import *

def get_team ( nb_players ):
	team = SoccerTeam ( name = " Nicolas / Téo ")
	if nb_players == 1:
		team.add ( " fonceur " , StrategyGoal())
	if nb_players == 2:
		team.add ( " fonceur bis" , StrategyFonceurBis())
		team.add ( " gaul " , StrategyGoal())
	return team

if __name__ == '__main__':
	team1 = get_team(1)
	team2 = SoccerTeam("equipe 1", [Player("FonceurBis", StrategyFonceurBis())])
	match = Simulation(team1, team2, 2000)
	match.start()
	show_simu(match)
	team1 = get_team(2)
	team2 = SoccerTeam("equipe 1", [Player("Fonceur", StrategyFonceur()), Player("FonceurBis", StrategyFonceurBis())])
	match = Simulation(team1, team2, 2000)
	match.start()
	show_simu(match)