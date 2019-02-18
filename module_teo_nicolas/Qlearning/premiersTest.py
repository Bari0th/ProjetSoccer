class q_state(object):
    def __init__(self,superstate):
        self.state = superstate
    
    def __getattr__(self, attr):
        return attr(self.state, attr)

    @property
    def centre(self):
        return soc.Vector2D(75,45)

    def distance_to_qfood(self, distance):
        if distance <= 10 :
            return 0
        elif distance <= 20 :
            return 1
        elif distance <= 35 :
            return 2
        elif distance <= 55 :
            return 3
        else :
            return 4

    def position_to_qfood(self, position):
        angle = (5 * (position - self.centre).angle) // pi
        distance = distance_to_qfood(position.distance(self.centre))
        return (distance, angle)

    @property
    def player_qfood(self):
        return self.position_to_qfood(self.player_pos)
    
    @property
    def ball_qfood(self):
        return self.position_to_qfood(self.ball_pos)

    @property
    def opp_qfood(self):
        return self.position_to_qfood(self.nearest_opp.position)
    
    def get_