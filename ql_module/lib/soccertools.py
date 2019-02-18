import math
import numpy as np
import soccersimulator as soc
import random
import tree

class MyVector2D:
    @staticmethod
    def getDirection(fromVector, toVector):
        vec = (toVector - fromVector)
        vec.normalize()
        return vec

class Environment:
    def __init__(self, nb_players_per_team, actions):
        assert 0 <= nb_players_per_team and nb_players_per_team <= 4, "entre 0 et 4 joueurs"
        self.nb_players_per_team = nb_players_per_team
        states = self.GetListOfStates()

        self.q_table = np.zeros([len(states), len(actions)])
        self.epsilon = EpsilonGreedy(0.1, len(actions))

    def GetListOfStates(self):
        terrain = TerrainData.getInstance()
        nx, ny = terrain.NB_CASES
        t = tree.StateTree(self.nb_players_per_team, nx, ny)
        return t.GetStates()


class EpsilonGreedy:
    def __init__(self, epsilon=0.1, n_arms = 1):
        self.epsilon = epsilon
        self.n_arms = n_arms
        self.counts = None
        self.values = None

        self.initialize()

    def initialize(self):
        self.counts = [0 for col in range(self.n_arms)]
        self.values = [0.0 for col in range(self.n_arms)]

    def ind_max(self, x):
        m = max(x)
        return x.index(m)

    def select_arm(self):
        if random.random() > self.epsilon :
            return self.ind_max(self.values)
        return random.randrange(len(self.values))

    def update(self, reward):
        chosen_arm = self.select_arm()
        self.counts[chosen_arm] += 1
        n = self.counts[chosen_arm]

        value = self.values[chosen_arm]
        new_value = ((n-1)/float(n)) * value + (1 / float(n)) * reward
        self.values[chosen_arm] = new_value
        
        
class GoalData:
    """
    Get data about the goal : its height, range, pos, center etc.
    """
    def __init__(self, team_id):
        assert team_id in [1,2]
        self.vector = soc.Vector2D(soc.settings.GAME_WIDTH * (team_id - 1), soc.settings.GAME_HEIGHT / 2)

    def __repr__(self):
        return self.vector

    @property
    def top(self):
        return self.vector + soc.Vector2D(0, soc.settings.GAME_GOAL_HEIGHT/2)

    @property
    def bottom(self):
        return self.vector - soc.Vector2D(0, soc.settings.GAME_GOAL_HEIGHT/2)
        
class TerrainData:

    terrain = None

    def __init__(self):
        """
        Singleton to get some data about the terrain such as its width, height, center, the goals etc.
        """
        self.TAILLE = (soc.settings.GAME_WIDTH, soc.settings.GAME_HEIGHT)
        self.NB_CASES = (3, 2)

        w,h = self.TAILLE
        nw, nh = self.NB_CASES
        self.TAILLE_CASE = (w / nw, h / nh)

        self.center = soc.Vector2D(w, h) / 2
        self.goals = [GoalData(1), GoalData(2)]

    @staticmethod
    def getInstance():
        if not TerrainData.terrain :
            TerrainData.terrain = TerrainData()
        return TerrainData.terrain

    def Discretize(self, position):
        w, h = self.TAILLE_CASE
        X = position.x // w
        Y = position.y // h

        return soc.Vector2D(X, Y)

    def Continoutize(self, position):
        w, h = self.TAILLE_CASE
        X = w * (2 * position.x + 1) * 0.5
        Y = h * (2 * position.y + 1) * 0.5
        return soc.Vector2D(X, Y)


e = Environment(2, [])
print("bb")

