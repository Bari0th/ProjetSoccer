import abc
import soccersimulator as soc
from lib import soccertools as ut

class SimpleStrategy(soc.Strategy):
    def __init__(self, strategyBehavior):
        soc.Strategy.__init__(self, strategyBehavior.name)
        self.behavior = strategyBehavior

    def compute_strategy(self, state, id_team, id_player):
        game_state = ut.GameState(state, id_team, id_player)
        acc = self.behavior.get_acc(game_state)
        shoot = self.behavior.get_shoot(game_state)
        return soc.SoccerAction(acc, shoot)

class StrategyBehavior(metaclass=abc.ABCMeta):
    def __init__(self, name):
        """
        Redefine compute_acc and compute_shoot
        You don't have to care about if you can shoot or not
        """
        self.name = name
    @abc.abstractmethod
    def compute_acc(self, game_state):
        pass
    @abc.abstractmethod
    def compute_shoot(self, game_state):
        pass

    def get_acc(self, game_state):
        return self.compute_acc(game_state)

    def get_shoot(self, game_state):
        if(game_state.canShoot()):
            return self.compute_shoot(game_state)
        return soc.Vector2D()
