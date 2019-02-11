import soccersimulator as soc

class Action:
	def __init__(self, superstate, name):
		self.superstate = superstate
		self.name = name
	def computeAction(self):
		return soc.SoccerAction()

class Move(Action):
	def __init__(self, superstate, name):
		Action.__init__(self, superstate, name)

class Shoot(Action):
	def __init__(self, superstate, name):
		Action.__init__(self, superstate, name)

class RunToBall(Move):
	def __init__(self, superstate):
		Move.__init__(self, superstate, "RunToBall")

	def computeAction(self):
		return soc.SoccerAction( acceleration = self.superstate.vect_play_ball)

class RunToPredictBall(Move):
	def __init__(self, superstate):
		Move.__init__(self, superstate, "RunToPredictBall")
	def computeAction(self):
		return soc.SoccerAction( acceleration = (self.superstate.vect_play_ball + self.superstate.ball_vit * 5 * self.superstate.coeff_distance) )

class RunToDefensivePos(Move):
	def __init__(self, superstate):
		Move.__init__(self, superstate, "RunToDefensivePos")
	def computeAction(self):
		return soc.SoccerAction(acceleration = (self.superstate.defensive_pos + self.superstate.ball_pos - self.superstate.player_pos))

class ShootToGoal(Shoot):
	def __init__(self, superstate):
		Shoot.__init__(self, superstate, "ShootToGoal")
	def computeAction(self):
		return soc.SoccerAction( shoot = ((self.superstate.opp_goal - self.superstate.player_pos).normalize() * 3) )

class ShootToNearestAlly(Shoot):
	def __init__(self, superstate):
		Shoot.__init__(self, superstate, "ShootToNearestAlly")
	def computeAction(self):
		return soc.SoccerAction( shoot = (self.superstate.nearest_ally.position - self.superstate.player_pos).normalize() * 6)