from .soccer import action as act
from .soccer import soccertools as ut
from .soccer import strategy_encapsulator as strat
from .soccer import discretizedterrain as d_terrain

from .soccergen import AlgoGen

class Manager:

    manager = None

    def __init__(self, it):
        """
        Singleton to compute the next actions for all players each tick
        """
        self.currentStep = -1
        self.nextActions = []
        self.ourTeam = it

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

        nb_player_per_team = len(state.players) // 2
        path = self._getPath(state)

        actions = AlgoGen.getInstance().getData(self.ourTeam, nb_player_per_team, path)
        self.nextActions = actions

    def _getPath(self, state):
        path = []
        for i in range(1, 3):
            team = [ (it, ip) for (it, ip) in state.players if it == i]
            for it, ip in team :
                p_state = state.player_state(it, ip)
                pos = p_state.position
                case = d_terrain.DiscretizedTerrain.getInstance().FromPositionToCase(pos)
                path.append(case)

        case = d_terrain.DiscretizedTerrain.getInstance().FromPositionToCase(state.ball.position)
        path.append(case)
        return path


if __name__ == "__main__":
    pass