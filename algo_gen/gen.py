import random


class Parameters :
    individualsNb = 20
    generationMaxNb = 50
    initialGenesNb = 10
    minFitness = 0

    mutationsRate = 0.1
    mutationAddRate = 0.2
    mutationDeleteRate = 0.1
    crossoverRate =  0.7

class Individual :
    def __init__(self):
        self.fitness = -1
        self.genome = []

    def Mutate(self):
        pass

    def Evaluate(self):
        pass

    def __repr__(self):
        s = "{} : {}".format(self.fitness, "-".join(list(map(lambda x : str(x), self.genome))))
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
        if type == "TSP":
            TSP.Init()

    def getIndividual(self, type, father=None, mother=None):
        ind = None
        if type == "TSP":
            ind = TSPIndividual(father, mother)
        return ind



class EvolutionnaryProcess:
    def __init__(self, problem):
        IndividualFactory.getInstance().Init(problem)
        self.population = []
        self.generationNb = 0
        self.bestFitness = 0
        self.problem = problem

        for i in range(Parameters.individualsNb):
            self.population.append(IndividualFactory.getInstance().getIndividual(problem))


    def Survival(self, newGen):
        self.population = newGen

    def Selection(self):
        totalRanks = Parameters.individualsNb * (Parameters.individualsNb + 1) // 2
        rand = random.randint(1, totalRanks)
        nbParts = Parameters.individualsNb
        totalParts = 0
        indIndex = 0

        while totalParts < rand :
            indIndex += 1
            totalParts += nbParts
            nbParts -= 1

        self.population.sort()
        return self.population[min(indIndex, len(self.population) - 1)]

    def Run(self):
        self.bestFitness = Parameters.minFitness + 1
        while (self.generationNb < Parameters.generationMaxNb and self.bestFitness > Parameters.minFitness):
            for ind in self.population :
                ind.Evaluate()

            self.population.sort()
            bestInd = self.population[0]
            print("Best : {} at gen {}".format(str(bestInd), self.generationNb))

            self.bestFitness = bestInd.fitness
            newGen = [bestInd]
            for i in range(Parameters.individualsNb - 1):
                if(random.random() <= Parameters.crossoverRate):
                    father = self.Selection()
                    mother = self.Selection()
                    ind = IndividualFactory.getInstance().getIndividual(self.problem, father=father, mother=mother)
                else :
                    father = self.Selection()
                    ind = IndividualFactory.getInstance().getIndividual(self.problem, father=father)

                newGen.append(ind)

            self.Survival(newGen)
            self.generationNb += 1

class City :
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

class TSP:
    cities = []
    distances = []

    @staticmethod
    def Init():
        TSP.cities = [City("Paris"), City("Lyon"), City("Marseille"), City("Nantes"), City("Bordeaux"), City("Toulouse"), City("Lille")]
        TSP.distances = []

        TSP.distances.append([0, 462, 772, 379, 546, 678, 215])
        TSP.distances.append([462, 0, 326, 598, 842, 506, 664])
        TSP.distances.append([772, 326, 0, 909, 555, 407, 1005])
        TSP.distances.append([379, 598, 909, 0, 338, 540, 584])
        TSP.distances.append([546, 842, 555, 338, 0, 250, 792])
        TSP.distances.append([678, 506, 407, 540, 250, 0, 926])
        TSP.distances.append([215, 664, 1005, 584, 792, 926, 0])


    @staticmethod
    def getDistance(city1, city2):
        return TSP.distances[TSP.cities.index(city1)][TSP.cities.index(city2)]

    @staticmethod
    def getCities():
        return TSP.cities.copy()


class TSPGene:
    def __init__(self, city=None, gene=None):
        if city :
            self.city = city
        else :
            self.city = gene.city

    def getDistance(self, gene):
        return TSP.getDistance(self.city, gene.city)

    def __repr__(self):
        return self.city.__repr__()

class TSPIndividual(Individual):
    def __init__(self, father=None, mother=None):
        Individual.__init__(self)
        self.genome = []
        if father is not None :
            if mother is None :
                for gene in father.genome :
                    self.genome.append(TSPGene(gene=gene))
            else :
                cuttingPoint = random.randint(0, len(father.genome) - 1)
                for gene in father.genom[:cuttingPoint]:
                    self.genome.append(TSPGene(gene=gene))
                for gene in mother.genome :
                    if gene not in self.genome :
                        self.genome.append(TSPGene(gene=gene))
            
            self.Mutate()
        else :
            cities = TSP.getCities()

            while(len(cities) > 0):
                index = random.randint(0, len(cities) - 1)
                city = cities.pop(index)
                self.genome.append(TSPGene(city))

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


if __name__ == "__main__":
    Parameters.crossoverRate = 0
    Parameters.mutationsRate = 0.3
    Parameters.mutationAddRate = 0
    Parameters.mutationDeleteRate = 0
    Parameters.minFitness = 2579
    gen = EvolutionnaryProcess("TSP")
    gen.Run()
