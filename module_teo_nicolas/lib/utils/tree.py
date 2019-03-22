from . import json

class Node:
    def __init__(self, val=None, children = []):
        self.val = val
        self.children = children

class SoccerTree:
    def __init__(self, all_coords, nbPlayersPerTeam, dimensions):
        nb_combi = len(all_coords) ** (nbPlayersPerTeam * 2 + 1)
        assert nb_combi <= 11000000, "Nombre de combinaisons plus petit que 11 millions (current : {})".format(nb_combi)
        self.root = Node()
        self.nbPlayersPerTeam = nbPlayersPerTeam
        self.dimensions = dimensions

        self._LoadPaths(all_coords)
        

    def CreateTree(self, all_coords, current, step=1):
        if step > self.nbPlayersPerTeam * 2 + 1 :
            return
        for coord in all_coords:
            node = Node(coord, [])
            current.children.append(node)

        for child in current.children:
            self.CreateTree(all_coords, child, step+1)

    def GetPaths(self, current):
        retLists = []
        if(len(current.children) == 0):
            leafList = []
            leafList.append(current.val)
            retLists.append(leafList)
        else :
            for child in current.children :
                nodeLists = self.GetPaths(child)
                for nodeList in nodeLists:
                    if current.val is not None :
                        nodeList.insert(0, current.val)
                    retLists.append(nodeList)

        return retLists

    def getKeysFromPaths(self, paths):
        """
        Optimize keys; may be able to do it directly in GetPaths
        """
        dico = dict()
        for path in paths :
            dico[SoccerTree.OptimizePath(self.nbPlayersPerTeam, path)] = True

        return list(dico.keys())

    def _LoadPaths(self, all_coords):
        self.CreateTree(all_coords, self.root)
        self.paths = self.getKeysFromPaths(self.GetPaths(self.root))
    
    @staticmethod
    def OptimizePath(nbPlayersPerTeam, path):
        team1 = path[1 : nbPlayersPerTeam] # ignore 1st player
        ball = [path[len(path) - 1]]
        team2 = path[nbPlayersPerTeam : len(path) - 1]

        team1.sort()
        team2.sort()
        return tuple([path[0]] + team1 + team2 + ball)