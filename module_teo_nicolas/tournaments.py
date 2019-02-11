import strategies as strat
import soccersimulator as soc
from lib import tree

class Tournaments:
    def __init__(self, behaviorClasses, nbPlayersPerTeam, nbSteps):
        self.strategies = self.createStrategiesFromBehaviorClasses(behaviorClasses)
        self.nbStrategies = len(self.strategies)
        self.nbPlayers = nbPlayersPerTeam
        self.nbSteps = nbSteps
        self.teams = None
        self.tournament = None
        self.createTeams()
        self.createTournament()

    def createTeams(self):
        soccTree = tree.SoccerTree(self.strategies, self.nbPlayers)
        self.teams = soccTree.GetTeams()
        if len(self.teams) == 1 :
            self.teams.append(self.teams[0].copy())

    def createStrategiesFromBehaviorClasses(self, behaviorClasses):
        behaviors = []
        for behaviorClass in behaviorClasses:
            behavior = behaviorClass()
            behaviors.append(behavior)

        return strat.createStrategies(behaviors)
    
    def createTournament(self):
        self.tournament = soc.SoccerTournament(nb_players=self.nbPlayers, max_steps=self.nbSteps)
        for team in self.teams:
            self.tournament.add_team(team)

    def playTournament(self):
        print(self.teams)
        self.tournament.play()

    def Show(self):
        nb_teams = self.tournament.nb_teams

        for i in range (nb_teams):
            for j in range (nb_teams):
                if i == j :
                    continue
                soc.show_simu(self.tournament.get_match(i, j))

    def printScores(self):
        self.tournament.print_scores()

if __name__ == "__main__":
    behaviorClasses = [strat.FonceurBehavior, strat.GoalBehavior]
    tournament = Tournaments(behaviorClasses, 2, 500)
    tournament.playTournament()
    #tournament.Show()
    tournament.printScores()

