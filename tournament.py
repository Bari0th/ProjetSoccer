from module_teo_nicolas import strategies as strat
import soccersimulator as soc


def get_team ( nb_players ):
	team = soc.SoccerTeam ( name = " Nicolas / Téo ")
	if nb_players == 1:
		team.add ( " Goal " , strat.createStrategy(strat.GoalBehavior()))
	if nb_players == 2:
		team.add ( " Attaquant " , strat.createStrategy(strat.FonceurBehavior()))
		team.add ( " Gaul " , strat.createStrategy(strat.GoalBehavior()))
	return team

if __name__ == '__main__':
	team1 = get_team(1)
	team2 = soc.SoccerTeam("equipe 1", [soc.Player("Attaquant", strat.createStrategy(strat.FonceurBehavior()))])
	match = soc.Simulation(team1, team2, 2000)
	match.start()
	soc.show_simu(match)
	team1 = get_team(2)
	team2 = soc.SoccerTeam("equipe 1", [soc.Player("Attaquant1", strat.createStrategy(strat.FonceurBehavior())), soc.Player("Attaquant2", strat.createStrategy(strat.FonceurBehavior()))])
	match = soc.Simulation(team1, team2, 2000)
	match.start()
	soc.show_simu(match)
