"""
We only define compute_strategy here and ways to create strategies from them
"""
import lib.adpater as ad
from lib import strategy_encapsulator as strat
from lib import soccertools as ut
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

        def compute_acc(self, game_state):
            ball = game_state.ball
            player = game_state.player

            direction = ut.MyVector2D.getDirection(player.position, ball.position)

            return direction * soc.settings.maxPlayerAcceleration

        def compute_shoot(self, game_state):
            ball = game_state.ball
            directionToGoal = ut.MyVector2D.getDirection(ball.position, game_state.getTheOtherGoal.middle)
            return directionToGoal * 5

class GoalBehaviorBallOwner(strat.StrategyBehavior):
    def __init__(self):
        strat.StrategyBehavior.__init__(self, "Goal")

    def compute_acc(self, game_state):
        posBall = game_state.ball.position + game_state.ball.vitesse * 5
        return ad.runThere( game_state.player, posBall)

    def compute_shoot(self, game_state):
        force = 10
        return ad.calculShoot(game_state, force)

class GoalBehaviorNotBallOwner(strat.StrategyBehavior):
    def __init__(self):
        strat.StrategyBehavior.__init__(self, "Goal")

    def compute_acc(self, game_state):
        ourGoal = ad.getOurGoal(game_state)
        posBall = game_state.ball.position
        
        goalTop = ourGoal + soc.Vector2D(0,soc.settings.GAME_GOAL_HEIGHT/2.)
        goalBot = ourGoal - soc.Vector2D(0,soc.settings.GAME_GOAL_HEIGHT/2.)
        
        ballToGoalTop = goalTop - posBall
        ballToGoalBot = goalBot - posBall
        angle = (ballToGoalTop.angle + ballToGoalBot.angle)/2.
        vect = soc.Vector2D(norm = 1./math.cos(angle)*ballToGoalBot.x/2., angle = angle)
        
        move = ad.goThere(game_state.player, vect+posBall)
        return move
    def compute_shoot(self, game_state):
        return soc.Vector2D(0,0)


class GoalBehavior(strat.StrategyBehavior):
    def __init__(self):
        strat.StrategyBehavior.__init__(self, "Goal")
        self.ballOwner = GoalBehaviorBallOwner()
        self.notBallOwner = GoalBehaviorNotBallOwner()

    def compute_acc(self, game_state):
        if ad.isBallOwner(game_state):
            return self.ballOwner.compute_acc(game_state)

        return self.notBallOwner.compute_acc(game_state)

    def compute_shoot(self, game_state):
        if ad.isBallOwner(game_state):
            return self.ballOwner.compute_shoot(game_state)

        return self.notBallOwner.compute_shoot(game_state)