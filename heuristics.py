import math


class Heuristic:
    def get_evaluation(self, state):
        pass


class ExampleHeuristic(Heuristic):
    def get_evaluation(self, state):
        return 0


class Hamming(Heuristic):
    def get_evaluation(self, state):
        state = list(state)

        finalState = []
        i = 0
        while(i < len(state)):
            finalState.append(i)
            i+=1

        return sum(x != y for x, y in zip(finalState, state))


class Manhattan(Heuristic):
    def get_evaluation(self, state):
        def manhattan_distance_sum(array1, array2):
            n = len(array1)

            total_distance = 0

            for i in range(n):
                for j in range(n):
                    element1 = array1[i][j]
                    element2 = array2[i][j]

                    distance = abs(i - element1 // n) + abs(j - element1 % n)
                    distance += abs(i - element2 // n) + abs(j - element2 % n)

                    total_distance += distance

            return total_distance

        def list_to_matrix(lst):
            n = int(math.sqrt(len(lst)))
            matrix = [lst[i:i + n] for i in range(0, len(lst), n)]
            return matrix

        def final_matrix(lst):
            n = int(math.sqrt(len(lst)))
            index_matrix = [list(range(i, i + n)) for i in range(0, len(lst), n)]
            return index_matrix

        state = list(state)

        matrixState = list_to_matrix(state)
        finalState = final_matrix(state)

        return manhattan_distance_sum(matrixState, finalState)