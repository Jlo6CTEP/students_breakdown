NORMALIZE_TO = 5 / 100

from Alg.Team import Team
from DB.db_manager import DbManager, MAX_GRADE

db = DbManager()


class Algorithm:
    # first element is mode of distribution
    # if set to true then all members must have almost same values
    # if false - values should be different
    # second parameter is number of such priorities, max function will be applied to them
    # last parameter if absolute value or number of parameters matter
    # true means value

    language_priority = [True, 3, 75 * NORMALIZE_TO, False]
    skill_priority = [False, 3, 75 * NORMALIZE_TO, True]
    psych_factor_priority = [False, 1, 10 * NORMALIZE_TO, False]
    grades_priority = [False, 1, 40 * NORMALIZE_TO, True]
    experience_priority = [False, 1, 50 * NORMALIZE_TO, False]
    study_group_priority = [True, 1, 100 * NORMALIZE_TO, False]
    role_priority = [False, 3, 70 * NORMALIZE_TO, False]
    project_priority = [True, 3, 90 * NORMALIZE_TO, False]

    def __init__(self):
        pass

    def do_the_magic(self):
        pass

    def priority_vector(self):
        return [self.language_priority] + [self.skill_priority] + \
               [self.psych_factor_priority] + [self.grades_priority] + \
               [self.experience_priority] + [self.study_group_priority] + \
               [self.role_priority] + [self.project_priority]

