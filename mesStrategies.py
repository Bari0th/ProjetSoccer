<<<<<<< HEAD
from math import *
from soccersimulator import *

def getOpponentGoal(id_team):
	if id_team == 1 :
		return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
	else : return Vector2D(0, GAME_HEIGHT/2)
	
def getOurGoal(id_team):
	if id_team == 1 :
		return Vector2D(0, GAME_HEIGHT/2)
	else : return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
	
def getAngle(vector):
	return copysign( acos(vector.x/vector.norm), vector.y) 
	
	
def runThere(player, targetedPos):
	return targetedPos - player.position
	
def goThere(player, targetedPos):
	traj = targetedPos - player.position
	vitesse = player.vitesse
	vitesseNormale = vitesse - vitesse.dot(traj / traj.norm) * (traj / traj.norm)
	if vitesseNormale.norm >= 0 :
		if vitesseNormale.norm >= maxPlayerAcceleration :
			return vitesseNormale * -1.
		else:
			return vitesseNormale * -1. + traj.normalize() * (maxPlayerAcceleration - vitesseNormale.norm)
	
	if getDistanceArret(vitesse.norm) >= traj.norm :
		return -1. * vitesse
	
	return traj
	
def getPlayersList(id_team, state):
	return state.states[id_team]
	
def getDistanceArret(vitesse):
	somme = 0
	while vitesse >= 0:
		somme += vitesse
		vitesse -= maxPlayerAcceleration
	return somme

	
	
class StrategyFonceur(Strategy):
	def _init_(self, name="Fonceur"):
		self.name = name
	
	def compute_strategy(self, state, id_team, id_player):
		goal = getOpponentGoal(id_team)
		
		acceleration = 1
		
		posPlayer = state.player_state(id_team, id_player).position
		posBall = state.ball.position
		
		force = 3.5

		move = runThere( state.player_state(id_team, id_player), posBall)

		shoot = goal - posPlayer
		shoot.normalize()

		return SoccerAction(move * acceleration, shoot * force)
		
class StrategyFonceurBis(Strategy):
	def _init_(self, name="Fonceur"):
		self.name = name
	
	def compute_strategy(self, state, id_team, id_player):
		goal = getOpponentGoal(id_team)
		
		acceleration = 1
		
		posBall = state.ball.position
		
		force = 3.5

		move = goThere( state.player_state(id_team, id_player), posBall)

		shoot = goal - state.player_state(id_team, id_player).position
		shoot.normalize()

		return SoccerAction(move * acceleration, shoot * force)

		
class StrategyGoal(Strategy):
	def _init_(self, name="Defenseur"):
		self.name = name

	def compute_strategy(self, state, id_team, id_player):
		ourGoal = getOurGoal(id_team)
		
		posBall = state.ball.position
		
		goalTop = ourGoal + Vector2D(0,GAME_GOAL_HEIGHT/2.)
		goalBot = ourGoal - Vector2D(0,GAME_GOAL_HEIGHT/2.)
		
		ballToGoalTop = goalTop - posBall
		ballToGoalBot = goalBot - posBall
		
		angle = (getAngle(ballToGoalTop) + getAngle(ballToGoalBot)) / 2.
		
		pos = posBall + Vector2D(angle = angle, norm = posBall.distance(ourGoal) / 2.3)
		
		move = goThere(state.player_state(id_team, id_player), (ballToGoalTop + ballToGoalBot) / 4 + posBall)
		
		return SoccerAction(move, Vector2D(0,0))


		#ajouter l'angle / 2 puis (distance entre but et balle) /2 + posBut

		
=======
from math import *
from soccersimulator import *

def getOpponentGoal(id_team):
	if id_team == 1 :
		return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
	else : return Vector2D(0, GAME_HEIGHT/2)
	
def getOurGoal(id_team):
	if id_team == 1 :
		return Vector2D(0, GAME_HEIGHT/2)
	else : return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
	
