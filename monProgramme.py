from math import *
from soccersimulator import *
from mesStrategies import *

gaul1 = Player("Gaul 1", StrategyGoal())
fonceur1 = Player("Fonceur 1 bis", StrategyFonceurBis())
team1 = SoccerTeam("equipe 1", [fonceur1, gaul1])
gaul2 = Player("Gaul 2", StrategyFonceur())
fonceur2 = Player("Fonceur 2", StrategyFonceur())
team2 = SoccerTeam("equipe 1", [gaul2, fonceur2])
match = Simulation(team1, team2, 2000)
match.start()
show_simu(match)

