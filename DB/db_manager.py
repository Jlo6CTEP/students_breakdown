import hashlib
import postgresql
from itertools import chain
from postgresql.exceptions import WrongObjectTypeError

DB_url = "pq://zpgkwdlt:M4Ef1T1p8VmvYamieL-JR3ZK4J0hztBy@dumbo.db.elephantsql.com:5432/zpgkwdlt"

undropable_tables = ["course", "project", "study_group", "privilege"]

tables_with_pk = dict.fromkeys(["course", "credentials", "group_by",
                                "poll", "privilege", "project",
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

    def __get_user_projects(self, student_id, template):
        query = self.db.prepare('select * from project_list where user_id = $1')(student_id)
        polls = []
        for row in query:
            project = self.db.prepare('select * from project where project_id = $1')(row[0])
            project_dict = {x[0]: x[1] for x in zip(self.project, project[0])}
            project_dict = {k: project_dict[k] for k in set(project_dict) - set(template)}
            polls.append(project_dict)
        return polls

    def get_student_projects(self, user_id):
        if self.get_priority(user_id) == "student":
            return self.__get_user_projects(user_id, {"min_student": None, "max_student": None})
        else:
            raise AssertionError("User is not a student")

    def get_ta_projects(self, user_id):
        if self.get_priority(user_id) == "ta":
            return self.__get_user_projects(user_id, {})
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

    def __is_open(self, proj_dict):
        query_line = "select * from project where is_open = false and project_id in ({})". \
            format(', '.join(["$" + str(x) for x in range(1, len(proj_dict) + 1)]))
        if len(self.db.prepare(query_line)(*proj_dict.values())) != 0:
            raise AssertionError("One of projects is closed")

    def fill_poll(self, user_id, course_id, proj_dict):
        self.__is_open(proj_dict)
        with self.db.xact() as x:
            query_line = "insert into project_list ({}) values ($1,$2),($3,$4),($5,$6)". \
                format(', '.join(self.project_list.keys()))
            x.start()
            self.db.prepare(query_line)(*list(chain(*[[user_id, x] for x in proj_dict.values()])))
            self.db.prepare(
                "insert into poll ({}) values ($1,$2,$3,$4,$5)". \
                    format("user_id, course_id, " + ', '.join(proj_dict.keys())))(user_id, course_id, *proj_dict.values())
            self.db.prepare("insert into course_list (user_id, course_id) values ($1, $2)")(user_id, course_id)
            x.commit()

    def modify_poll(self, user_id, poll_id, proj_dict):
        self.__is_open(proj_dict)
        poll = self.db.prepare("select ({}) from poll where poll_id = $1 and user_id = $2". \
                               format(', '.join(proj_dict.keys())))(poll_id, user_id)[0]
        old = {x[1]: x[0] for x in zip(poll, proj_dict.keys())}
        if len(old) == 0:
            raise AssertionError("This poll doesn't belong to user")
        query = "update poll set ({}) = ({}) where poll_id = $1 and user_id = $2". \
            format(', '.join(proj_dict.keys()), ', '.join(["$" + str(x) for x in range(3, len(proj_dict) + 3)]))
        with self.db.xact() as t:
            t.start()
            self.db.prepare(query)(poll_id, user_id, *proj_dict.values())
            for x in old.keys():
                self.db.prepare("update project_list set project_id = $1 where user_id = $2 and project_id = $3") \
                    (proj_dict[x], user_id, old[x])
            t.commit()

    def get_user_info(self, user_id):
        user_row = self.db.prepare('select * from "user" where user_id = $1')(user_id)[0][1:]
        user_dict = {x[0]: x[1] for x in zip(self.user, user_row)}

        group_row = self.db.prepare('select * from study_group where group_id in '
                                    '(select group_id from group_list where user_id = $1)')(user_id)
        group_dict = [{x[0]: x[1] for x in zip(self.study_group, row[1:])} for row in group_row]

        course_row = self.db.prepare('select * from course where course_id in '
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
                return Record({x[0]: x[1] for x in zip(self.poll, self.db.prepare(
                    "select * from poll as k where user_id = $1 and course_id = $2")(user_id, course_id)[0][1:])})
            except IndexError:
                return None
        else:
            raise AssertionError("User is not a student")

    def get_course_polls(self, course_id):
        records = []
        from Alg.Record import Record
        for record in self.db.prepare("select * from poll where course_id = $1")(course_id):
            records.append(Record({x[0]: x[1] for x in zip(self.poll, record[1:])}))
        return records


    # auchtung injection is possible (but who gives a fuck?)
    # yeah evil abuser can plunge his dirty dick right about here

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

            group_list = []
            for x in group_table:
                record = self.group_list
                record['group_id'] = self.db.prepare('select group_id from study_group where "group"=$1') \
                    (x)[0][0]
                record['user_id'] = user_id
                group_list.append(record)

            self.db.prepare('insert into credentials ({}) values  ($1, $2, $3)'.
                            format(', '.join(credential_table.keys())))(*credential_table.values())
            for x in group_list:
                self.db.prepare('insert into group_list ({}) values ($1, $2)'.
                                format(', '.join(x.keys())))(*x.values())
            t.commit()
        return user_id

    def get_project_teams(self, project_id):
        teams = self.db.prepare('select * from team where project_id = $1')(project_id)
        teams_dict = []
        for row in teams:
            teams_dict.append({x[0]: x[1] for x in zip(self.team, row[1:])})
        return teams_dict

    def get_team_members(self, team_id):
        return {x[0]: x[1] for x in zip(self.team,
                                        self.db.prepare('select * from team where team_id=$1')(team_id)[0][1:])}

    def create_team(self, user_dict):
        user_dict = {x[0]: x[1] for x in user_dict.items() if x[1] is not None}

        insert = 'insert into team ({}) values ({}) returning team_id' \
            .format(', '.join(user_dict.keys()), ', '.join(['$' + str(x) for x in range(1, len(user_dict) + 1)]))
        with self.db.xact() as t:
            t.start()
            team_id = self.db.prepare(insert)(*user_dict.values())[0][0]

            for x in user_dict.items():
                if x[0].startswith('student'):
                    record = self.team_list
                    record['user_id'] = x[1]
                    record['team_id'] = team_id
                    self.db.prepare('insert into team_list ({}) values ($1, $2)'. \
                                    format(', '.join(record.keys())))(*record.values())
            t.commit()
        return team_id

    def clear_db(self):
        q = list(zip(*self.db.query("select table_name from information_schema.tables "
                                    "where table_schema = 'public' order by table_name")))[0]
        for x in q:
            try:
                if x not in undropable_tables:
                    self.db.execute('truncate "{}"'.format(x))
                    print("Table {} was truncated".format(x))
            except WrongObjectTypeError:
                pass


db = DbManager()
