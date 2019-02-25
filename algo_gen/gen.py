import parameters
import random

class Individual :
    def __init__(self):
        self.fitness = -1
        self.genome = []

    def Mutate(self):
        pass

    def Evaluate(self):
        pass

    def __repr__(self):
        s = "{} : {}".format(self.fitness, "-".join(self.genome))
        return s

    def __str__(self):
        return self.__repr__()

    def __lt__ (self, other):
        return self.fitness < other.fitness

    def __gt__ (self, other):
        return self.fitness > other.fitness

    def __eq__ (self, other):
        return self.fitness == other.fitness

    def __ne__ (self, other):
        return not self.__eq__(other)

class IndividualFactory:
    factory = None
    @staticmethod
    def getInstance():
        if not IndividualFactory.factory :
            IndividualFactory.factory = IndividualFactory()
        return IndividualFactory.factory

    def Init(self, type):
        pass

    def getIndividual(self, type, father=None, mother=None):
        ind = None
        return ind



class EvolutionnaryProcess:
    def __init__(self, problem):
        IndividualFactory.getInstance().Init(problem)
        self.population = []
        self.generationNb = 0
        self.bestFitness = 0
        self.problem = problem

        for i in range(parameters.Parameters.individualsNb):
            self.population.append(IndividualFactory.getInstance().getIndividual(problem))


    def Survival(self, newGen):
        self.population = newGen

    def Selection(self):
        totalRanks = parameters.Parameters.individualsNb * (parameters.Parameters.individualsNb + 1) // 2
        rand = random.randint(1, totalRanks)
        nbParts = parameters.Parameters.individualsNb
        totalParts = 0
        indIndex = 0

        while totalParts < rand :
            indIndex += 1
            totalParts += nbParts
            nbParts -= 1

        self.population.sort()
        return self.population[indIndex]

    def Run(self):
        self.bestFitness = parameters.Parameters.minFitness + 1
        while (self.generationNb < parameters.Parameters.generationMaxNb and self.bestFitness > parameters.Parameters.minFitness):
            for ind in self.population :
                ind.Evaluate()

            self.population.sort()
            bestInd = self.population[len(self.population) - 1]
            print("Best : {} at gen {}".format(bestInd, self.generationNb))

            self.bestFitness = bestInd.fitness
            newGen = [bestInd]
            for i in range(parameters.Parameters.individualsNb - 1):
                if(random.random() <= parameters.Parameters.crossoverRate):
                    father = self.Selection()
                    mother = self.Selection()
                    ind = IndividualFactory.getInstance().getIndividual(self.problem, father=father, mother=mother)
                else :
                    father = self.Selection()
                    ind = IndividualFactory.getInstance().getIndividual(self.problem, father=father)

                newGen.append(ind)

            self.Survival(newGen)
            self.generationNb += 1

        

    