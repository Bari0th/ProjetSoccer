import soccersimulator as soc
import random

import module_teo_nicolas.strategies as strats
import module_teo_nicolas.algo_gen.gen as gen

from sklearn.model_selection import ParameterGrid

class GoalSearch(object): 
    def __init__(self, strategyBehavior, simu=None, trials=20, max_steps=1000000, max_round_step=400): 
        self.strategyBehavior = strategyBehavior
        self.simu = simu 
        self.trials = trials 
        self.max_steps = max_steps 
        self.max_round_step = max_round_step
        self.genetic_algo = gen.EvolutionnaryProcess(SoccerProblem, SoccerIndividual)
    def start(self, show=True): 
        if not self.simu: 
            team1 = soc.SoccerTeam("Team␣1") 
            team2 = soc.SoccerTeam("Team␣2")

            strat = strats.createStrategy(self.strategyBehavior())
            team1.add(strat.name, strat) 
            
            team2.add(soc.Strategy().name, soc.Strategy()) 
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

    def begin_round(self, team1, team2, state): 
        vec = soc.Vector2D.create_random(low=0, high=1)
        ball = soc.Vector2D(vec.x * soc.settings.GAME_WIDTH, vec.y * soc.settings.GAME_HEIGHT)

        self.simu.state.states[(1, 0)].position = ball.copy() # Player position 
        self.simu.state.states[(1, 0)].vitesse = soc.Vector2D() # Player acceleration 

        self.simu.state.ball.position = ball.copy() # Ball position

        self.last_step = self.simu.step # Last step of the game

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

    def update_round(self, team1, team2, state): # Stop the round if it is too long 
        if state.step > self.last_step + self.max_round_step: 
            self.simu.end_round()
    def get_res(self):
        return self.res
    def get_best(self): 
        return max(self.res, key=self.res.get)

class SoccerGene:
    def __init__(self, gene=None, name=None, value=None):
        assert gene is not None or (name is not None and value is not None)
        if value and name:
            self.value = value
            self.name = name
        else :
            self.value = gene.value
            self.name = gene.name

    def __repr__(self):
        return "{} : {}".format(self.name, str(self.value))

class SoccerIndividual(gen.Individual):
        def __init__(self, father=None, mother=None):
            gen.Individual.__init__(self)
            self.genome = []
            if father is not None :
                if mother is None :
                    for gene in father.genome :
                        self.genome.append(SoccerGene(gene=gene))
                else :
                    cuttingPoint = random.randint(0, len(father.genome) - 1)
                    for gene in father.genom[:cuttingPoint]:
                        self.genome.append(SoccerGene(gene=gene))
                    for gene in mother.genome :
                        if gene not in self.genome :
                            self.genome.append(SoccerGene(gene=gene))
                
                self.Mutate()
            else :
                self.InitGenome()

        def InitGenome(self):
            pass

        def Mutate(self):
            if(random.random() <= Parameters.mutationsRate):
                index1 = random.randint(0, len(self.genome) - 1)
                gene = self.genome.pop(index1)
                index2 = random.randint(0, len(self.genome) - 1)
                self.genome.insert(index2, gene)

        def Evaluate(self):
            totalKm = 0
            oldGene = None
            for gene in self.genome:
                if oldGene != None :
                    totalKm += gene.getDistance(oldGene)
                oldGene = gene

            totalKm += oldGene.getDistance(self.genome[0])
            self.fitness = totalKm
            return self.fitness


class SoccerProblem :
    @staticmethod
    def Init():
        pass


if __name__ == "__main__":
    strat = strats.AttaquantBehavior
    gs = GoalSearch(strat)
    gs.start()