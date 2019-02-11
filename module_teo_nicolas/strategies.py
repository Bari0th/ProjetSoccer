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
            strat.StrategyBehavior.__init__(self, "Fonceur")
    
    def compute_acc(self, super_state):
        move = act.Move(super_state)
        return move.run_to_predict_ball

    def compute_shoot(self, super_state):
        shoot = act.Shoot(super_state)
        return shoot.shoot_to_goal

        
class GoalBehavior(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Goal")

    def compute_acc(self, super_state):
        move = act.Move(super_state)
        if super_state.is_ball_nearest :
            return move.run_to_predict_ball
        return move.run_to_defensive_pos

    def compute_shoot(self, super_state):
        shoot = act.Shoot(super_state)
        if super_state.is_ball_nearest :
            return shoot.shoot_to_goal
        return shoot.shoot_to_nearest_ally