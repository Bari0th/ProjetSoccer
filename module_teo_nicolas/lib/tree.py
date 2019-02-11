import soccersimulator as soc
from random import randint

names = ["fromage", "gateaux", "fraises", "croissant", "papier wc", "vase", "pain", "Vénus", "Mercure", "Neptune", "Terre", "Mars", "Jupiter", "Saturne", "Uranus", "Pluton"]

def getName():
    if len(names) >= 2 :
        name = names.pop(randint(0, len(names) - 1))
    else :
        name = names[0]

    return name

class Node:
    def __init__(self, val=None, children = []):
        self.val = val
        self.children = children

class SoccerTree:
    def __init__(self, strategies, nbPlayersPerTeam):
        self.root = Node()
        self.nbPlayersPerTeam = nbPlayersPerTeam
        self.teams = []

        self.CreateTree(strategies, self.root)
        self.paths = self.GetPaths(self.root)

    def CreateTree(self, strategies, current, step=1):
        if step > self.nbPlayersPerTeam :
            return
        for strategy in strategies:
            node = Node(strategy, [])
            current.children.append(node)

        for child in current.children:
            self.CreateTree(strategies, child, step+1)

    def GetPaths(self, current):
        retLists = []
        if(len(current.children) == 0):
            leafList = []
            leafList.append(soc.Player(str(current.val),current.val))
            retLists.append(leafList)
        else :
            for child in current.children :
                nodeLists = self.GetPaths(child)
                for nodeList in nodeLists:
                    if current.val is not None :
                        nodeList.insert(0, soc.Player(str(current.val),current.val))
                    retLists.append(nodeList)

        return retLists

    def GetTeams(self):
        teams_dict = dict()
        teams = []
        for path in self.paths:
            key_list = [x.strategy.name for x in path]
            key_list.sort()
            key = "".join(key_list)
            if key not in teams_dict :
                teams.append(soc.SoccerTeam(getName(), path))
                teams_dict[key] = True

        return teams
