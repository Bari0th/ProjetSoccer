"""
We only define compute_strategy here and ways to create strategies from them
"""
import soccersimulator as soc

from .soccer import action as act
from .soccer import strategy_encapsulator as strat

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


class FonceurBehavior(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Fonceur", act.RunToPredictBall(), act.StrongShootToGoal())

class AttaquantBehavior(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Attaquant", act.RunToPredictBall(), act.ShootToMoveToGoal())
    def updateActions(self, super_state):
        if super_state.player_pos.distance(super_state.opp_goal) > 30:
            self.changeShootAction(act.ShootToMoveToGoal())
        else : 
            self.changeShootAction(act.StrongShootToGoal())

        
class GoalBehaviorTeam(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Goal", act.RunToDefensivePos(), act.ShootToNearestAlly())

    def updateActions(self, super_state):
        if super_state.is_ball_nearest :
            self.changeMoveAction(act.RunToPredictBall())
            if ((super_state.opp_goal - super_state.player_pos).angle - (super_state.nearest_ally.position - super_state.player_pos).angle) < math.pi/4:
                self.changeShootAction(act.ShootToNearestAllyFarFromOpponent())
            elif ((super_state.player_pos - super_state.opp_goal).norm < 30) and not(super_state.is_opp_goal_nearer_than_opp):
                self.changeShootAction(act.StrongShootToGoal())
            else :
                self.changeShootAction(act.ShootToMoveToGoal())

        else :
            self.changeMoveAction(act.RunToDefensivePos())
            self.changeShootAction(act.ShootToGoal())   


class GoalBehaviorAlone(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Goal", act.RunToDefensivePos(), act.ShootToCornerFarFromOpp())

    def updateActions(self, super_state):
        if super_state.ball_in_corner:
            self.changeMoveAction(act.RunToDefensivePos())
            self.changeShootAction(act.ShootToCornerFarFromOpp())
        elif super_state.is_ball_nearest :
            self.changeMoveAction(act.RunToPredictBall())
            if not(super_state.is_opp_goal_nearer_than_opp) :
                self.changeShootAction(act.ShootToMoveToGoal())
            else : 
                self.changeShootAction(act.ShootToCornerFarFromOpp())
        else :
            self.changeMoveAction(act.RunToDefensivePos())
            self.changeShootAction(act.ShootToCornerFarFromOpp())