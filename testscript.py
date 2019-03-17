import math
import postgresql
import random

MAX_SCALE = 10
TWO_PI_SQRT = 2.506
SIGMA = 2
MU = 1.5


def gauss(x):
    return 1 / SIGMA / TWO_PI_SQRT * math.e ** (-(x - MU) ** 2 / (2 * SIGMA ** 2))


projects = ['breakdown', 'classes_feedback',
            'delivery', 'attendance', 'cross_service',
            'rent', 'peer_assessment', 'startup',
            'timetable', 'applicants', 'time_tracking']
languages = ['Python', 'Java', 'JS', 'PHP', 'C++', 'C#', 'Eiffel']
roles = ['front', 'back', 'manager', 'screwaround']
psych_factors = ['intro', 'extro']
experiences = ['noob', 'know_syntax', 'know_something',
               'frameworker', 'coding_jedi', 'godalike']
exp_offset = [4, 5, 6, 8, 9, 10]
grades_range = range(0, 10)

exp_with_offset = [x for x in zip(exp_offset, experiences)]
gauss_range = range(-4, 6)

grades_distr = [gauss(x) for x in gauss_range]
grades_distr2 = list(map(lambda x: x + ((1 - sum(grades_distr)) / len(gauss_range)), grades_distr))

db = postgresql.open("pq://zpgkwdlt:M4Ef1T1p8VmvYamieL-JR3ZK4J0hztBy@dumbo.db.elephantsql.com:5432/zpgkwdlt")
study_groups = ["BS17-{}".format(x) for x in range(1, 9)]

# equal = same for every team member
# uniform = different for team
study_group_priority = ['equal', 100]
project_priority = ['equal', 90]
language_priority = ['equal', 75]
role_priority = ['uniform', 70]
experience_priority = ['uniform', 50]
grades_priority = ['uniform', 40]
psych_factor_priority = ['uniform', 10]

for x in range(200):
    exp = random.choice(exp_with_offset)
    skills = sorted(random.choices(list(map(lambda x: x * exp[0] / 10, grades_range)),
                                   weights=grades_distr2, k=3), reverse=True)
    rand_lang = random.choices(languages, k=3)
    rand_projects = random.choices(projects, k=3)

    db.execute("""INSERT INTO spdb_test (student_id,
            language1, language1_skill,
            language2, language2_skill,
            language3, language3_skill,
            project_role, psych_factor,
            grades, experience, study_group,
            project1, project2, project3)
            VALUES
            ({}, '{}', {}, '{}', {}, '{}', {}, '{}', '{}', {}, '{}', '{}', '{}', '{}', '{}')"""
               .format(x, rand_lang[0], round(skills[0], 3),
                       rand_lang[1], round(skills[1], 3),
                       rand_lang[2], round(skills[2], 3),
                       "/".join(random.sample(roles, random.randint(1, len(roles) - 1))),
                       random.choice(psych_factors),
                       round(random.triangular(0, min(exp[0] + 2, 10)), 3),
                       exp[1],
                       random.choice(study_groups),
                       rand_projects[0], rand_projects[1], rand_projects[2]
                       ),
               )
db.close()
