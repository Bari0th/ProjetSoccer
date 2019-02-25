"""
We only define compute_strategy here and ways to create strategies from them
"""
import math

import soccersimulator as soc

from .lib import action as act
from .lib import soccertools as ut
from .lib import strategy_encapsulator as strat


def createStrategy(behavior):
    return strat.SimpleStrategy(behavior)

def createStrategies(behaviors):
    strats = []
    for behavior in behaviors:
        strats.append(strat.SimpleStrategy(behavior))
    return strats

class FonceurBehavior(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Fonceur", act.RunToPredictBall(), act.ShootToMoveToGoal())
    def updateActions(self, super_state):
        if super_state.player_pos.distance(super_state.ball_pos) > 20:
            self.changeShootAction(act.ShootToMoveToGoal())
        else : 
            self.changeShootAction(act.StrongShootToGoal())

        
class GoalBehavior(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Goal", act.RunToDefensivePos(), act.ShootToNearestAlly())

    def updateActions(self, super_state):
        if super_state.is_ball_nearest :
            self.changeMoveAction(act.RunToPredictBall())
            if super_state.has_an_ally:
                if ((super_state.opp_goal - super_state.player_pos).angle - (super_state.nearest_ally.position - super_state.player_pos).angle) < math.pi/4:
                    self.changeShootAction(act.ShootToNearestAllyFarFromOpponent())
                elif ((super_state.player_pos - super_state.opp_goal).norm < 30) and not(super_state.is_opp_goal_nearer_than_opp):
                    self.changeShootAction(act.StrongShootToGoal())
                else :
                    self.changeShootAction(act.ShootToMoveToGoal())
            else : self.changeShootAction(act.ShootToGoal())

        else :
            self.changeMoveAction(act.RunToDefensivePos())
            self.changeShootAction(act.ShootToGoal())