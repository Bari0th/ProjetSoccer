from math import *
from soccersimulator import *
from mesOutils import *

class StrategyFonceur(Strategy):
	def _init_(self, name="Fonceur"):
		self.name = name
	
	def compute_strategy(self, state, id_team, id_player):
		goal = getOpponentGoal(id_team)
		
		acceleration = 1
		
		posPlayer = state.player_state(id_team, id_player).position
		posBall = state.ball.position + state.ball.vitesse * 10
		
		force = 3.5

		move = runThere( state.player_state(id_team, id_player), posBall)

		shoot = Vector2D(0, 0)
		if canShoot(state, id_team, id_player) :
			shoot = calculShoot(state, id_team, id_player, getOpponentGoal(id_team), force)
		return SoccerAction(move, shoot)
		
class StrategyFonceurBis(Strategy):
	def _init_(self, name="Fonceur Bis"):
		self.name = name
	
	def compute_strategy(self, state, id_team, id_player):
		goal = getOpponentGoal(id_team)
		
		acceleration = 1
		
		posBall = state.ball.position + state.ball.vitesse * 10
		
		force = 3.5

		move = runThere( state.player_state(id_team, id_player), posBall)

		shoot = Vector2D(0, 0)
		if canShoot(state, id_team, id_player) :
			shoot = calculShoot(state, id_team, id_player, getOpponentGoal(id_team), force)
		return SoccerAction(move, shoot)

		
class StrategyGoal(Strategy):
	def _init_(self, name="Defenseur"):
		self.name = name

	def compute_strategy(self, state, id_team, id_player):
	
		if isBallOwner(id_player, id_team, state) :
			goal = getOpponentGoal(id_team)
			force = 10
			posBall = state.ball.position + state.ball.vitesse * 5
			move = runThere( state.player_state(id_team, id_player), posBall)
			shoot = Vector2D(0, 0)
			if canShoot(state, id_team, id_player) :
				shoot = calculShoot(state, id_team, id_player, getOpponentGoal(id_team), force)
			return SoccerAction(move, shoot)
			
		ourGoal = getOurGoal(id_team)
		posBall = state.ball.position
		
		goalTop = ourGoal + Vector2D(0,GAME_GOAL_HEIGHT/2.)
		goalBot = ourGoal - Vector2D(0,GAME_GOAL_HEIGHT/2.)
		
		ballToGoalTop = goalTop - posBall
		ballToGoalBot = goalBot - posBall
		angle = (ballToGoalTop.angle + ballToGoalBot.angle)/2.
		vect = Vector2D(norm = 1./cos(angle)*ballToGoalBot.x/2., angle = angle)
		
		move = goThere(state.player_state(id_team, id_player), vect+posBall)
		
		return SoccerAction(move, Vector2D(0,0))


		#ajouter l'angle / 2 puis (distance entre but et balle) /2 + posBut
