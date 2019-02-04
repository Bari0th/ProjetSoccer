from soccersimulator import *
from math import *
from 

class Move(object):
    def __init__(self,superstate):
        self.superstate = superstate
    
    def __getattr__(self,attr):
        return getattr(self.superstate, attr)

    @property
    def run_to_ball(self):
        return SoccerAction( acceleration = self.vect_play_ball.norm )

    @property
    def run_to_predict_ball(self):
        return SoccerAction( acceleration = self.vect_play_ball.norm + self.ballVit * 5 * self.coeff_distance )

    @property
    def run_to_defensive_pos(self):
        return SoccerAction(acceleration = Vector2D(norm = (self.ally_goal - self.ballPos).x / acos(state.angle_median_ally_goal(self.ballPos)), angle = state.angle_median_ally_goal(self.ballPos)))


class Shoot(object):
    def __init__(self,superstate):
        self.superstate = superstate

    def __getattr__(self,attr):
        return getattr(self.superstate, attr)

    @property
    def shoot_to_goal(self):
        if self.can_shoot:
            return SoccerAction( shoot = ((self.opp_goal - self.playerPos).normalize * 3) )
        return SoccerAction()

    @property
    def shoot_to_nearest_ally(self):
        if self.can_shoot:
            return SoccerAction( shoot = (self.nearest_ally - self.playerPos).normalize * 6)
        return SoccerAction()