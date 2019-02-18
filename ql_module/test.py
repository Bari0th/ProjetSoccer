from . import strategies as strat

class SuperState:
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.it = id_team
        self.ip = id_player