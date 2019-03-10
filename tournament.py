import soccersimulator as soc
from module_teo_nicolas import get_team

if __name__ == '__main__':
	team1 = get_team(2)
	team2 = get_team(2)
	match = soc.Simulation(team1, team2, 2000)
	match.start()
	soc.show_simu(match)
