import soccersimulator as soc

class super_state(object):
    def __init__(self, state):
        self.state = state

    def __getattr__(self, attr):
        return getattr(self.state, attr)

    