from . import json

class SoccerTree:
    def __init__(self, all_coords, nbPlayersPerTeam, dimensions):
        nb_combi = len(all_coords) ** (nbPlayersPerTeam * 2 + 1)
        assert nb_combi <= 11000000, "Nombre de combinaisons plus petit que 11 millions (current : {})".format(nb_combi)
        self.nbPlayersPerTeam = nbPlayersPerTeam
        self.dimensions = dimensions

        self._LoadPaths(all_coords)

    def _LoadPaths(self, all_coords):
        paths = []

        w, h = self.dimensions
        size = w * h 

        if self.nbPlayersPerTeam == 1 :
            for pos_p1 in range(size):
                for pos_p2 in range(size):
                    for pos_ball in range(size):
                        paths.append((all_coords[pos_p1], all_coords[pos_p2], all_coords[pos_ball]))
        elif self.nbPlayersPerTeam == 2 :
            for pos_p1 in range(size):
                for pos_p2 in range(size):
                    for pos_p3 in range(size):
                        for pos_p4 in range(pos_p3,size):
                            for pos_ball in range(size):
                                paths.append((all_coords[pos_p1], all_coords[pos_p2], all_coords[pos_p3], all_coords[pos_p4], all_coords[pos_ball]))
        elif self.nbPlayersPerTeam == 4 :
            for pos_p1 in range(size):
                for pos_p2 in range(size):
                    for pos_p3 in range(pos_p2,size):
                        for pos_p4 in range(pos_p3,size):
                            for pos_p5 in range(size):
                                for pos_p6 in range(pos_p5, size):
                                    for pos_p7 in range(pos_p6, size):
                                        for pos_p8 in range(pos_p7,size):
                                            for pos_ball in range(size):
                                                paths.append((all_coords[pos_p1], all_coords[pos_p2], all_coords[pos_p3], all_coords[pos_p4], all_coords[pos_p5], all_coords[pos_p6], all_coords[pos_p7], all_coords[pos_p8], all_coords[pos_ball]))


        self.paths = paths
    
    @staticmethod
    def OptimizePath(nbPlayersPerTeam, path):
        team1 = path[1 : nbPlayersPerTeam] # ignore 1st player
        ball = [path[len(path) - 1]]
        team2 = path[nbPlayersPerTeam : len(path) - 1]

        team1.sort()
        team2.sort()
        return tuple([path[0]] + team1 + team2 + ball)