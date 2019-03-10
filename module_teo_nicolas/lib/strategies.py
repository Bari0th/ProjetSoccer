"""
We only define compute_strategy here and ways to create strategies from them
"""
import soccersimulator as soc

from .lib import action as act
from .lib import strategy_encapsulator as strat

from . import manager as man

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
        state = super_state.state
        it = super_state.it
        ip = super_state.ip
        actions = man.Manager.getInstance(it).getNextActions(state, ip)
            
        self.changeShootAction(actions[0])
        self.changeShootAction(actions[1])