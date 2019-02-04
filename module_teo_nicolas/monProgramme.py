from math import *
from soccersimulator import *
from outils import *
from mesStrategies import *


team1 = SoccerTeam("equipe 1", [Player("Gaul", StrategyGoal()), Player("Fonceur", StrategyFonceurBis())])
team2 = SoccerTeam("equipe 1", [Player("Fonceur", StrategyFonceur()), Player("FonceurBis", StrategyFonceurBis())])
match = Simulation(team1, team2, 2000)
match.start()
show_simu(match)

