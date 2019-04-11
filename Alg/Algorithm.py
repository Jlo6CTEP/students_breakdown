import random
from DB.db_manager import db
from Alg.Team import MEMBER_COUNT

NORMALIZE_TO = 10/100
POPULATION_SIZE = 100

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
    # first element is mode of distribution
    # if set to true then all members must have almost same values
    # if false - values should be different
    # second parameter is number of such priorities, max function will be applied to them
    # fourth parameter if absolute value or number of parameters matter
    # true means value
    # last parameter is should we take this into account

    def __init__(self):
        self.team_list = []

    def do_the_magic(self):
        self.team_list = []
        student_list = db.get_students()

        population = []
        from Alg.Team import Team
        for x in range(POPULATION_SIZE):
            random.shuffle(student_list)
            solution = [Team() for x in range(len(student_list)//MEMBER_COUNT)]
            for f in range(len(student_list)):
                solution[f//MEMBER_COUNT] += student_list[f]
            population.append(solution)
            solution = []
        print()
