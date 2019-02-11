import soccersimulator as soc

class Move(object):
	def __init__(self,superstate):
		self.superstate = superstate

	@property
	def run_to_ball(self):
		return soc.SoccerAction( acceleration = self.superstate.vect_play_ball)

	@property
	def run_to_predict_ball(self):
		return soc.SoccerAction( acceleration = (self.superstate.vect_play_ball + self.superstate.ball_vit * 5 * self.superstate.coeff_distance) )

	@property
	def run_to_defensive_pos(self):
		return soc.SoccerAction(acceleration = (self.superstate.defensive_pos + self.superstate.ball_pos - self.superstate.player_pos))


class Shoot(object):
	def __init__(self,superstate):
		self.superstate = superstate

	@property
	def shoot_to_goal(self):
		"""
		Plus la peine de s'embeter avec le can shoot
		"""
		return soc.SoccerAction( shoot = ((self.superstate.opp_goal - self.superstate.player_pos).normalize() * 3) )

	@property
	def shoot_to_nearest_ally(self):
		return soc.SoccerAction( shoot = (self.superstate.nearest_ally.position - self.superstate.player_pos).normalize() * 6)