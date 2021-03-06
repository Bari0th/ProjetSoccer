"""
We only define compute_strategy here and ways to create strategies from them
"""
import soccersimulator as soc
import math

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
        actions = man.Manager.getInstance().getNextActions(state, it, ip)
            
        self.changeMoveAction(actions[0])
        self.changeShootAction(actions[1])

class TraineeBehavior(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Trainee", act.RunToPredictBall(), act.ShootToGoal())

class FonceurBehavior(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Fonceur", act.RunToBall(), act.StrongShootToGoal())

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
            strat.StrategyBehavior.__init__(self, "Goal Team", act.RunToDefensivePos(), act.ShootToNearestAlly())

    def updateActions(self, super_state):
        if super_state.is_ball_nearest :
            self.changeMoveAction(act.RunToPredictBall())
            if ((super_state.opp_goal - super_state.player_pos).angle - (super_state.nearest_ally.position - super_state.player_pos).angle) < math.pi/3:
                self.changeShootAction(act.ShootToNearestAllyFarFromOpponent())
            elif ((super_state.player_pos - super_state.opp_goal).norm < 30) and (super_state.is_opp_goal_nearer):
                self.changeShootAction(act.StrongShootToGoal())
            else :
                self.changeShootAction(act.ShootToMoveToGoal())

        else :
            self.changeShootAction(act.ShootToNearestAllyFarFromOpponent())
            if super_state.is_ball_near_our_goal :
                self.changeMoveAction(act.RunToCloseDefensivePos())
            else :self.changeMoveAction(act.RunToDefensivePos())

class newGoalBehaviorTeam(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Goal", act.RunToDefensivePos(), act.ShootToNearestAlly())

    def updateActions(self, super_state):
        if super_state.is_ball_nearest :
            self.changeMoveAction(act.RunToPredictBall())
            if ((super_state.opp_goal - super_state.player_pos).angle - (super_state.nearest_ally.position - super_state.player_pos).angle) < math.pi/3:
                self.changeShootAction(act.ShootToNearestAllyFarFromOpponent())
            elif ((super_state.player_pos - super_state.opp_goal).norm < 30) and (super_state.is_opp_goal_nearer):
                self.changeShootAction(act.StrongShootToGoal())
            else :
                self.changeShootAction(act.ShootToMoveToGoal())

        else :
            self.changeShootAction(act.ShootToNearestAllyFarFromOpponent())
            self.changeMoveAction(act.RunToCloseDefensivePos())


class GoalBehaviorAlone(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Goal Alone", act.RunToDefensivePos(), act.ShootToCornerFarFromOpp())
            self.oppPos = soc.Vector2D(0,0)
            self.hasMoved = False
            

    def updateActions(self, super_state):
        if not(self.hasMoved):
            if self.oppPos == soc.Vector2D(0,0) :
                self.oppPos = super_state.nearest_opp.position
            elif super_state.nearest_opp.position.distance(self.oppPos) < 1:
                self.oppPos = super_state.nearest_opp.position
                self.changeMoveAction(act.RunToPredictBall())
                if super_state.player_pos.distance(super_state.opp_goal) > 30:
                    self.changeShootAction(act.ShootToMoveToGoal())
                else : 
                    self.changeShootAction(act.StrongShootToGoal())
            else :
                self.hasMoved = True
            
        else :
            self.changeMoveAction(act.RunToDefensivePos()) 
            if super_state.ball_in_corner:
                self.changeMoveAction(act.RunToCloseDefensivePos())
                self.changeShootAction(act.ShootToGoal())
            elif super_state.is_ball_nearest :
                self.changeMoveAction(act.RunToPredictBall())
                if (super_state.is_opp_goal_nearer) :
                    self.changeShootAction(act.ShootToMoveToGoal())
                else : 
                    self.changeShootAction(act.ShootToCornerFarFromOpp())
            else :
                self.changeShootAction(act.ShootToCornerFarFromOpp())
                if super_state.is_ball_near_our_goal :
                    self.changeMoveAction(act.RunToCloseDefensivePos())
                else :self.changeMoveAction(act.RunToDefensivePos())

        
class Att_Def_BehaviorTeam(strat.StrategyBehavior):
    def __init__(self):
            strat.StrategyBehavior.__init__(self, "Att / Def", act.RunToDefensivePos(), act.ShootToNearestAlly())

    def updateActions(self, super_state):
        if super_state.is_ball_nearest :
            self.changeMoveAction(act.RunToPredictBall())
            if super_state.is_opp_goal_nearer:
                if ((super_state.player_pos - super_state.opp_goal).norm < 30):
                    self.changeShootAction(act.StrongShootToGoal())
                else: 
                    self.changeShootAction(act.ShootToMoveToGoal())
            elif super_state.is_attacked:
                self.changeShootAction(act.OffensivePass())
            else :
                self.changeShootAction(act.ShootToOffensivePos())

        elif super_state.is_team_is_ball_nearest:
            self.changeMoveAction(act.MoveToOffensivePos())

        elif super_state.is_from_allies_our_goal_nearest:
            self.changeShootAction(act.ShootToNearestAllyFarFromOpponent())
            if super_state.is_ball_near_our_goal :
                self.changeMoveAction(act.RunToCloseDefensivePos())
            else :self.changeMoveAction(act.RunToDefensivePos())
    




