import strategies as strat
import soccersimulator as soc
from lib import strategy_encapsulator as encap

behavior = strat.FonceurBehavior()

team1 = soc.SoccerTeam(name="Team 1")
team2 = soc.SoccerTeam(name="Team 2")

team1.add("Peter le Fonceur", strat.createStrategy(behavior))  
team2.add("Topher le fonceur", soc.Strategy())

simu = soc.Simulation(team1, team2, 500)

# Simulate and display the match
soc.show_simu(simu)