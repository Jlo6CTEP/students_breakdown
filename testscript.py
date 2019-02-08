import postgresql
import random

projects = ['breakdown', 'classes_feedback',
            'delivery', 'attendance', 'cross_service',
            'rent', 'peer_assessment', 'startup',
            'timetable', 'applicants', 'time_tracking']
languages = ['Python', 'Java', 'JS', 'PHP', 'C++', 'C#', 'Eiffel']
roles = ['front', 'back', 'manager', 'screwaround']
psych_factors = ['intro', 'extro']
experiences = ['noob', 'know_syntax', 'know_something',
               'frameworker', 'coding_jedi', 'godalike']
db = postgresql.open("pq://postgres:gtxfnrf@localhost:5432/spdb")
study_groups = ["BS17-{}".format(x) for x in range(1, 9)]


study_group_priority = ['equal', 100]
project_priority = ['equal', 90]
language_priority = ['equal', 75]
role_priority = ['uniform', 70]
experience_priority = ['uniform', 50]
grades_priority = ['uniform', 40]
psych_factor_priority = ['uniform', 10]


for x in range(200):
    # noinspection SqlResolve
    db.execute("""INSERT INTO spdb_test (student_id,
             language1, language1_skill,
             language2, language2_skill,
             language3, language3_skill,
             project_role, psych_factor,
             grades, experience, project,
             study_group)
             VALUES
             ({}, '{}', {}, '{}', {}, '{}', {}, '{}', '{}', {}, '{}', '{}', '{}')"""
               .format(x, random.choice(languages), round(random.uniform(7, 10), 3),
                       random.choice(languages), round(random.uniform(4, 7), 3),
                       random.choice(languages), round(random.uniform(0, 4), 3),
                       "/".join(random.sample(roles, random.randint(1, len(roles) - 1))),
                       random.choice(psych_factors),
                       round(random.triangular(0, 10), 3),
                       random.choice(experiences),
                       random.choice(projects),
                       random.choice(study_groups))
               )

db.close()