def getAngle(vector):
	return copysign( acos(vector.x/vector.norm), vector.y)

def runThere(player, targetedPos):
	return targetedPos - player.position
	
def goThere(player, targetedPos):
	traj = targetedPos - player.position
	vitesse = player.vitesse
	vitesseNormale = vitesse - vitesse.dot(traj / traj.norm) * (traj / traj.norm)
	if vitesseNormale.norm >= 0 :
		if vitesseNormale.norm >= maxPlayerAcceleration :
			return vitesseNormale * -1.
		else:
			return vitesseNormale * -1. + traj.normalize() * (maxPlayerAcceleration - vitesseNormale.norm)
	
	if getDistanceArret(vitesse.norm) >= traj.norm :
		return -1. * vitesse
	
	return traj

def isClosest(player, opponent, posBall):
	return (posBall - player.position).norm < (posBall - opponent.position).norm
	
def getPlayersList(id_team, state):
	return state.states[id_team]

def getOthersPlayers(player, id_team, state):
	return [ ( it , ip ) for ( it , ip ) in state.players if it != id_team or ip != id_player]	

def isBallOwner(player, id_team, state):
	posBall = state.ball.position
	distanceBallPlayer = (posBall - player.position).norm
	playerList = getOthersPlayers(player, id_team, state)
	for otherPlayer in playerList : 
		if (posBall - otherPlayer.position).norm <= distanceBallPlayer:
			return False
	return True
	
	
	
def getDistanceArret(vitesse):
	if vitesse <= 0 or maxPlayerAcceleration <= 0:
		return 0

	somme = 0
	while vitesse >= 0:
		somme += vitesse
		vitesse -= maxPlayerAcceleration
	return somme

	
	
class StrategyFonceur(Strategy):
	def _init_(self, name="Fonceur"):
		self.name = name
	
	def compute_strategy(self, state, id_team, id_player):
		goal = getOpponentGoal(id_team)
		
		acceleration = 1
		
		posPlayer = state.player_state(id_team, id_player).position
		posBall = state.ball.position
		
		force = 3.5

		move = runThere( state.player_state(id_team, id_player), posBall)

		shoot = goal - posPlayer
		shoot.normalize()

		return SoccerAction(move * acceleration, shoot * force)
		
class StrategyFonceurBis(Strategy):
	def _init_(self, name="Fonceur"):
		self.name = name
	
	def compute_strategy(self, state, id_team, id_player):
		goal = getOpponentGoal(id_team)
		
		acceleration = 1
		
		posBall = state.ball.position
		
		force = 3.5

		move = goThere( state.player_state(id_team, id_player), posBall)

		shoot = goal - state.player_state(id_team, id_player).position
		shoot.normalize()

		return SoccerAction(move * acceleration, shoot * force)

		
class StrategyGoal(Strategy):
	def _init_(self, name="Defenseur"):
		self.name = name

	def compute_strategy(self, state, id_team, id_player):
		ourGoal = getOurGoal(id_team)
		
		posBall = state.ball.position
		
		goalTop = ourGoal + Vector2D(0,GAME_GOAL_HEIGHT/2.)
		goalBot = ourGoal - Vector2D(0,GAME_GOAL_HEIGHT/2.)
		
		ballToGoalTop = goalTop - posBall
		ballToGoalBot = goalBot - posBall
		print("Joueur ",id_team," : ", ballToGoalTop.angle)
		angle = (ballToGoalTop.angle + ballToGoalBot.angle)/2.
		vect = Vector2D(norm = ballToGoalTop.x/2., angle = angle)
		
		move = goThere(state.player_state(id_team, id_player), vect+posBall)
		
		return SoccerAction(move, Vector2D(0,0))


		#ajouter l'angle / 2 puis (distance entre but et balle) /2 + posBut

		
>>>>>>> 5f749532cfde274d465200f4e74269f5f3603a87
