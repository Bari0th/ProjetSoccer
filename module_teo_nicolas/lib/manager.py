from .soccer import action as act
from .soccer import soccertools as ut
from .soccer import strategy_encapsulator as strat

class Manager:

    manager = None

    def __init__(self, it):
        """
        Singleton to compute the next actions for all players each tick
        """
        self.currentStep = -1
        self.nextActions = []
        self.ourTeam = it
        self.possibleActions = act.getAllActions()

    @staticmethod
    def getInstance(id_team):
        if not Manager.manager :
            Manager.manager = Manager(id_team)
        return Manager.manager

    def getNextActions(self, state, id_player):
        assert id_player in [0,1,2,3]
        if state.step > self.currentStep :
            self._computeNextActions(state)
        return self.nextActions[id_player]

    def _computeNextActions(self, state):
        self.currentStep = state.step
        self.nextActions = [[act.DontMove(), act.DontShoot()], [act.DontMove(), act.DontShoot()], [act.DontMove(), act.DontShoot()], [act.DontMove(), act.DontShoot()]]


if __name__ == "__main__":
    pass