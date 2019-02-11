import strategies as strat
import tournaments as trn

if __name__ == "__main__":
    behaviorClasses = [strat.FonceurBehavior, strat.GoalBehavior]
    tournament = trn.Tournaments(behaviorClasses, 2, 500)
    tournament.playTournament()
    tournament.Show()
    tournament.printScores()