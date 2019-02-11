import soccersimulator as soc

class MyVector2D:
    @staticmethod
    def getDirection(fromVector, toVector):
        vec = (toVector - fromVector)
        vec.normalize()
        return vec

class GameState:
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
    
    def canShoot(self):
        """
        Returns true only if the player is within the range of the ball
        """
        distance = self.ball.position.distance(self.player.position)
        return distance <= soc.settings.PLAYER_RADIUS + soc.settings.BALL_RADIUS

    @property
    def getMyGoal(self):
        """
        Returns a GoalData
        """
        return self.terrainData.getMyGoal(self.id_team)

    @property
    def getTheOtherGoal(self):
        """
        Returns a GoalData
        """
        return self.terrainData.getTheOtherGoal(self.id_team)

    @property
    def ball(self):
        """
        Returns a MobileMixin
        """
        return self.state.ball

    @property
    def player(self):
        """
        Returns a MobileMixin
        """
        return self.state.player_state(self.id_team, self.id_player)

    @property
    def terrainData(self):
        return TerrainData.getInstance()
        
class GoalData:
    """
    Get data about the goal : its height, range, pos, center etc.
    """
    def __init__(self, team_id):
        assert team_id in [1,2]
        if team_id == 1 :
            self.x_range = soc.Vector2D(0,0)
            self.middle = soc.Vector2D(0, soc.settings.GAME_HEIGHT/2)
        else :
            self.x_range = soc.Vector2D(soc.settings.GAME_WIDTH, soc.settings.GAME_WIDTH)
            self.middle = soc.Vector2D(soc.settings.GAME_WIDTH, soc.settings.GAME_HEIGHT/2)

        self.y_range = (soc.Vector2D(-1, 1) * soc.settings.GAME_GOAL_HEIGHT + soc.Vector2D(1, 1) * soc.settings.GAME_HEIGHT) / 2
        self.height = soc.settings.GAME_GOAL_HEIGHT

    def __repr__(self):
        return "min : {} max : {} middle : {}".format(self.x_range, self.y_range, self.middle)
class TerrainData:

    terrain = None

    def __init__(self):
        """
        Singleton to get some data about the terrain such as its width, height, center, the goals etc.
        """
        self.width = soc.settings.GAME_WIDTH
        self.height = soc.settings.GAME_HEIGHT
        self.center = soc.Vector2D(self.width, self.height) / 2
        self.goals = [GoalData(1), GoalData(2)]

    @staticmethod
    def getInstance():
        if not TerrainData.terrain :
            TerrainData.terrain = TerrainData()
        return TerrainData.terrain

    def getMyGoal(self, id_team):
        assert id_team in [1,2]
        return self.goals[id_team - 1]

    def getTheOtherGoal(self, id_team):
        assert id_team in [1,2]
        if id_team == 1 :
            return self.getMyGoal(2)
        return self.getMyGoal(1)


if __name__ == "__main__":
    pass