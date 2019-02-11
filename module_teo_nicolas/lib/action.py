import soccersimulator as soc

class Action:
	def __init__(self, superstate):
		self.superstate = superstate
	def computeAction(self):
		return soc.SoccerAction()

class Move(Action):
	pass

class Shoot(Action):
	pass

class RunToBall(Move):
	def computeAction(self):
		return soc.SoccerAction( acceleration = self.superstate.vect_play_ball)

class RunToPredictBall(Move):
	def computeAction(self):
		return soc.SoccerAction( acceleration = (self.superstate.vect_play_ball + self.superstate.ball_vit * 5 * self.superstate.coeff_distance) )

class RunToDefensivePos(Move):
	def computeAction(self):
		return soc.SoccerAction(acceleration = (self.superstate.defensive_pos + self.superstate.ball_pos - self.superstate.player_pos))

class ShootToGoal(Shoot):
	def computeAction(self):
		return soc.SoccerAction( shoot = ((self.superstate.opp_goal - self.superstate.player_pos).normalize() * 3) )

class ShootToNearestAlly(Shoot):
	def computeAction(self):
		return soc.SoccerAction( shoot = (self.superstate.nearest_ally.position - self.superstate.player_pos).normalize() * 6)