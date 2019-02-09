from math import *
from soccersimulator import *
from .outils import *

class StrategyFonceur(Strategy):
    def _init_(self, name="Fonceur"):
        self.name = name
    
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state,id_team,id_player)
        move = Move(s)
        shoot = Shoot(s)

        return move.run_to_predict_ball + shoot.shoot_to_goal
        
class StrategyFonceurBis(Strategy):
    def _init_(self, name="Fonceur Bis"):
        self.name = name
    
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        move = Move(s)
        shoot = Shoot(s)
        return move.run_to_ball + shoot.shoot_to_goal

        
class StrategyGoal(Strategy):
    def _init_(self, name="Goal"):
        self.name = name

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        move = Move(s)
        shoot = Shoot(s)
        if s.is_ball_nearest :
            return move.run_to_predict_ball + shoot.shoot_to_goal

        return move.run_to_defensive_pos + shoot.shoot_to_nearest_ally

"""class StrategyAttaquant (Strategy):
    def _init_(self, name="Attaquant"):
        self.name = name

    def compute_strategy(self, state, id_team, id_player):
        
"""
