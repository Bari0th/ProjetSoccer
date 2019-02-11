
from lib import teo_utils as teo

def isBallOwner(game_state):
    return teo.isBallOwner(game_state.id_player, game_state.id_team, game_state.state)

def calculShoot(game_state, force):
    return teo.calculShoot(game_state.state, game_state.id_team, game_state.id_player, teo.getOpponentGoal(game_state.id_team), force)

def runThere(player, targetedPos):
    return teo.runThere(player, targetedPos)

def getOurGoal(game_state):
    return teo.getOurGoal(game_state.id_team)

def goThere(player, there):
    return teo.goThere(player, there)