import soccersimulator as soc
from .utils.json import encode_json, decode_json
from .soccer import discretizedterrain as d_terrain
from .soccer import action as act
from . import strategies as strats

class AlgoGen :
    algo = None

    def __init__(self):
        self.possibleActions = act.getAllActions()
        self.max_steps = 1000000
        self.max_round_step = 500
        self.simu = None

        try:
            self.data = decode_json("IA_DATA")
        except FileNotFoundError:
            self.data = {
                "1" : dict(),
                "2" : dict(),
                "3" : dict(),
                "4" : dict()
            }

    @staticmethod
    def getInstance():
        if not AlgoGen.algo :
            AlgoGen.algo = AlgoGen()
        return AlgoGen.algo

    def getData(self, id_team, nb_player_per_team, key):
        assert nb_player_per_team in [1,2,3,4]
        dimension = d_terrain.DiscretizedTerrain.getInstance().getDimension()

        if dimension in self.data[str(nb_player_per_team)]:
            if key in self.data[str(nb_player_per_team)][dimension] :
                return self.data[str(nb_player_per_team)][dimension][key][id_team]

        return [[act.DontMove(), act.DontShoot()]] * nb_player_per_team

    def Train(self, nb_player_per_team, show=False):
        team1 = soc.SoccerTeam("Team␣1") 
        team2 = soc.SoccerTeam("Team␣2")

        for i in range(nb_player_per_team):
            strat = strats.createStrategy(strats.AutoBehavior())
            team1.add(strat.name + " " + str(i), strat)
            strat = strats.createStrategy(strats.AttaquantBehavior())
            team2.add(strat.name + " " + str(i), strat)

        self.simu = soc.Simulation(team1, team2, max_steps=self.max_steps) 
        self.simu.listeners += self

        if show: 
            soc.show_simu(self.simu) 
        else: 
            self.simu.start()

    def begin_match(self, team1, team2, state): 
        self.last_step = 0 # Step of the last round 
        self.criterion = 0 # Criterion to maximize (here, number of goals) 
        self.cpt_trials = 0 # Counter for trials 

        self.res = dict() # Dictionary of results

    

if __name__ == "__main__":
    a = AlgoGen.getInstance()
    encode_json(a.data, "test")
    data = decode_json("test")
    print(data["1"])