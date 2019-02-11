import soccersimulator as soc

class Action:
	def __init__(self, name):
		self.name = name
	def computeAction(self, superstate):
		return soc.SoccerAction()

class Move(Action):
	def __init__(self, name):
		Action.__init__(self, name)

class Shoot(Action):
	def __init__(self, name):
		Action.__init__(self, name)

class RunToBall(Move):
	def __init__(self):
		Move.__init__(self, "RunToBall")

	def computeAction(self, superstate):
		return soc.SoccerAction( acceleration = superstate.vect_play_ball)

class RunToPredictBall(Move):
	def __init__(self):
		Move.__init__(self, "RunToPredictBall")
	def computeAction(self, superstate):
		return soc.SoccerAction( acceleration = (superstate.vect_play_ball + superstate.ball_vit * 5 * superstate.coeff_distance) )

class RunToDefensivePos(Move):
	def __init__(self):
		Move.__init__(self, "RunToDefensivePos")
	def computeAction(self, superstate):
		return soc.SoccerAction(acceleration = (superstate.defensive_pos + superstate.ball_pos - superstate.player_pos))

class ShootToGoal(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootToGoal")
	def computeAction(self, superstate):
		return soc.SoccerAction( shoot = ((superstate.opp_goal - superstate.player_pos).normalize() * 3) )

class ShootToNearestAlly(Shoot):
	def __init__(self):
		Shoot.__init__(self, "ShootToNearestAlly")
	def computeAction(self, superstate):
		return soc.SoccerAction( shoot = (superstate.nearest_ally.position - superstate.player_pos).normalize() * 6)