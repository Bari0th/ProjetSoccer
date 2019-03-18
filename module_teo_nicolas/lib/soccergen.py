import soccersimulator as soc
from .utils.json import encode_json, decode_json
from .soccer import discretizedterrain as d_terrain
from .soccer import soccertools as tools
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

        self.terrain = tools.TerrainData.getInstance()

        # genetic
        self.nb_iterations = 15
        self.nb_individuals = 10
        self.genome_size = 1
        self.steps_per_action = 30

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
        self.current_individual_index = 0
        self.current_iteration_index = 0
        self.current_gene_index = 0
        self.currentPath = path
        self.nb_player_per_team = nb_player_per_team

        team1 = soc.SoccerTeam("Team␣1") 
        team2 = soc.SoccerTeam("Team␣2")

        for i in range(nb_player_per_team):
            strat = strats.createStrategy(strats.TraineeBehavior())
            team1.add(strat.name + " " + str(i), strat)

            if(nb_player_per_team == 1):
                strat = strats.createStrategy(strats.GoalBehaviorAlone())
            else :
                strat = strats.createStrategy(strats.GoalBehaviorTeam())
            team2.add(strat.name + " " + str(i), strat)

        self.simu = soc.Simulation(team1, team2, max_steps=self.max_steps) 
        self.simu.listeners += self

        print("Path ", path)
        print("max_round_step : {}, steps_per_iteration : {}".format(self.max_round_step, self.steps_per_iteration))

        if show: 
            soc.show_simu(self.simu) 
        else: 
            self.simu.start() 

    def get_ith_player_behavior(self, team, i):
        return team.players[i].strategy.behavior

    def get_current_gene_for_ith_player(self, i, step):
        print("******************")
        print("step " , step, "/", self.max_steps - 1)
        print("current gene ", self.current_gene_index, "/", self.genome_size - 1)
        print("Current individual ", self.current_individual_index, "/", self.nb_individuals - 1)
        print("For player ", i, "/", self.nb_player_per_team - 1)
        print("In team ", 1)
        current_iter = self.current_iteration_index
        print("FOR ITER ", current_iter, "/", self.nb_iterations - 1)
        move_index, shoot_index = self.population[self.current_individual_index][i][self.current_gene_index]
        actMove = self.possibleActions["moves"][self.data["moves"][move_index]]()
        actShoot = self.possibleActions["shoots"][self.data["shoots"][shoot_index]]()
        print(actMove.name, actShoot.name)
        print("******************")
        return actMove, actShoot

    def ResetFitnesses(self):
        for i in range(len(self.fitnesses)):
            self.fitnesses[i] = 0

    def begin_match(self, team1, team2, state):

        self.res = dict() # Dictionary of results

        self.key = self._computeKey(self.currentPath)

        # initialiser la population
        self.population = []
        self.fitnesses = [0] * self.nb_individuals
        shoots_len = len(self.data["shoots"])
        moves_len = len(self.data["moves"])

        for i in range(self.nb_individuals):
            ind = []
            for j in range(self.nb_player_per_team):
                ind.append([])
                for k in range(self.genome_size):
                    gene = (random.randrange(0, moves_len), random.randrange(0, shoots_len))
                    ind[j].append(gene)

            self.population.append(ind)

    def begin_round(self, team1, team2, state):
        print("-------------------BEGIN ROUND--------------------")
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
        
    def update_round(self, team1, team2, state):
        distance_to_goal = self.simu.state.ball.position.distance(self.terrain.getTheOtherGoal(1).vector)
        self.fitnesses[self.current_individual_index] -= distance_to_goal
        print(self.fitnesses)

        if state.step % self.steps_per_action == 0 :
            print("Increment gene")
            self.current_gene_index += 1
            self.current_gene_index %= self.genome_size

            if self.current_gene_index == 0 :
                print("On a fait tous les genes on passe a l'individu suivant")
                self.simu.end_round()
                return

            for i in range (self.nb_player_per_team):
                m, s = self.get_current_gene_for_ith_player(i, self.simu.step)
                self.get_ith_player_behavior(team1, i).changeMoveAction(m)
                self.get_ith_player_behavior(team1, i).changeShootAction(s)

    def end_round(self, team1, team2, state):
        coeff = 3 * self.max_round_step / ((state.step % self.max_round_step) + 1)
        print("coeff ", coeff)
        if state.goal == 1 :
            print("team 1 marque")
            self.fitnesses[self.current_individual_index] += abs(self.fitnesses[self.current_individual_index]) * coeff
        elif state.goal == 2 :
            print("team 2 marque")
            self.fitnesses[self.current_individual_index] -= abs(self.fitnesses[self.current_individual_index]) * coeff
        
        print("Le round est fini, on passe à l'individu suivant et on recommence au premier gene")
        self.current_gene_index = 0
        self.current_individual_index += 1
        self.current_individual_index %= self.nb_individuals
        if self.current_individual_index == 0 :
            print("On a fait le tour des individus, on passe la génération suivante")
            self.current_iteration_index += 1
            self.current_iteration_index %= self.nb_iterations
            if self.current_iteration_index == 0 :
                print("On a fait le tours des iterations, on arrete le match")
                self.simu.end_match()
                return

            

            self.ResetFitnesses()

            
        print("-------------------END ROUND--------------------")
        pass

    def end_match(self, team1, team2, state):
        pass

if __name__ == "__main__":
    a = AlgoGen.getInstance()
    encode_json(a.data, "test")
    data = decode_json("test")
    print(data["1"])