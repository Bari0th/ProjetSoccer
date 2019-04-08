
import soccersimulator as soc
import math
from module_teo.lib import strategies as st
from volleyball_question2 import StrategyAttaque
from volleyball_question3 import StrategyDefense

from module_teo.lib.soccer import action as act
from module_teo.lib.soccer import strategy_encapsulator as strat




class StrategyAttaqueEn1V1(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Echauffement", act.RunToPredictBall(), act.ShootFarFromOpp())
            self.hasshot = False

    def updateActions(self, super_state):
        if super_state.ball_in_my_part :
            if self.hasshot :
                if super_state.ball_vit.norm < 0.1 :
                    self.changeShootAction(act.ShootFarFromOpp())
                else :
                    self.changeShootAction(act.Wait())
            else :
                self.changeMoveAction(act.RunToPredictBall())
                if super_state.far_from_middle :
                    self.changeShootAction(act.GoMiddle())
                else :
                    self.changeShootAction(act.ShootFarFromOpp())
                    if super_state.can_shoot:
                        self.hasshot = True
        else :
            self.hasshot = False
            self.changeMoveAction(act.SmartReplace())


if __name__ == '__main__':
    team1 = soc.SoccerTeam ( name = "Bumper")
    team2 = soc.SoccerTeam ( name = "Glouteur")
    team1.add ( "Bumper 1" , st.createStrategy(StrategyAttaqueEn1V1()))
    team2.add ( "Glouteur 1" , st.createStrategy(StrategyAttaqueEn1V1()))



    simu = soc.VolleySimulation(team1, team2)
    soc.volley_show_simu(simu)