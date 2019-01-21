from math import *
from soccersimulator import *

class StrategyFonceur(Strategy):
	def _init_(self, name="Fonceur"):
		self.name = name

	def compute_strategy(self, state, id_team, id_player):
		if id_team == 1 :
			goal = Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
		else : goal = Vector2D(0, GAME_HEIGHT/2)
		
		acceleration = 0.1
		
		posPlayer = state.player_state(id_team, id_player).position
		posBall = state.ball.position
		
		force = 1

		move = posBall - posPlayer
		move.normalize() 

		shoot = goal - posPlayer
		shoot.normalize()

		return SoccerAction(move * acceleration, shoot * force)
