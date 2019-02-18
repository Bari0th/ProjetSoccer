import math

import soccersimulator as soc


class MyVector2D:
    @staticmethod
    def getDirection(fromVector, toVector):
        vec = (toVector - fromVector)
        vec.normalize()
        return vec

class SuperState:
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.it = id_team
        self.ip = id_player
        self.key = lambda r: r[0]

    @property
    def can_shoot(self):
        """
        Returns true only if the player is within the range of the ball
        """
        return self.dist_play_ball <= soc.settings.PLAYER_RADIUS + soc.settings.BALL_RADIUS

    @property
    def getMyGoal(self):
        """
        Returns a GoalData
        """
        return self.terrainData.getMyGoal(self.it)

    @property
    def getTheOtherGoal(self):
        """
        Returns a GoalData
        """
        return self.terrainData.getTheOtherGoal(self.it)

    @property
    def ball(self):
        """
        Returns a MobileMixin
        """
        return self.state.ball
        
    @property
    def ball_pos(self):
        return self.ball.position

    @property
    def ball_vit(self):
        return self.ball.vitesse

    @staticmethod
    def nearest_player(pos, player_list):
        return min([(player.position.distance(pos), player) for player in player_list])[1]

    @property
    def player(self):
        """
        Returns a MobileMixin
        """
        return self.state.player_state(self.it, self.ip)

    @property	
    def player_pos(self):
        return self.state.player_state(self.it,self.ip).position
	
    @property	
    def player_vit(self):
        return self.state.player_state(self.it,self.ip).vitesse

    @property	
    def nearest_opp(self):
        return min([(opp.position.distance(self.player_pos), opp) for opp in self.opponents], key=self.key)[1]
		
    @property	
    def nearest_ally(self):
        return min([(ally.position.distance(self.player_pos), ally) for ally in self.allies], key=self.key)[1]
		
    @property
    def nearest_player(self):
        return min([(player.position.distance(self.player_pos), player) for player in self.players], key=self.key)[1]

    @property
    def nearest_ball_all_allies(self):
        return min([(ally.position.distance(self.ball_pos), ally) for ally in self.all_allies], key=self.key)[1]

    @property
    def nearest_ball_ally(self):
        return min([(ally.position.distance(self.ball_pos), ally) for ally in self.allies], key=self.key)[1]
	
    @property	
    def nearest_ball_opp(self):
        return min([(opp.position.distance(self.ball_pos), opp) for opp in self.opponents], key=self.key)[1]
		
    @property
    def nearest_ball_player(self):
        return min([(player.position.distance(self.ball_pos), player) for player in self.players], key=self.key)[1]
		
    @property
    def players(self):
        return [self.state.player_state(it,ip) for (it,ip) in self.state.players]
		
    @property
    def allies(self):
        return [self.state.player_state(it,ip) for (it,ip) in self.state.players if (it == self.it and ip != self.ip)]
		
    @property
    def all_allies(self):
        return [self.state.player_state(it,ip) for (it,ip) in self.state.players if it == self.it]
		
    @property
    def opponents(self):
        return [self.state.player_state(it,ip) for (it,ip) in self.state.players if it != self.it]

    @property
    def vect_play_ball(self):
        return self.ball_pos - self.player_pos

    @property
    def dist_play_ball(self):
        return self.vect_play_ball.norm

    @property
    def opp_goal(self):
        return self.getTheOtherGoal.vector    
        
    @property	
    def nearest_opp_goal_opp(self):
        return min([(opp.position.distance(self.opp_goal), opp) for opp in self.opponents], key=self.key)[1]

    @property
    def is_opp_goal_nearer_than_opp(self):
        return (self.player_pos.distance(self.opp_goal) - self.nearest_opp_goal_opp.position.distance(self.opp_goal)) > 0
	
    @property
    def ally_goal(self):
        return self.getMyGoal.vector

    @property
    def is_ball_nearest(self):
        return (self.player_pos.distance(self.ball_pos) + 0.5 < self.nearest_ball_opp.position.distance(self.ball_pos)) and (self.player_pos.distance(self.ball_pos) <= self.nearest_ball_all_allies.position.distance(self.ball_pos) )

    @property
    def coeff_distance(self):
        if self.dist_play_ball > 40 : 
            return 1
        return self.dist_play_ball / 40

    @property
    def ally_goal_top(self):
        return self.getMyGoal.top

    @property
    def ally_goal_bot(self):
        return self.getMyGoal.bottom

    @property
    def opp_goal_top(self):
        return self.getTheOtherGoal.top

    @property
    def opp_goal_bot(self):
        return self.getTheOtherGoal.bottom

    @property
    def defensive_pos(self):
        return soc.Vector2D(norm = ((self.ally_goal - self.ball_pos).x / 2. ) / math.cos(self.angle_median_ally_goal(self.ball_pos)), angle = self.angle_median_ally_goal(self.ball_pos))

    def angle_median_ally_goal(self, pos):
        return (((self.ally_goal_top - pos).angle + (self.ally_goal_bot - pos).angle) / 2) % (2 * math.pi)

    def angle_median_opp_goal(self, pos):
        return (((self.opp_goal_top - pos).angle + (self.opp_goal_bot - pos).angle ) / 2) % (2 * math.pi)

    @property
    def terrainData(self):
        return TerrainData.getInstance()

    @property
    def has_an_ally(self):
        return (len(self.allies) > 0)

    @property
    def bot_ally_corner(self):
        return soc.Vector2D((self.it - 1) * 150,90)

    @property
    def top_ally_corner(self):
        return soc.Vector2D((self.it - 1) * 150, 0)

    @property
    def top_opp_corner(self):
        return soc.Vector2D((self.it % 2) * 150,90)

    @property
    def bot_opp_corner(self):
        return soc.Vector2D((self.it % 2) * 150, 0)

    @property
    def ball_in_corner(self):
        return min([self.ball_pos.distance(corner_pos) for corner_pos in [self.top_ally_corner, self.bot_ally_corner]]) < 15


        
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
