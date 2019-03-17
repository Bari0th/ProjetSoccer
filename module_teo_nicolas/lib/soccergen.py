import soccersimulator as soc
from .utils.json import encode_json, decode_json
from .soccer import discretizedterrain as d_terrain
from .soccer import action as act
from . import strategies as strats
import random

class AlgoGen :
    algo = None

    def __init__(self):
        self.possibleActions = act.getAllActions()
        self.simu = None
        self.currentPath = None
        self.nb_player_per_team = 0

        # genetic
        self.nb_iterations = 50
        self.nb_individuals = 20
        self.genome_size = 10
        self.steps_per_action = 20
        self.curr_ind_index = 0

        self.max_round_step = self.steps_per_action * self.genome_size # steps to test on individual
        self.steps_per_iteration = self.nb_individuals * self.max_round_step 
        self.max_steps = self.steps_per_iteration * self.nb_iterations # steps to test all individuals * nb_iterations

        try:
            self.data = decode_json("IA_DATA")
        except FileNotFoundError:
            self.data = {
                "1" : dict(),
                "2" : dict(),
                "3" : dict(),
                "4" : dict(),
                "shoots" : self.possibleActions["shoots"]["names"],
                "moves" : self.possibleActions["moves"]["names"]
            }

    @staticmethod
    def getInstance():
        if not AlgoGen.algo :
            AlgoGen.algo = AlgoGen()
        return AlgoGen.algo

    def getData(self, id_team, nb_player_per_team, path):
        assert nb_player_per_team in [1,2,3,4]
        dimension = d_terrain.DiscretizedTerrain.getInstance().getDimension()
        key = self._computeKey(path)

        if dimension in self.data[str(nb_player_per_team)]:
            if key in self.data[str(nb_player_per_team)][str(dimension)] :
                return self.data[str(nb_player_per_team)][str(dimension)][key][str(id_team)]

        return [[act.DontMove(), act.DontShoot()]] * nb_player_per_team

    def testSave(self):
        encode_json(self.data, "test")

    def testLoad(self):
        data = decode_json("test")
        return data

    def _computeKey(self, path):
        key = ""
        for case in path:
            key += str(case)

        return key

    def Train(self, path, nb_player_per_team, show=False):
        self.currentPath = path
        self.nb_player_per_team = nb_player_per_team

        team1 = soc.SoccerTeam("Team␣1") 
        team2 = soc.SoccerTeam("Team␣2")

        for i in range(nb_player_per_team):
            behavior = strats.TraineeBehavior()
            strat = strats.createStrategy(behavior)
            team1.add(strat.name + " " + str(i), strat)

            if(nb_player_per_team == 1):
                strat = strats.createStrategy(strats.GoalBehaviorAlone())
            else :
                strat = strats.createStrategy(strats.GoalBehaviorTeam())
            team2.add(strat.name + " " + str(i), strat)

        self.simu = soc.Simulation(team1, team2, max_steps=self.max_steps) 
        self.simu.listeners += self

        if show: 
            soc.show_simu(self.simu) 
        else: 
            self.simu.start()

    def get_ith_player_behavior(self, team, i):
        return team.players[i].strategy.behavior

    def get_current_gene_for_ith_player(self, i, step):
        current_iter = self.get_current_iteration_index(step)
        move_index, shoot_index = self.population[i][current_iter]
        actMove = self.possibleActions["moves"][self.data["moves"][move_index]]()
        actShoot = self.possibleActions["shoots"][self.data["shoots"][shoot_index]]()
        return actMove, actShoot

    def get_current_iteration_index(self, step):
        return step // self.steps_per_iteration

    def begin_match(self, team1, team2, state):

        self.last_step = 0

        self.res = dict() # Dictionary of results

        self.key = self._computeKey(self.currentPath)

        # initilaiser la population
        self.population = []
        shoots_len = len(self.data["shoots"])
        moves_len = len(self.data["moves"])
        for i in range (self.nb_individuals) :
            individual = []
            for j in range(self.genome_size):
                gene = (random.randrange(0, moves_len), random.randrange(0, shoots_len))
                individual.append(gene)

            self.population.append(individual)

    def begin_round(self, team1, team2, state):
        for i in range (len(self.currentPath)):
            coord = self.currentPath[i]
            pos = d_terrain.DiscretizedTerrain.getInstance().FromCaseToPosition(coord)
            if i < self.nb_player_per_team : #team1
                self.simu.state.states[(1, i)].position = pos
                m, s = self.get_current_gene_for_ith_player(i, self.simu.step)
                self.get_ith_player_behavior(team1, i).changeMoveAction(m)
                self.get_ith_player_behavior(team1, i).changeShootAction(s)
            elif i == len(self.currentPath) - 1 : #ball
                self.simu.state.ball.position = pos
            else : #team2
                self.simu.state.states[(2, i - self.nb_player_per_team)].position = pos

        self.last_step = self.simu.step # Last step of the game
        
    def update_round(self, team1, team2, state): # Stop the round if it is too long 
        if state.step > self.last_step + self.max_round_step: 
            self.simu.end_round()

    def end_round(self, team1, team2, state): 
        # A round ends when there is a goal of if max step is achieved 
        if state.goal > 0: 
            self.criterion += 1 # Increment criterion
        self.cpt_trials += 1 # Increment number of trials

        print("Crit:␣{}␣␣␣Cpt:␣{}".format(self.criterion, self.cpt_trials))
        if self.cpt_trials >= self.trials: # Save the result 
            self.res[tuple(self.cur_param.items())] = self.criterion / self.trials
        # Reset parameters 
        self.criterion = 0 
        self.cpt_trials = 0
        # Next parameter value 
        """
        if self.cur_param is not None: 
            self.simu.end_match()
        """

if __name__ == "__main__":
    a = AlgoGen.getInstance()
    encode_json(a.data, "test")
    data = decode_json("test")
    print(data["1"])