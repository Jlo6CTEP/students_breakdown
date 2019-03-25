import math
import string

import postgresql
import random
from DB.db_manager import db, SCHEMA
from numpy import random as rand
from Alg import Record

TWO_PI_SQRT = 2.506
SIGMA = 2
MU = 1.5

TXT = 1


def gauss(x):
    return 1 / SIGMA / TWO_PI_SQRT * math.e ** (-(x - MU) ** 2 / (2 * SIGMA ** 2))


db1 = postgresql.open("pq://zpgkwdlt:M4Ef1T1p8VmvYamieL-JR3ZK4J0hztBy@dumbo.db.elephantsql.com:5432/zpgkwdlt")

projects = db1.query("select * from project")
languages = db1.query("select * from languages")
roles = db1.query("select * from project_roles")
psych_factors = db1.query("select * from psych_factor")
experiences = db1.query("select * from experience")
study_groups = db1.query("select * from study_group")

# experience + skill_offsets (to make PL skills correlating with experience)
skill_offset = [4, 5, 6, 8, 9, 10]
skill_range = range(0, 10)
exp_with_offset = [x for x in zip(skill_offset, experiences)]

# creates gaussian distribution of skills' probability
gauss_range = range(-4, 6)
skills_distr = [gauss(x) for x in gauss_range]

# normalizes it to form full group (hi prob_stat)
skills_distr = list(map(lambda x: x + ((1 - sum(skills_distr)) / len(gauss_range)), skills_distr))

mails = open("../Data/email.txt").read().split(',')
names = open("../Data/first_name.txt").read().split(',')
surnames = open("../Data/last_name.txt").read().split(',')

for x in range(200):
    # exp_with_offset[0] is skill offset. This parameter will scale skills for all 3 languages,
    # because it is strange when student with experience level noob has maximum skill in some PL

    #   take one random (skill offset) pair
    exp = random.choice(exp_with_offset)

    # scale skills to chosen skill offset level
    skills_scaled = list(map(lambda x: x * exp[0] / 10, skill_range))

    # takes 3 random values
    skills = sorted([skills_scaled[x] for x in rand.choice(range(len(skills_scaled)), p=skills_distr, size=3)],
                    reverse=True)

    # 3 unique languages
    rand_lang = random.sample(languages, k=3)
    rand_projects = random.sample(projects, k=3)
    rand_roles = random.sample(roles, k=random.randint(1, 3))

    # pad the remaining with null
    rand_roles = rand_roles + ([('NULL', 'NULL')] * 3)[:3 - len(rand_roles)]

    rand_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
    rand_mail = random.choice(mails)
    rand_name = random.choice(names)
    rand_surname = random.choice(surnames)
    next_id = db.get_next_id()
    # insert into main database
    record = Record.Record(rand_name, rand_surname, rand_mail, rand_password, sid=next_id,
                           record={x[1]: x[0] for x in zip([rand_lang[0][TXT], rand_lang[1][TXT],
                                                            rand_lang[2][TXT], round(skills[0], 3),
                                                            round(skills[1], 3), round(skills[2], 3),
                                                            random.choice(psych_factors)[TXT],
                                                            round(random.triangular(0, min(exp[0] + 2, 10)), 3),
                                                            exp[1][TXT], random.choice(study_groups)[TXT],
                                                            rand_projects[0][TXT], rand_projects[1][TXT],
                                                            rand_projects[2][TXT], rand_roles[0][TXT],
                                                            rand_roles[1][TXT], rand_roles[2][TXT]],
                                                           SCHEMA)})
    db.insert_student(record)
