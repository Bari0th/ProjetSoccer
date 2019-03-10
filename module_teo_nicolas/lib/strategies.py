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

class AutoBehavior(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Auto", act.DontMove(), act.DontShoot())
            
    def updateActions(self, super_state):
        if super_state.player_pos.distance(super_state.opp_goal) > 30:
            self.changeShootAction(act.ShootToMoveToGoal())
        else : 
            self.changeShootAction(act.StrongShootToGoal())