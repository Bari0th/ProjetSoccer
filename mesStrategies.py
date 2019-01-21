from math import *
from soccersimulator import *

def getGoal(id_team):
	if id_team == 1 :
		return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
	else : return Vector2D(0, GAME_HEIGHT/2)

class StrategyFonceur(Strategy):
	def _init_(self, name="Fonceur"):
		self.name = name
	
	def compute_strategy(self, state, id_team, id_player):
		goal = getGoal(id_team)
		
		acceleration = 1
		
		posPlayer = state.player_state(id_team, id_player).position
		posBall = state.ball.position
		
		force = 3.5

		move = posBall - posPlayer
		move.normalize() 

		shoot = goal - posPlayer
		shoot.normalize()

		return SoccerAction(move * acceleration, shoot * force)

class StrategyGoal(Strategy):
	def _init_(self, name="Defenseur"):
		self.name = name

	def compute_strategy(self, state, id_team, id_player):
		goal = getGoal(id_team)
		
		posBall = state.ball.position

		posPlay = state.player_state(id_team, id_player)

		#ajouter l'angle / 2 puis (distance entre but et balle) /2 + posBut

		
