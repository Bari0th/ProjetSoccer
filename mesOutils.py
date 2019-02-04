from math import *
from soccersimulator import *

def canShoot(state, id_team, id_player):
    return (state.ball.position - state.player_state(id_team, id_player).position).norm <= BALL_RADIUS + PLAYER_RADIUS

def calculShoot(state, id_team, id_player, target, strength):
    return (target - state.player_state(id_team, id_player).position).normalize() * strength

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

def getOthersPlayers(id_player, id_team, state):
	return [ state.player_state( it , ip ) for ( it , ip ) in state.players if it != id_team ]	

def isBallOwner(id_player, id_team, state):
	posBall = state.ball.position + state.ball.vitesse * 5
	player = state.player_state(id_team, id_player)
	distanceBallPlayer = (posBall - player.position).norm
	playerList = getOthersPlayers(id_player, id_team, state)
	for otherPlayer in playerList : 
		if (posBall - (otherPlayer.position + otherPlayer.vitesse * 5)).norm <= distanceBallPlayer:
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

def predictDistanceBall(player, state):
	return state.ball.position + state.ball.vitesse * 5 * ((player.position - state.ball.position).norm) / 80.
