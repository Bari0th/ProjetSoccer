from math import *
from soccersimulator import *
from mesStrategies import *

team1 = SoccerTeam("equipe 1", [Player("Gaul", StrategyGoal()), Player("Fonceur", StrategyFonceur())])
team2 = SoccerTeam("equipe 1", [Player("Gaul", StrategyGoal()), Player("Fonceur", StrategyFonceur())])
match = Simulation(team1, team2, 2000)
match.start()
show_simu(match)

