import random

import soccersimulator as soc

from . import strategies as strats
from .soccer import action as act
from .soccer import discretizedterrain as d_terrain
from .soccer import soccertools as tools
from .utils.json import decode_json, encode_json
from .utils.tree import SoccerTree


class QSoccer:
    algo = None
    def __init__(self, nb_player_per_team):
        self.d_terrain = d_terrain.DiscretizedTerrain.getInstance()
        self.nb_player_per_team = nb_player_per_team
        self.terrain = tools.TerrainData.getInstance()

        # create q table and counts
        self.q_table = {}
        self.counts = {}

        self.states = []
        self.actions = []
        self._initStateSpace()
        self._initQTableAndCounts()

        # Initiate Soccer
        self.simu = None
        

    def _initStateSpace(self):
        all_coords = self.d_terrain.AllPossibleCoords()
        tree = SoccerTree(all_coords, self.nb_player_per_team)
        self.states = list(map(lambda x : tuple(x), tree.paths))

    def _initQTableAndCounts(self):
        self.possibleActions = act.getAllActions()
        moves = self.possibleActions["moves"]["names"]
        shoots = self.possibleActions["shoots"]["names"]

        moves_len = len(moves)
        shoots_len = len(shoots)
        for state in self.states :
            self.q_table[str(state)] = {}
            self.counts[str(state)] = {}
            for i in range(moves_len):
                for j in range(shoots_len):
                    key = (i , j)
                    self.actions.append(key)
                    self.q_table[str(state)][str(key)] = 0
                    self.counts[str(state)][str(key)] = 0
                    

    def Train(self, show=False):
        self.epochs = 5
        self.epsilon = 0.1
        self.current_epoch = 0

        self.step_per_epoch = 4
        self.max_steps = self.epochs * self.step_per_epoch

        team1 = soc.SoccerTeam("Jambon") 
        team2 = soc.SoccerTeam("Beurre")

        for i in range(self.nb_player_per_team):
            strat = strats.createStrategy(strats.TraineeBehavior())
            team1.add(strat.name + " " + str(i), strat)

            if(self.nb_player_per_team == 1):
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

    def _testSave(self):
        encode_json(self.q_table, "q_table")

    def _testLoad(self):
        data = decode_json("q_table")
        return data

    def _getS0(self):
        return random.choice(self.states)

    def _getA0(self):
        return random.choice(self.actions)

    def _get_ith_player_behavior(self, team, i):
        return team.players[i].strategy.behavior

    def _get_current_action_for_ith_player(self, i):
        self.currentAction = self._getA0()
        move_index, shoot_index = self.currentAction
        actMove = self.possibleActions["moves"][self.possibleActions["moves"]["names"][move_index]]()
        actShoot = self.possibleActions["shoots"][self.possibleActions["shoots"]["names"][shoot_index]]()
        return actMove, actShoot

    def _getNextAction(self, act_probs):
        if (random.random() < self.epsilon):
            return self._getA0()
        best = None
        bestVal = 0
        for action in act_probs :
            if bestVal < act_probs[action] or best is None :
                best = action
                bestVal = act_probs[action]

        return best

    def _getNextState(self, soccerstate):
        newState = []
        for i in range (2 * self.nb_player_per_team + 1):
            coord = self.currentState[i]
            pos = self.d_terrain.FromCaseToPosition(coord)
            if i < self.nb_player_per_team : #team1
                pos = self.simu.state.states[(1, i)].position
            elif i == len(self.currentState) - 1 : #ball
                pos = self.simu.state.ball.position
            else : #team2
                pos = self.simu.state.states[(2, i - self.nb_player_per_team)].position

            coord = self.d_terrain.FromPositionToCase(pos)
            newState.append(coord)
        return tuple(newState)

    def _evaluate(self, soccerstate):
        if self.currentState not in self.returns :
            self.returns[self.currentState] = {}

        if self.currentAction not in self.returns[self.currentState] :
            self.returns[self.currentState][self.currentAction] = 0

        distance_to_goal = soccerstate.ball.position.distance(self.terrain.getTheOtherGoal(1).vector)
        self.returns[self.currentState][self.currentAction] -= distance_to_goal / 100

        if soccerstate.goal > 0 :
            coeff = 3 * self.step_per_epoch / ((soccerstate.step % self.step_per_epoch) + 1)
            print("coeff ", coeff)
            if soccerstate.goal == 1 :
                print("team 1 marque")
                self.returns[self.currentState][self.currentAction]  += abs(self.returns[self.currentState][self.currentAction]) * coeff
            elif soccerstate.goal == 2 :
                print("team 2 marque")
                self.returns[self.currentState][self.currentAction]  -= abs(self.returns[self.currentState][self.currentAction]) * coeff


        self.counts[str(self.currentState)][str(self.currentAction)] += 1


    def _updatePlayerBehavior(self, team):
        m, s = self._get_current_action_for_ith_player(0)
        self._get_ith_player_behavior(team, 0).changeMoveAction(m)
        self._get_ith_player_behavior(team, 0).changeShootAction(s)

    def _updateQTable(self):
        for state in self.returns :
            for action in self.returns[state] :
                old = self.q_table[str(state)][str(action)]
                count = self.counts[str(state)][str(action)]
                self.q_table[str(state)][str(action)] = old + (1.0 / count) * (self.returns[state][action] - old)
                print("({}, {}) : OLD = {} / NEW = {}".format(state, action, old, self.q_table[str(state)][str(action)]))

    def begin_match(self, team1, team2, state):
        pass

    def begin_round(self, team1, team2, state):
        print("-------------------BEGIN ROUND--------------------")
        self.currentState = self._getS0()
        for i in range (len(self.currentState)):
            coord = self.currentState[i]
            pos = self.d_terrain.FromCaseToPosition(coord)
            if i < self.nb_player_per_team : #team1
                self.simu.state.states[(1, i)].position = pos
            elif i == len(self.currentState) - 1 : #ball
                self.simu.state.ball.position = pos
            else : #team2
                self.simu.state.states[(2, i - self.nb_player_per_team)].position = pos

        self._updatePlayerBehavior(team1)

        self.returns = {}

    def update_round(self, team1, team2, state):
        self._evaluate(state)

        act_probs = self.q_table[str(self.currentState)]
        self.currentAction = self._getNextAction(act_probs)

        self.currentState = self._getNextState(state)

        self._updatePlayerBehavior(team1)

        if state.step % self.step_per_epoch == 0 :
            self.simu.end_round()

    def end_round(self, team1, team2, state):
        self._evaluate(state)
        self._updateQTable()

        print("Le round est fini, on passe à l'epoch suivante et on recommence au premier gene")
        self.current_epoch += 1
        self.current_epoch %= self.epochs
        
        if self.current_epoch == 0 :
            print("On a fait le tours des epochs, on arrete le match")
            self.simu.end_match()
            return

        print("Current epoch : {}".format(self.current_epoch))

    def end_match(self, team1, team2, state):
        self._testSave()
