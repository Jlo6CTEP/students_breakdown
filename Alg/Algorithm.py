import random

from Alg.Solution import Solution
from DB.db_manager import db
from math import ceil

NORMALIZE_TO = 10 / 100
POPULATION_SIZE = 20

BEST_SOLUTIONS = 8
BASE_CROSSOVER_RATE = 8

# first element is mode of distribution
# if set to true then all members must have almost same values
# if false - values should be different
# second parameter is number of such priorities, max function will be applied to them
# fourth parameter if absolute value or number of parameters matter
# true means value
# last parameter is should we take this into account

language_priority = [True, 3, 75 * NORMALIZE_TO, False, True]
skill_priority = [False, 3, 75 * NORMALIZE_TO, True, False]
psych_factor_priority = [False, 1, 10 * NORMALIZE_TO, False, True]
grades_priority = [False, 1, 40 * NORMALIZE_TO, True, False]
experience_priority = [False, 1, 50 * NORMALIZE_TO, False, True]
study_group_priority = [True, 1, 100 * NORMALIZE_TO, False, False]
project_priority = [True, 3, 90 * NORMALIZE_TO, False, True]
role_priority = [False, 3, 70 * NORMALIZE_TO, False, True]


def priority_vector(): 
    return [language_priority] + [skill_priority] + \
           [psych_factor_priority] + [grades_priority] + \
           [experience_priority] + [study_group_priority] + \
           [project_priority] + [role_priority]


class Algorithm:
    team_list = None

    CROSSOVER_RATE = {200: ceil(BASE_CROSSOVER_RATE/1),
                      206: ceil(BASE_CROSSOVER_RATE/2),
                      212: ceil(BASE_CROSSOVER_RATE/3),
                      219: ceil(BASE_CROSSOVER_RATE/4),
                      225: ceil(BASE_CROSSOVER_RATE/5),
                      231: ceil(BASE_CROSSOVER_RATE/6),
                      238: ceil(BASE_CROSSOVER_RATE/7),
                      244: ceil(BASE_CROSSOVER_RATE/8),
                      250: ceil(BASE_CROSSOVER_RATE/9),
                      100500: ceil(BASE_CROSSOVER_RATE/9)}

    def __crossover_intensity(self, fitness):
        return [x[1] for x in self.CROSSOVER_RATE.items() if fitness < x[0]][0]

    def __init__(self):
        self.team_list = []

    def do_the_magic(self):
        self.team_list = []
        student_list = db.get_students()

        population = []
        for x in range(POPULATION_SIZE):
            random.shuffle(student_list)
            solution = Solution()
            for f in range(0, len(student_list), MEMBER_COUNT):
                solution.add_team(sum(student_list[f:f+MEMBER_COUNT]))
            population.append(solution)
        fitness = 0
        generation = 0
        population.sort(reverse=True)
        while fitness < 250:
            fitness = population[0].fitness()
            print("Generation: {}, best result: {}".format(generation, fitness))
            crossover_rate = self.__crossover_intensity(fitness)
            heirs = []
            for x in population[:BEST_SOLUTIONS]:
                heirs.append(x.self_fuck(crossover_rate))
            population[len(population)-BEST_SOLUTIONS-1:] = heirs
            population.sort(reverse=True)
            generation += 1
        return population[0]
