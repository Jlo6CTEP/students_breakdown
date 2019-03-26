import random
from copy import deepcopy

from Alg.Team import MEMBER_COUNT
SIZE_PENALTY = 50


class Solution(list):

    student_ptr = {}
    team_ptr = {}
    __fitness_var = None

    def __init__(self):
        super().__init__()

    def fitness(self):
        if self.__fitness_var:
            return self.__fitness_var
        else:
            self.__fitness_var = \
                sum([t.happiness() + abs(MEMBER_COUNT - len(t)) * SIZE_PENALTY for t in self])/len(self)
            return self.__fitness_var

    def self_fuck(self, n):
        self.__fitness_var = None
        heir = deepcopy(self)
        random_genes = random.sample(heir.student_ptr.keys(), 2 * n)

        try:
            for x in random_genes:
                f = heir.team_ptr[x]
                l = heir.student_ptr[x]
        except:
            print("fuck")

        source_genes = random_genes[:n]
        target_genes = random_genes[n:]

        for x in zip(source_genes, target_genes):
            heir.team_ptr[x[0]] - heir.student_ptr[x[0]]
            heir.team_ptr[x[0]] + heir.student_ptr[x[1]]
            heir.team_ptr[x[1]] - heir.student_ptr[x[1]]
            heir.team_ptr[x[1]] + heir.student_ptr[x[0]]
        return heir

    def add_team(self, team):
        self.__fitness_var = None
        for x in team:
            self.student_ptr.update({x.student_id: x})
            self.team_ptr.update({x.student_id: team})
        self.append(team)

    def __lt__(self, other):
        return self.fitness() < other.fitness()
