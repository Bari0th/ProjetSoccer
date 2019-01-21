from math import *
from soccersimulator import *
from mesStrategies import *

joueur1 = Player("joueur 1", StrategyFonceur())
joueur2 = Player("joueur 2", StrategyFonceur())
team1 = SoccerTeam("equipe 1", [joueur1, joueur2])
team2 = team1.copy()
match = Simulation(team1, team2, 2000)
match.start()
show_simu(match)

