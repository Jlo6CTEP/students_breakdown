import hashlib
import postgresql
from itertools import chain
from postgresql.exceptions import WrongObjectTypeError

DB_url = "pq://zpgkwdlt:M4Ef1T1p8VmvYamieL-JR3ZK4J0hztBy@dumbo.db.elephantsql.com:5432/zpgkwdlt"

clearable_tables = {"poll", "project", "team", "team_list",
                    "user", "group_list", "credentials",
                    "breakdown_course", "project_list", "course_list"}

tables_with_pk = dict.fromkeys(["course", "credentials", "group_by",
                                "poll", "privilege", "topic", "project",
                                "study_group", "team", "user"])


class DbManager:
    db = None
    max_project_id = None
    id_to_privilege = {}

    def __init__(self):
        self.db = postgresql.open(DB_url)
        query = self.db.query('select * from privilege')
        self.id_to_privilege = {x[0]: x[1] for x in query}
        self.max_project_id = self.db.query("select max(project_id) from project")[0][0]

    def __getattr__(self, table_name):
        r = self.db.prepare('select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = $1')(table_name)
        if table_name in tables_with_pk:
            r = r[1:]
        if len(r) == 0:
            raise AttributeError("Incorrect attribute name")
        setattr(self, table_name, dict.fromkeys(chain(*r)))
        return dict.fromkeys(chain(*r))

    def get_priority(self, user_id):
        student = self.db.prepare('select priv_id from "user" where user_id = $1')(user_id)[0]
        return self.id_to_privilege[student[0]]

    def get_user_topics(self, user_id):
        query = self.db.prepare('select * from user_topic_list where user_id = $1')(user_id)
        topics = []
        for row in query:
            topic = self.db.prepare('select topic_name from topic where topic_id= $1')(row[1])
            project_dict = {x[0]: x[1] for x in zip(self.topic, topic[0])}
            topics.append(project_dict)
        return topics

    def get_ta_projects(self, user_id):
        if self.get_priority(user_id) == "ta":
            self.db.prepare("select * from project where project_id in "
                            "(select project_id from ta_project_list where user_id = $1)")
        else:
            raise AssertionError("User is not a TA")

    def create_new_project(self, user_id, poll_info):
        if self.get_priority(user_id) == "ta":
            query_line = "insert into project ({}) values ({})". \
                format(', '.join(poll_info.keys()),
                       ', '.join(["$" + str(x) for x in range(len(poll_info))]))
            self.db.prepare(query_line)(*poll_info.values())
        else:
            raise AssertionError("User is not a TA")

    def __is_open(self, topic_dict):
        query_line = "select * from project where project_id in " \
                     "(select project_id from project_topic_list where topic_id in ({})) and is_open = false". \
            format(', '.join(["$" + str(x) for x in range(1, len(topic_dict) + 1)]))
        return len(self.db.prepare(query_line)(*topic_dict.values())) == 0

    def fill_poll(self, user_id, topic_dict):
        if not self.__is_open({x[0]: x[1] for x in topic_dict.items() if x[0].startswith("topic")}):
            raise AssertionError("One of projects is closed")
        with self.db.xact() as x:
            query_line = "insert into user_topic_list ({}) values ($1,$2),($3,$4),($5,$6)". \
                format(', '.join(self.user_topic_list.keys()))
            x.start()
            self.db.prepare(query_line)(*list(chain(*[[user_id, x[1]] for x in topic_dict.items()
                                                      if x[0].startswith("topic")])))

            self.db.prepare("insert into poll ({}) values ($1,$2,$3,$4,$5,$6)".
                            format("user_id, " + ', '.join(topic_dict.keys())))(user_id, *topic_dict.values())
            if len(self.db.prepare("select * from course_list where (user_id, course_id) = ($1, $2)")
                    (user_id, topic_dict['course_id'])) == 0:
                self.db.prepare("insert into course_list (user_id, course_id) values ($1, $2)") \
                    (user_id, topic_dict['course_id'])
            x.commit()

    def modify_poll(self, user_id, poll_id, topic_dict):
        if not self.__is_open(topic_dict):
            raise AssertionError("One of projects is closed")
        poll = self.db.prepare("select ({}) from poll where poll_id = $1 and user_id = $2".
                               format(', '.join(topic_dict.keys())))(poll_id, user_id)[0]
        old = {x[1]: x[0] for x in zip(poll, topic_dict.keys())}
        if len(old) == 0:
            raise AssertionError("This poll doesn't belong to user")
        query = "update poll set ({}) = ({}) where poll_id = $1 and user_id = $2". \
            format(', '.join(topic_dict.keys()), ', '.join(["$" + str(x) for x in range(3, len(topic_dict) + 3)]))
        with self.db.xact() as t:
            t.start()
            self.db.prepare(query)(poll_id, user_id, *topic_dict.values())
            for x in old.keys():
                self.db.prepare("update project_topic_list set project_id=$1 where topic_id=$2 and project_id = $3") \
                    (topic_dict[x], user_id, old[x])
            t.commit()

    def get_user_info(self, user_id):
        user_row = self.db.prepare('select * from "user" where user_id = $1')(user_id)[0][1:]
        user_dict = {x[0]: x[1] for x in zip(self.user, user_row)}

        group_row = self.db.prepare('select * from study_group where group_id in '
                                    '(select group_id from user_group_list where user_id = $1)')(user_id)
        group_dict = [{x[0]: x[1] for x in zip(self.study_group, row[1:])} for row in group_row]

        course_row = self.db.prepare('select * from breakdown_course where course_id in '
                                     '(select course_id from course_list where user_id = $1)')(user_id)
        course_dict = [{x[0]: x[1] for x in zip(self.course, row[1:])} for row in course_row]

        priv_row = self.db.prepare('select * from privilege where priv_id in '
                                   '(select priv_id from "user" where user_id = $1)')(user_id)[0][1:]
        priv_dict = {x[0]: x[1] for x in zip(self.privilege, priv_row)}

        user_dict.update({"study_group": group_dict})
        user_dict.update({"course": course_dict})
        user_dict.update(priv_dict)
        return user_dict

    def get_student_poll(self, user_id, course_id):
        if self.get_priority(user_id) == "student":
            try:
                from Alg.Record import Record
                d = Record({x[0]: x[1] for x in zip(self.poll, self.db.prepare(
                    "select * from poll as k where user_id = $1 and course_id = $2")(user_id, course_id)[0][1:])})
                for x in d.items():
                    if x[0].startswith("topic"):
                        d[x[0]] = self.db.prepare('select topic_name from topic  where topic_id = $1') \
                            (x[1])[0][0]
                d['course_id'] = self.db.prepare('select name from breakdown_course where course_id = $1') \
                    (d['course_id'])[0][0]
            except IndexError:
                return None
        else:
            raise AssertionError("User is not a student")
        return d

    def get_project_polls(self, project_id):
        records = []
        from Alg.Record import Record
        for record in self.db.prepare("select * from poll where project_id = $1")(project_id):
            records.append(Record({x[0]: x[1] for x in zip(self.poll, record[1:])}))
        return records

    # auchtung injection is possible (but who gives a fuck?)
    # yeah evil abuser can plunge his dirty dick right about here
    def fill_student(self, record):
        self.db.prepare(
            """update records set
                          ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) 
                                = ((select language_id from languages where language = $2),
                                (select language_id from languages where language = $3),
                                (select language_id from languages where language = $4), $5, $6, $7,
                                (select factor_id from psych_factor where factor = $8), $9,
                                (select experience_id from experience where experience = $10),
                                (select group_id from study_group where "group" = $11),
                                (select project_id from project where project = $12),
                                (select project_id from project where project = $13),
                                (select project_id from project where project = $14),
                                (select role_id from project_roles where role = $15),
                                (select role_id from project_roles where role = $16),
                                (select role_id from project_roles where role = $17))
                                where student_id = $1""".format(*record.keys()))(record.student_id, *record.values())

    def register_student(self, record):
        hasher = hashlib.md5()
        hasher.update(record.password.encode("ASCII"))
        self.db.prepare("""insert into records 
                          ({}, {}, {}, {}, {}) 
                                values ($1, $2, $3, $4, $5)""".format(*S_ID, *CREDENTIALS, *NAMES)) \
            (record.student_id, record.email, hasher.hexdigest(), record.name, record.surname)

    def insert_student(self, record):
        self.register_student(record)
        self.fill_student(record)

    def delete_student(self, student_id):
        self.db.prepare("delete from records where student_id = $1")(student_id)

    def get_students(self):
        records = list(self.db.query("select * from records"))
        email, password, name, surname = [SCHEMA.index(x) + 1 for x in CREDENTIALS + NAMES]
        from Alg import Record
        return list([Record.Record(row[name], row[surname], row[email], row[password],
                                   {x[1]: x[0] for x in zip(row[1:], SCHEMA)}, sid=row[0]) for row in records])

    def get_student(self, student_id=None, email=None, password=None):
        if email is not None and password is not None:
            hasher = hashlib.md5()
            hasher.update(password.encode("ASCII"))
            row = self.db.prepare("select * from records where (email, password) = ($1,$2)") \
                (email, hasher.hexdigest())
        elif student_id is not None:
            row = self.db.prepare("select * from records where student_id = $1")(student_id)
        else:
            raise ValueError("incorrect arguments")
        if len(row) == 0:
            return None
        else:
            row = list(row[0])
        row = self.id_to_val(row)
        email, password, name, surname = [SCHEMA.index(x) + 1 for x in CREDENTIALS + NAMES]
        from Alg import Record
        return Record.Record(row[name], row[surname], row[email], row[password],
                             {x[1]: x[0] for x in zip(row[1:], SCHEMA)}, sid=row[0])

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

    def get_next_id(self):
        return self.db.query("select nextval(pg_get_serial_sequence('records', 'student_id')) as new_id")[0][0]


