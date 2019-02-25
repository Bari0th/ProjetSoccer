from module_teo_nicolas import strategies as strat
import soccersimulator as soc
from module_teo_nicolas import get_team

if __name__ == '__main__':
	team1 = get_team(1)
	team2 = soc.SoccerTeam("equipe 1", [soc.Player("Fonceur", strat.createStrategy(strat.AttaquantBehavior()))])
	match = soc.Simulation(team1, team2, 2000)
	match.start()
	soc.show_simu(match)
	team1 = get_team(2)
	team2 = soc.SoccerTeam("equipe 1", [soc.Player("Fonceur", strat.createStrategy(strat.GoalBehaviorTeam())), soc.Player("Attaquant", strat.createStrategy(strat.FonceurBehavior()))])
	match = soc.Simulation(team1, team2, 2000)
	match.start()
	soc.show_simu(match)
