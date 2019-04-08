
import soccersimulator as soc
import math
from module_teo.lib import strategies as st
from volleyball_question2 import StrategyAttaque

from module_teo.lib.soccer import action as act
from module_teo.lib.soccer import strategy_encapsulator as strat

class StrategyDefense(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Echauffement", act.RunToPredictBall(), act.ShootFarFromOpp())

    def updateActions(self, super_state):
        if super_state.ball_in_my_part :
            self.changeMoveAction(act.RunToPredictBall())
        else :
            self.changeMoveAction(act.SmartReplace())

if __name__ == '__main__':
    team1 = soc.SoccerTeam ( name = "Bumper")
    team2 = soc.SoccerTeam ( name = "Glouteur")
    team1.add ( "Bumper 1" , st.createStrategy(StrategyDefense()))
    team2.add ( "Glouteur 1" , st.createStrategy(StrategyAttaque()))



    simu = soc.VolleySimulation(team1, team2)
    soc.volley_show_simu(simu)