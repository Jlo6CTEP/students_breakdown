NORMALIZE_TO = 10/100


class Algorithm:
    team_list = None
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

    def __init__(self):
        self.team_list = []

    def do_the_magic(self):
        pass

    def priority_vector(self):
        return [self.language_priority] + [self.skill_priority] + \
               [self.psych_factor_priority] + [self.grades_priority] + \
               [self.experience_priority] + [self.study_group_priority] + \
               [self.project_priority] + [self.role_priority]
