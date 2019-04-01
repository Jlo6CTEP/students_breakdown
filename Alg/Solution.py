import random
from copy import deepcopy, copy

from Alg.Team import Team


class Solution(list):
    student_ptr = {}
    team_ptr = {}
    __fitness_var = None

    def __init__(self, f=None):
        if f is not None:
            super().__init__(f)
        else:
            super().__init__()
        self.student_ptr = {}
        self.team_ptr = {}

    def __copy__(self):
        solution = Solution()
        for x in self:
            solution.add_team(Team(x))
        return solution

    def fitness(self):
        if self.__fitness_var:
            return self.__fitness_var
        else:
            self.__fitness_var = \
                sum([t.happiness() for t in self]) / len(self)
            return self.__fitness_var

    def add_team(self, team):
        self.__fitness_var = None
        for x in team:
            self.student_ptr.update({x.user_id: x})
            self.team_ptr.update({x.user_id: team})
        self.append(team)

    def __lt__(self, other):
        return self.fitness() < other.fitness()


