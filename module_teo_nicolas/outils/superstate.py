from soccersimulator import *
from math import *

class SuperState(object):
	def __init__(self, state, id_team, id_player):
		self.state = state
		self.it = id_team
		self.ip = id_player
		self.key = lambda r: r[0]
	
	def __getattr__(self,attr):
		return getattr(self.state, attr)

	@property
	def ball(self):
		return self.state.ball

	@property
	def ball_pos(self):
		return self.ball.position

	@property
	def ball_vit(self):
		return self.ball.vitesse

	def nearest_player(pos, player_list):
		return min([(player.position.distance(pos), player) for player in player_list])[1]
	
	@property	
	def player(self):
		return self.player_state(self.it,self.ip)
	
	@property	
	def player_pos(self):
		return self.player_state(self.it,self.ip).position
	
	@property	
	def player_vit(self):
		return self.player_state(self.it,self.ip).vitesse

	
	
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
		return [self.player_state(it,ip) for (it,ip) in self.state.players]
		
	@property
	def allies(self):
		return [self.player_state(it,ip) for (it,ip) in self.players if (it == self.it and ip != self.ip)]
		
	@property
	def all_allies(self):
		return [self.player_state(it,ip) for (it,ip) in self.players if it == self.it]
		
	@property
	def opponents(self):
		return [self.player_state(it,ip) for (it,ip) in self.players if it != self.it]

	@property
	def vect_play_ball(self):
		return self.ball_pos - self.player_pos

	@property
	def dist_play_ball(self):
		return self.vect_play_ball.norm
	
	@property
	def can_shoot(self):
		return self.dist_play_ball <= (BALL_RADIUS + PLAYER_RADIUS)

	@property
	def opp_goal(self):
		return Vector2D(GAME_WIDTH * (self.it % 2), GAME_HEIGHT/2)
	
	@property
	def ally_goal(self):
		return Vector2D(GAME_WIDTH * (self.it - 1), GAME_HEIGHT/2)

	@property
	def is_ball_nearest(self):
		return self.player == self.nearest_ball_player

	@property
	def coeff_distance(self):
		if self.dist_play_ball > 40 : return 1.
		return self.dist_play_ball / 40.

	@property
	def ally_goal_top(self):
		return self.ally_goal + Vector2D(0,GAME_GOAL_HEIGHT/2.)

	@property
	def ally_goal_bot(self):
		return self.ally_goal - Vector2D(0,GAME_GOAL_HEIGHT/2.)

	@property
	def opp_goal_top(self):
		return self.opp_goal + Vector2D(0,GAME_GOAL_HEIGHT/2.)

	@property
	def opp_goal_bot(self):
		return self.opp_goal - Vector2D(0,GAME_GOAL_HEIGHT/2.)

	@property
	def defensive_pos(self):
		return Vector2D(norm = ((self.ally_goal - self.ball_pos).x / 2. ) / cos(self.angle_median_ally_goal(self.ball_pos)), angle = self.angle_median_ally_goal(self.ball_pos))

	def angle_median_ally_goal(self, pos):
		return (((self.ally_goal_top - pos).angle + (self.ally_goal_bot - pos).angle) / 2.) % (2.*pi)

	def angle_median_opp_goal(self, pos):
		return (((self.opp_goal_top - pos).angle + (self.opp_goal_bot - pos).angle ) / 2.) % (2.*pi)


		
