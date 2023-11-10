import copy
import random
import time
from collections import deque

import config


class Algorithm:
    def __init__(self, heuristic=None):
        self.heuristic = heuristic
        self.nodes_evaluated = 0
        self.nodes_generated = 0

    def get_legal_actions(self, state):
        self.nodes_evaluated += 1
        max_index = len(state)
        zero_tile_ind = state.index(0)
        legal_actions = []
        if 0 <= (up_ind := (zero_tile_ind - config.N)) < max_index:
            legal_actions.append(up_ind)
        if 0 <= (right_ind := (zero_tile_ind + 1)) < max_index and right_ind % config.N:
            legal_actions.append(right_ind)
        if 0 <= (down_ind := (zero_tile_ind + config.N)) < max_index:
            legal_actions.append(down_ind)
        if 0 <= (left_ind := (zero_tile_ind - 1)) < max_index and (left_ind + 1) % config.N:
            legal_actions.append(left_ind)
        return legal_actions

    def apply_action(self, state, action):
        self.nodes_generated += 1
        copy_state = list(state)
        zero_tile_ind = state.index(0)
        copy_state[action], copy_state[zero_tile_ind] = copy_state[zero_tile_ind], copy_state[action]
        return tuple(copy_state)

    def get_steps(self, initial_state, goal_state):
        pass

    def get_solution_steps(self, initial_state, goal_state):
        begin_time = time.time()
        solution_actions = self.get_steps(initial_state, goal_state)
        print(f'Execution time in seconds: {(time.time() - begin_time):.2f} | '
              f'Nodes generated: {self.nodes_generated} | '
              f'Nodes evaluated: {self.nodes_evaluated}')
        return solution_actions


class ExampleAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []
        while state != goal_state:
            legal_actions = self.get_legal_actions(state)
            action = legal_actions[random.randint(0, len(legal_actions) - 1)]
            solution_actions.append(action)
            state = self.apply_action(state, action)
        return solution_actions

# BFS obilazak
# class ExampleAlgorithm1(Algorithm):
#     def get_steps(self, initial_state, goal_state):
#         state = initial_state
#         solution_actions = []
#
#         queue = deque()
#         queue.append(state)
#
#         passedStates = []
#
#         while state != goal_state:
#             state = queue.popleft()
#             legal_actions = self.get_legal_actions(state)
#
#             firstState = copy.copy(state)
#             print(firstState)
#
#             for legal_action in legal_actions:
#                 action = legal_action
#
#                 state = firstState
#                 state  = self.apply_action(state, action)
#
#                 backAction = state.index(0)
#
#                 if(state not in passedStates):
#                     queue.append(state)
#                     passedStates.append(state)
#                     solution_actions.append(action)
#                     solution_actions.append(backAction)
#
#             state = copy.copy(firstState)
#
#         return solution_actions


class BFS(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []

        explored = []

        queue = deque()
        queue.append([state])

        def bfsShortestPath():
            while(queue):
                path = queue.popleft()
                node = path[-1]

                if(node not in explored):
                    state = copy.copy(node)
                    neighbourActions = self.get_legal_actions(state)

                    firstState = copy.copy(state)

                    for na in neighbourActions:
                        newPath = list(path)

                        state = self.apply_action(state, na)

                        if(state in newPath):
                            state = copy.copy(firstState)
                            continue

                        newPath.append(state)
                        queue.append(newPath)

                        if(state == goal_state):
                            shortestPath = newPath
                            return shortestPath


                        state = copy.copy(firstState)

                    explored.append(node)

        shortestPath = bfsShortestPath()

        tmpShortestPath = copy.copy(shortestPath)
        tmpShortestPath.pop(0)
        for t in tmpShortestPath:
            solution_actions.append(t.index(0))

        return solution_actions


class BestFirst(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []

        explored = []

        queue = []
        queue.append([[state], 0])

        def bestFirstShortestPath():
            while(queue):
                path = queue.pop(0)[0]
                node = path[-1]

                if(node not in explored):
                    state = copy.copy(node)
                    neighbourActions = self.get_legal_actions(state)

                    firstState = copy.copy(state)

                    for na in neighbourActions:
                        newPath = list(path)

                        state = self.apply_action(state, na)

                        if(state in newPath):
                            state = copy.copy(firstState)
                            continue

                        newPath.append(state)
                        h = self.heuristic.get_evaluation(state)
                        queue.append([newPath, h])

                        if(state == goal_state):
                            shortestPath = newPath
                            return shortestPath

                        state = copy.copy(firstState)

                    explored.append(node)

                #sort queue before poping
                queue.sort(key=lambda x: x[1])

        shortestPath = bestFirstShortestPath()

        tmpShortestPath = copy.copy(shortestPath)
        tmpShortestPath.pop(0)
        for t in tmpShortestPath:
            solution_actions.append(t.index(0))

        return solution_actions

class AStar(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []

        explored = []

        queue = []
        queue.append([[state], 0])

        def AStarShortestPath():
            while(queue):
                path = queue.pop(0)[0]
                node = path[-1]

                if(node not in explored):
                    state = copy.copy(node)
                    neighbourActions = self.get_legal_actions(state)

                    firstState = copy.copy(state)

                    for na in neighbourActions:
                        newPath = list(path)

                        state = self.apply_action(state, na)

                        if(state in newPath):
                            state = copy.copy(firstState)
                            continue

                        newPath.append(state)
                        h = self.heuristic.get_evaluation(state) + len(newPath)
                        queue.append([newPath, h])

                        if(state == goal_state):
                            shortestPath = newPath
                            return shortestPath

                        state = copy.copy(firstState)

                    explored.append(node)

                #sort queue before poping
                queue.sort(key=lambda x: x[1])

        shortestPath = AStarShortestPath()

        tmpShortestPath = copy.copy(shortestPath)
        tmpShortestPath.pop(0)
        for t in tmpShortestPath:
            solution_actions.append(t.index(0))

        return solution_actions