#db = DbManager()

    def check_credentials(self, username, password):
        h = hashlib.md5()
        h.update(password.encode("ASCII"))
        password = h.hexdigest()
        return len(self.db.prepare("select * from credentials where username = $1 and password = $2")
                   (username, password)) != 0

    def register_user(self, registration_info):
        if len(self.db.prepare('select * from credentials where username = $1')(registration_info['username'])) != 0:
            raise AttributeError("Username already exists")
        if len(self.db.prepare('select * from "user" where mail = $1')(registration_info['mail'])) != 0:
            raise AttributeError("Email is already in use")

        registration_info['priv_id'] = self.db.prepare('select priv_id from privilege where priv_name = $1')(
            registration_info['priv_name'])[0][0]
        main_table_info = {k: registration_info[k] for k in set(self.user)}
        credential_table = {k: registration_info[k] for k in set(self.credentials)}
        group_table = registration_info["study_group"]
        with self.db.xact() as t:
            t.start()
            user_id = self.db.prepare('insert into "user" ({}) values ($1, $2, $3, $4) returning user_id'.
                                      format(', '.join(main_table_info.keys())))(*main_table_info.values())[0][0]

            credential_table.update({'user_id': user_id})

            h = hashlib.md5()
            h.update(credential_table['password'].encode("ASCII"))
            credential_table['password'] = h.hexdigest()

            user_group_list = []
            for x in group_table:
                record = self.user_group_list
                record['group_id'] = self.db.prepare('select group_id from study_group where "group"=$1') \
                    (x)[0][0]
                record['user_id'] = user_id
                user_group_list.append(record)

            self.db.prepare('insert into credentials ({}) values  ($1, $2, $3)'.
                            format(', '.join(credential_table.keys())))(*credential_table.values())
            for x in user_group_list:
                self.db.prepare('insert into user_group_list ({}) values ($1, $2)'.
                                format(', '.join(x.keys())))(*x.values())
            t.commit()
        return user_id

    def get_project_teams(self, project_id):
        teams = self.db.prepare('select * from team where topic_id in '
                                '(select topic_id from project_topic_list where project_id = $1)')(project_id)
        teams_dict = []
        for row in teams:
            teams_dict.append({x[0]: x[1] for x in zip(self.team, row[1:])})
        return teams_dict

    def get_team_members(self, team_id):
        return {x[0]: x[1] for x in zip(self.team,
                                        self.db.prepare('select * from team where team_id=$1')(team_id)[0][1:])}

    def create_team(self, course_id, topic_id, users):

        insert = 'insert into team (topic_id, course_id) values ($1, $2) returning team_id'
        with self.db.xact() as t:
            t.start()
            team_id = self.db.prepare(insert)(topic_id, course_id)[0][0]

            for x in users:
                record = self.student_team_list
                record['user_id'] = x
                record['team_id'] = team_id
                self.db.prepare('insert into student_team_list ({}) values ($1, $2)'. \
                                format(', '.join(record.keys())))(*record.values())
            t.commit()
        return team_id

    def get_projects(self):
        projects = self.db.query('select * from project')
        projects_dict = []
        for row in projects:
            projects_dict.append({x[0]: x[1] for x in zip(self.project, row[1:])})
        return projects_dict

    def get_project_info(self, project_id):
        project = self.db.prepare("select * from project where project_id = $1")(project_id)[0]
        return {x[0]: x[1] for x in zip(self.project, project[1:])}

    def add_project(self, project_info):
        line = 'insert into project ({}) values ({}) returning project_id'. \
            format(', '.join(project_info.keys()), ', '.join(['$' + str(x) for x in range(1, len(project_info) + 1)]))
        return self.db.prepare(line)(*project_info.values())[0][0]

    def clear_db(self):
        q = list(zip(*self.db.query("select table_name from information_schema.tables "
                                    "where table_schema = 'public' order by table_name")))[0]
        for x in q:
            try:
                if x in clearable_tables:
                    self.db.execute('truncate "{}"'.format(x))
                    print("Table {} was truncated".format(x))
            except WrongObjectTypeError:
                pass


db = DbManager()
