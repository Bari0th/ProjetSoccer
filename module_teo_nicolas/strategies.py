"""
We only define compute_strategy here and ways to create strategies from them
"""
import lib.action as act
import lib.strategy_encapsulator as strat
import lib.soccertools as ut
import soccersimulator as soc
import math

def createStrategy(behavior):
    return strat.SimpleStrategy(behavior)

def createStrategies(behaviors):
    strats = []
    for behavior in behaviors:
        strats.append(strat.SimpleStrategy(behavior))
    return strats

class FonceurBehavior(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, act.RunToPredictBall(), act.ShootToGoal())

        
class GoalBehavior(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, act.RunToDefensivePos(), act.ShootToNearestAlly())