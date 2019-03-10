from .lib import action as act
from .lib import soccertools as ut
from .lib import strategy_encapsulator as strat

class Manager:

    manager = None

    def __init__(self):
        """
        Singleton to compute the next actions for all players each tick
        """
        self.currentStep = -1
        self.nextActions = dict()

    @staticmethod
    def getInstance():
        if not Manager.manager :
            Manager.manager = Manager()
        return Manager.manager

    def getNextActions(self, state, id_team):
        assert id_team in [1,2]
        if state.step > self.currentStep :
            self._computeNextActions(state, id_team)
        return self.nextActions

    def _computeNextActions(self, state, id_team):
        self.currentStep += 1
        self.nextActions = dict()


if __name__ == "__main__":
    pass