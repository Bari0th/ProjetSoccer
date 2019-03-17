from module_teo_nicolas.lib.soccergen import AlgoGen
from module_teo_nicolas.lib.utils.tree import SoccerTree
from module_teo_nicolas.lib.soccer.discretizedterrain import DiscretizedTerrain

nb_player_per_team = 2

d = DiscretizedTerrain.getInstance()
all_coords = d.AllPossibleCoords()
tree = SoccerTree(all_coords, nb_player_per_team)
paths = tree.paths

algo = AlgoGen.getInstance()

for path in paths :
    algo.Train(path, nb_player_per_team, show=True)