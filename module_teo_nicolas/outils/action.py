from soccersimulator import *
from math import *

class Move(object):
	def __init__(self,superstate):
		self.superstate = superstate
	
	def __getattr__(self,attr):
		return getattr(self.superstate, attr)

	@property
	def run_to_ball(self):
		return SoccerAction( acceleration = self.vect_play_ball)

	@property
	def run_to_predict_ball(self):
		return SoccerAction( acceleration = (self.vect_play_ball + self.ball_vit * 5 * self.coeff_distance) )

	@property
	def run_to_defensive_pos(self):
		return SoccerAction(acceleration = (self.defensive_pos + self.ball_pos - self.player_pos))


class Shoot(object):
	def __init__(self,superstate):
		self.superstate = superstate

	def __getattr__(self,attr):
		return getattr(self.superstate, attr)

	@property
	def shoot_to_goal(self):
		if self.can_shoot:
			return SoccerAction( shoot = ((self.opp_goal - self.player_pos).normalize() * 3) )
		return SoccerAction()

	@property
	def shoot_to_nearest_ally(self):
		if self.can_shoot:
			return SoccerAction( shoot = (self.nearest_ally.position - self.player_pos).normalize() * 6)
		return SoccerAction()