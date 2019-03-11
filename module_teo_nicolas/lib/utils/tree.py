class Node:
    def __init__(self, val=None, children = []):
        self.val = val
        self.children = children

class SoccerTree:
    def __init__(self, all_coords, nbPlayersPerTeam):
        self.root = Node()
        self.nbPlayersPerTeam = nbPlayersPerTeam

        self.CreateTree(all_coords, self.root)
        self.paths = self.GetPaths(self.root)

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