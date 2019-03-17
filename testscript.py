import math
import postgresql
import random
from numpy import random as rand

TWO_PI_SQRT = 2.506
SIGMA = 2
MU = 1.5


def gauss(x):
    return 1 / SIGMA / TWO_PI_SQRT * math.e ** (-(x - MU) ** 2 / (2 * SIGMA ** 2))


db = postgresql.open("pq://zpgkwdlt:M4Ef1T1p8VmvYamieL-JR3ZK4J0hztBy@dumbo.db.elephantsql.com:5432/zpgkwdlt")

projects = db.query("select * from project")
languages = db.query("select * from languages")
roles = db.query("select * from project_roles")
psych_factors = db.query("select * from psych_factor")
experiences = db.query("select * from experience")
study_groups = db.query("select * from study_group")

# experience + skill_offsets (to make PL skills correlating with experience)
skill_offset = [4, 5, 6, 8, 9, 10]
skill_range = range(0, 10)
exp_with_offset = [x for x in zip(skill_offset, experiences)]

# creates gaussian distribution of skills' probability
gauss_range = range(-4, 6)
skills_distr = [gauss(x) for x in gauss_range]

# normalizes it to form full group (hi prob_stat)
skills_distr = list(map(lambda x: x + ((1 - sum(skills_distr)) / len(gauss_range)), skills_distr))

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
    # exp_with_offset[0] is skill offset. This parameter will scale skills for all 3 languages,
    # because it is strange when student with experience level noob has maximum skill in some PL

    #   take one random (skill offset) pair
    exp = random.choice(exp_with_offset)

    # scale skills to chosen skill offset level
    skills_scaled = list(map(lambda x: x * exp[0] / 10, skill_range))

    # takes 3 random values
    skills = sorted([skills_scaled[x] for x in rand.choice(range(len(skills_scaled)), p=skills_distr, size=3)])

    # 3 unique languages
    rand_lang = random.sample(languages, k=3)
    rand_projects = random.sample(projects, k=3)
    rand_roles = random.sample(roles, k=random.randint(1, 3))

    # pad the remaining with null
    rand_roles = rand_roles + ([('NULL', 'NULL')] * 3)[:3 - len(rand_roles)]

    # insert into main database
    db.execute("""INSERT INTO records 
                    (student_id, language1, language1_skill, 
                    language2, language2_skill, 
                    language3, language3_skill, 
                    psych_factor, grades, experience, 
                    study_group, project1, project2, project3) 
                    VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"""
               .format(x, rand_lang[0][0], round(skills[0], 3),
                       rand_lang[1][0], round(skills[1], 3),
                       rand_lang[2][0], round(skills[2], 3),
                       random.choice(psych_factors)[0],
                       round(random.triangular(0, min(exp[0] + 2, 10)), 3),
                       exp[1][0], random.choice(study_groups)[0],
                       rand_projects[0][0], rand_projects[1][0], rand_projects[2][0]
                       ),
               )

    # insert into students roles table
    db.execute("INSERT INTO students_roles values ({}, {}, {}, {})"
               .format(x, rand_roles[0][0], rand_roles[1][0], rand_roles[2][0]))
db.close()
