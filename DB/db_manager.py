import postgresql
from Alg import Record

DB_url = "pq://zpgkwdlt:M4Ef1T1p8VmvYamieL-JR3ZK4J0hztBy@dumbo.db.elephantsql.com:5432/zpgkwdlt"

# this names matches column names so be careful
LANGUAGES = ['language1', 'language2', 'language3']  #
SKILLS = ['language1_skill', 'language2_skill', 'language3_skill']
PSYCH_FACTOR = ['psych_factor']  #
EXPERIENCE = ['experience']  #
STUDY_GROUP = ['study_group']  #
GRADES = ['grades']
PROJECTS = ['project1', 'project2', 'project3']  #
ROLES = ['role1', 'role2', 'role3']  #
CREDENTIALS = ['email', 'password']
NAMES = ['name', 'surname']
OTHER = []
MAX_GRADE = 10

SHORT_SCHEMA = LANGUAGES + SKILLS + PSYCH_FACTOR + GRADES + EXPERIENCE + STUDY_GROUP + PROJECTS + ROLES
MEDIUM_SCHEMA = SHORT_SCHEMA + CREDENTIALS
SCHEMA = MEDIUM_SCHEMA + NAMES


class DbManager:
    db = None

    def __init__(self):
        self.db = postgresql.open(DB_url)

    # auchtung injection is possible (but who gives a fuck?)
    # yeah evil abuser can plunge his dirty dick right about here
    def insert_student(self, record):
        self.db.prepare(
            """insert into records ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) 
                                        values ( 
                                        (select language_id from languages where language = $1),
                                        (select language_id from languages where language = $2),
                                        (select language_id from languages where language = $3), $4, $5, $6,
                                        (select factor_id from psych_factor where factor = $7), $8,
                                        (select experience_id from experience where experience = $9),
                                        (select group_id from study_group where "group" = $10),
                                        (select project_id from project where project = $11),
                                        (select project_id from project where project = $12),
                                        (select project_id from project where project = $13),
                                        (select role_id from project_roles where role = $14),
                                        (select role_id from project_roles where role = $15),
                                        (select role_id from project_roles where role = $16), $17, $18, $19, $20)"""
                .format(*record.keys(), *NAMES))(*record.values(), record.name, record.surname)

    def delete_student(self, student_id):
        self.db.prepare("delete from records where student_id = $1")(student_id)

    def get_student(self, student_id):
        row = self.db.prepare("select * from records where student_id = $1")(student_id)[0]
        name, surname = [SCHEMA.index(x) for x in NAMES]
        return Record.Record(row[0], name, surname, {x[1]: x[0] for x in zip(row[1:len(row) - 2], MEDIUM_SCHEMA)})

    def get_students(self):
        records = list(self.db.query("select * from records"))
        name, surname = [SCHEMA.index(x) for x in NAMES]
        return list([Record.Record(row[0], row[name], row[surname], {x[1]: x[0] for x in zip(row[1:], SCHEMA)},
                                   ) for row in records])

    def get_student_record(self, student_id=None, email=None, password=None):
        if email is not None and password is not None:
            row = list(self.db.prepare("select * from records where (email, password) = ($1,$2)")(email, password)[0])
        elif student_id is not None:
            row = list(self.db.prepare("select * from records where student_id = $1")(student_id)[0])
        else:
            raise ValueError("incorrect arguments")
        row = self.id_to_val(row)
        name, surname = [SCHEMA.index(x) for x in NAMES]
        return Record.Record(row[0], name, surname, {x[1]: x[0] for x in zip(row[1:], SCHEMA)})

    def id_to_val(self, row):
        row[1] = self.db.query("select language from languages where language_id = {}".format(row[1]))[0][0]
        row[2] = self.db.query("select language from languages where language_id = {}".format(row[2]))[0][0]
        row[3] = self.db.query("select language from languages where language_id = {}".format(row[3]))[0][0]
        row[7] = self.db.query("select factor from psych_factor where factor_id = {}".format(row[7]))[0][0]
        row[9] = self.db.query("select experience from experience where experience_id = {}".format(row[9]))[0][0]
        row[10] = self.db.query("select 'group' from study_group where group_id = {}".format(row[10]))[0][0]
        row[11] = self.db.query("select project from project where project_id = {}".format(row[11]))[0][0]
        row[12] = self.db.query("select project from project where project_id = {}".format(row[12]))[0][0]
        row[13] = self.db.query("select project from project where project_id = {}".format(row[13]))[0][0]
        row[14] = None if row[14] is None else \
            self.db.query("select role from project_roles where role_id = {}".format(row[14]))[0][0]
        row[15] = None if row[15] is None else \
            self.db.query("select role from project_roles where role_id = {}".format(row[15]))[0][0]
        row[16] = None if row[16] is None else \
            self.db.query("select role from project_roles where role_id = {}".format(row[16]))[0][0]
        return row

    def get_max_ids(self):
        lg = self.db.query("select max(language_id) from languages")[0][0]
        pf = self.db.query("select max(factor_id) from psych_factor")[0][0]
        ex = self.db.query("select max(experience_id) from experience")[0][0]
        pj = self.db.query("select max(project_id) from project")[0][0]
        sg = self.db.query("select max(group_id) from study_group")[0][0]
        pr = self.db.query("select max(role_id) from project_roles")[0][0]

        max_indexes = [[lg for x in range(len(LANGUAGES))] + [MAX_GRADE for x in range(len(LANGUAGES))] +
                       [pf for x in range(len(PSYCH_FACTOR))] + [MAX_GRADE for x in range(len(GRADES))] +
                       [ex for x in range(len(EXPERIENCE))] + [pj for x in range(len(PROJECTS))] +
                       [sg for x in range(len(STUDY_GROUP))] + [pr for x in range(len(ROLES))]][0]

        return max_indexes
