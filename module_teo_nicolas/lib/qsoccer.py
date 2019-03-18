from .soccer import discretizedterrain as d_terrain
from .utils.tree import SoccerTree
from .soccer import action as act

class QSoccer:
    algo = None
    def __init__(self, nb_player_per_team):
        self.d_terrain = d_terrain.DiscretizedTerrain.getInstance()
        self.nb_player_per_team = nb_player_per_team

        # create q table and counts
        self.q_table = {}
        self.counts = {}

        states = self._initStateSpace()
        self._initQTableAndCounts(states)
        

    def _initStateSpace(self):
        all_coords = self.d_terrain.AllPossibleCoords()
        tree = SoccerTree(all_coords, self.nb_player_per_team)
        states = list(map(lambda x : tuple(x), tree.paths))
        return states

    def _initQTableAndCounts(self, states):
        possibleActions = act.getAllActions()
        moves = possibleActions["moves"]["names"]
        shoots = possibleActions["shoots"]["names"]

        moves_len = len(moves)
        shoots_len = len(shoots)
        for state in states :
            for i in range(moves_len):
                for j in range(shoots_len):
                    sa = (state, (i , j))
                    self.q_table[sa] = 0.0
                    self.counts[sa] = 0