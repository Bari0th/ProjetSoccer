import gen
import random
import parameters

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

class TSPIndividual(gen.Individual):
    def __init__(self, father=None, mother=None):
        self.genome = []
        if father != None :
            if mother == None :
                for gene in father.genome :
                    self.genome.append(TSPGene(gene))
            else :
                cuttingPoint = random.randint(0, len(father.genome) - 1)
                for gene in father.genom[:cuttingPoint]:
                    self.genome.append(TSPGene(gene))
                for gene in mother.genome :
                    if gene not in self.genome :
                        self.genome.append(TSPGene(gene))
            
            self.Mutate()
        else :
            cities = TSP.getCities()

            while(len(cities) > 0):
                index = random.randint(0, len(cities) - 1)
                city = cities.pop(index)
                self.genome.append(TSPGene(city))

    def Mutate(self):
        if(random.random() <= parameters.Parameters.mutationsRate):
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

        totalKm = oldGene.getDistance(self.genome[0])
        fitness = totalKm
        return fitness