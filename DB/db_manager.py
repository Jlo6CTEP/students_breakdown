import postgresql
from itertools import chain
from postgresql.exceptions import WrongObjectTypeError

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

if __name__ == "__main__":
    settings.configure()

DB_url = "pq://zpgkwdlt:M4Ef1T1p8VmvYamieL-JR3ZK4J0hztBy@dumbo.db.elephantsql.com:5432/zpgkwdlt"

clearable_tables = ["poll", "team", "student_team_list", "course_list", "auth_user_groups"]

tables_with_pk = dict.fromkeys(["breakdown_course", "group_by",
                                "poll", "topic", "project",
                                "study_group", "team", "auth_user"])

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
]


class DbManager:
    db = None
    max_project_id = None
    max_lang_id = None

    def __init__(self):
        self.db = postgresql.open(DB_url)
        self.max_project_id = self.db.query("select max(project_id) from project")[0][0]
        self.max_lang_id = self.db.query("select max(language_id) from language")[0][0]

    def __getattr__(self, table_name):
        """
        Obtains schema of table with name table_name.
        call: DbManager_instance.table_name
        This also ignores first column of table that in tables_with_pk set
        This used to remove pk (which is first column here)
        :param table_name: name of table to obtain schema
        :return: dict with (column_name:none) pairs
        :raises AttributeError if there is no such table in db
        """
        r = self.db.prepare('select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = $1')(table_name)
        if table_name in tables_with_pk:
            r = r[1:]
        if len(r) == 0:
            raise AttributeError("Incorrect attribute name")
        setattr(self, table_name, dict.fromkeys(chain(*r)))
        return dict.fromkeys(chain(*r))

    def get_priority(self, user_id):
        """
        Obtains privilege of given user in textual form
        :param user_id: id of user to obtain privilege
        :return: privilege name
        :raises Various DB exceptions in case of incorrect input
        """
        return self.db.prepare('select "name" from auth_group where id in '
                               '(select group_id from auth_user_groups where user_id = $1)')(user_id)[0][0]

    def get_user_topics(self, user_id):
        """
        Obtains topics of given user in a list of dictionaries form
        :param user_id: user id to obtain topics
        :return: list of dicts, where
            keys correspond to column names of **topic** table
            values correspond to actual values of this column
        :raises Various DB exceptions in case of incorrect input
        """
        query = self.db.prepare('select * from user_topic_list where user_id = $1')(user_id)
        topics = []
        for row in query:
            topic = self.db.prepare('select * from topic where topic_id= $1')(row[1])
            project_dict = {x[0]: x[1] for x in zip(self.topic, topic[0])}
            topics.append(project_dict)
        return topics

    def get_ta_projects(self, user_id):
        """
        Obtains projects created by given TA in a list of dictionaries form
        :param user_id: id of TA to obtain projects
        :return: list of dicts where
            keys correspond to column names of **project** table
            values correspond to actual values of this column
        :raises AssertionError, if given user is not a TA
        """
        if self.get_priority(user_id) != "ta":
            raise AssertionError("User is not a TA")
        query = self.db.prepare("select project_id from project where project_id in "
                                "(select project_id from ta_project_list where user_id = $1)")(user_id)
        if len(query) == 0:
            return None
        projects = []
        for row in query:
            projects.append(self.get_project_info(row[0]))
        return projects

    def get_student_projects(self, user_id):
        """
        Obtains projects created of given student in a list of dictionaries form
        :param user_id: id of user to obtain projects
        :return: list of dicts where
            keys correspond to column names of **project** table
            values correspond to actual values of this column
        :raises AssertionError, if given user is not a student
        """
        if self.get_priority(user_id) != "student":
            raise AssertionError("User is not a student")
        query = self.db.prepare("select project_id from project where project_id in "
                                "(select project_id from group_project_list where group_id in "
                                "(select group_id from user_group_list where user_id = $1)) ")(user_id)
        if len(query) == 0:
            return None
        projects = []
        for row in query:
            projects.append(self.get_project_info(row[0]))
        return projects

    def create_new_project(self, user_id, project_info):
        """
        Creates new project with given initial information
        :param user_id: id of TA who creates the project
        :param project_info: info about project in a dictionary form, where
            keys correspond to column names of **project** table
            values correspond to values to be inserted
            plus this key and value
            groups : [list_of_groups]
        :return: id of newly created project
        :raises Various DB exceptions in case of incorrect input
        """
        if self.get_priority(user_id) != "ta":
            raise AssertionError("User is not a TA")
        with self.db.xact() as x:
            x.start()
            groups = project_info.pop('groups')
            query_line = "insert into project ({}) values ({}) returning project_id". \
                format(', '.join(project_info.keys()),
                       ', '.join(["$" + str(x) for x in range(1, len(project_info) + 1)]))
            project_id = self.db.prepare(query_line)(*project_info.values())[0][0]
            self.db.prepare("insert into ta_project_list (user_id,project_id) values ($1,$2)")(user_id, project_id)
            for f in groups:
                self.db.prepare('insert into group_project_list values ($1, '
                                '(select group_id from study_group where "group" = $2))')(project_id, f)
            x.commit()
            return project_id

    def __is_open(self, topics):
        """
        Check if projects of given topics are open
        :param topics: set of topics id to check
        :return: True if all projects are open, false otherwise
        """
        query_line = "select * from project where project_id in " \
                     "(select project_id from project_topic_list where topic_id in ({})) and due_date < now()". \
            format(', '.join(["$" + str(x) for x in range(1, len(topics) + 1)]))
        return len(self.db.prepare(query_line)(*topics.values())) == 0

    def fill_poll(self, user_id, poll_info):
        """
        Fills poll of given user with given data
        :param user_id: user which fills the poll
        :param poll_info: poll data in a dictionary form, where
            keys correspond to column names of **poll** table
            values correspond to values to be inserted
            Values must be ID
        :return: id of newly filled poll
        :raises AssertionError if some of projects are closed
        :raises Various DB exceptions in case of incorrect input
        """
        if not self.__is_open({x[0]: x[1] for x in poll_info.items() if x[0].startswith("topic")}):
            raise AssertionError("One of projects is closed")
        with self.db.xact() as x:
            query_line = "insert into user_topic_list ({}) values ($1,$2),($3,$4),($5,$6)". \
                format(', '.join(self.user_topic_list.keys()))
            x.start()
            self.db.prepare(query_line)(*list(chain(*[[user_id, x[1]] for x in poll_info.items()
                                                      if x[0].startswith("topic")])))

            poll_id = self.db.prepare("insert into poll ({}) values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10) returning poll_id".
                                      format("user_id, " + ', '.join(poll_info.keys())))(user_id, *poll_info.values())
            if len(self.db.prepare("select * from course_list where (user_id, course_id) = ($1, $2)")
                       (user_id, poll_info['course_id'])) == 0:
                self.db.prepare("insert into course_list (user_id, course_id) values ($1, $2)") \
                    (user_id, poll_info['course_id'])
            x.commit()
            return poll_id[0][0]

    def modify_poll(self, user_id, poll_id, poll_info):
        """
        Modifies given poll of given user
        :param user_id: user which own poll with poll_id id
        :param poll_id: poll to be modified
        :param poll_info: poll data wich will be modified in a dictionary form, where
            keys correspond to column names of **poll** table
            values correspond to values to be modified
            Values must be ID
        :return: None
        :raises Various DB exceptions in case of incorrect input
        :raises AssertionError if some of projects are closed
        :raises AssertionError if poll doesn't belong to user
        """
        if not self.__is_open(poll_info):
            raise AssertionError("One of projects is closed")
        poll = self.db.prepare("select ({}) from poll where poll_id = $1 and user_id = $2".
                               format(', '.join(poll_info.keys())))(poll_id, user_id)[0]
        old = {x[1]: x[0] for x in zip(poll, poll_info.keys())}
        if len(old) == 0:
            raise AssertionError("This poll doesn't belong to user")
        query = "update poll set ({}) = ({}) where poll_id = $1 and user_id = $2". \
            format(', '.join(poll_info.keys()), ', '.join(["$" + str(x) for x in range(3, len(poll_info) + 3)]))
        with self.db.xact() as t:
            t.start()
            self.db.prepare(query)(poll_id, user_id, *poll_info.values())
            for x in old.keys():
                self.db.prepare("update project_topic_list set project_id=$1 where topic_id=$2 and project_id = $3") \
                    (poll_info[x], user_id, old[x])
            t.commit()

    def get_user_info(self, user_id):
        """
        Obtains info about given user
        :param user_id: id of user to obtain info
        :return: user info in a dictionary form
            {
                name:name_of_user,
                surname:surname_of_user,
                email:email_of_user,
                study_group: set_of_study_groups
                course:set_of_courses
                priv_name: privilege name
            }
            if there is no such user, returns None
        """
        user_row = self.db.prepare('select first_name, last_name, email from auth_user where id = $1')(user_id)
        if len(user_row) == 0:
            return None
        user_row = user_row[0]
        user_dict = {x[0]: x[1] for x in zip(['first_name', 'last_name', 'email'], user_row)}
        user_dict.pop("priv_id")

        group_row = self.db.prepare('select * from study_group where group_id in '
                                    '(select group_id from user_group_list where user_id = $1)')(user_id)
        group_dict = {row[1:][0] for row in group_row}

        course_row = self.db.prepare('select * from breakdown_course where course_id in '
                                     '(select course_id from course_list where user_id = $1)')(user_id)
        course_dict = {row[1:][0] for row in course_row}

        priv_row = self.get_priority(user_id)
        priv_dict = {'priv_name', priv_row}

        user_dict.update({"study_group": group_dict})
        user_dict.update({"course": course_dict})
        user_dict.update(priv_dict)
        return user_dict

    def get_student_polls(self, user_id, project_id, de_idfy=True):
        """
        Obtains info about polls of given student in given project
        :param user_id: poll owner id
        :param project_id: id of course
        :return: list of Record(dict) objects of form
            {
                topic1: user_topic1,
                topic2: user_topic2,
                topic3: user_topic2,
                course: user_course,
                project: user_project
            }
        :raises Various DB exceptions in case of incorrect input
        :raises AssertionError, if given user is not a student
        """
        if self.get_priority(user_id) != "student":
            raise AssertionError("User is not a student")
        from Alg.Record import Record
        polls = []
        query = self.db.prepare("select * from poll where user_id = $1 and project_id = $2")(user_id, project_id)
        if len(query) == 0:
            return None
        for row in query:
            d = Record({x[0]: x[1] for x in zip(self.poll, row[1:])})
            if de_idfy:
                self.de_idfy(d)
            polls.append(d)
        return polls

    def get_project_polls(self, project_id):
        """
        Returns list of all polls of project
        :param project_id: id of project to get polls
        :return: all polls in a list of dictionaries form, where
            keys correspond to column names of **poll** table
            values correspond to values of polls
        """
        records = []
        from Alg.Record import Record
        for record in self.db.prepare("select * from poll where project_id = $1")(project_id):
            records.append(Record({x[0]: x[1] for x in zip(self.poll, record[1:])}))
        return records

    def check_credentials(self, username, password):
        """
        Check if this credentials are valid
        :param username:
        :param password:
        :return: False if credentials are invalid, dictionary of user data otherwise
        """
        pass_from_db = self.db.prepare("select * from auth_user where (username) = ($1)")(username)[0][1]
        if not check_password(password, pass_from_db):
            return False
        res = self.db.prepare("select id, username, first_name, last_name from auth_user where username = $1")(username)[0]
        columns = ("id", "username", "first_name", "last_name")
        ans = {x[0]: x[1] for x in zip(columns, res)}
        return ans

    def force_insert_user(self, registration_info):
        """
        Registers user with given registration data
        :param registration_info: input data in a dictionary form
        {
            password: user_password, 
            mail: user_mail,
            name: user_name, 
            surname: user_surname,
            study_group: [user_study_group] list, 
            username: user_nickname,
            priv_name: user_privilege
        }
        :return: id of newly registered user
        :raises AttributeError if username already exists
        :raises AttributeError if email is already in use
        :raises various DB errors if incorrect input
        """
        if len(self.db.prepare('select * from auth_user where username = $1')(registration_info['username'])) != 0:
            raise AttributeError("Username already exists")
        if len(self.db.prepare('select * from auth_user where email = $1')(registration_info['mail'])) != 0:
            raise AttributeError("Email is already in use")

        level = self.db.prepare('select id from auth_group where "name" = $1')(registration_info['priv_name'])[0][0]
        group_table = registration_info["study_group"]
        with self.db.xact() as t:
            t.start()

            registration_info['password'] = make_password(registration_info['password'])

            user_id = self.db.prepare('insert into auth_user ('
                                      'password, email, first_name, last_name, '
                                      'username, is_superuser, is_active, is_staff, date_joined) '
                                      'values ($1, $2, $3, $4, $5, FALSE, TRUE, FALSE, now()) returning id') \
                (*[registration_info[x] for x in ['password', 'mail', 'name', 'surname', 'username']])[0][0]

            user_group_list = []
            for x in group_table:
                record = self.user_group_list
                record['group_id'] = self.db.prepare('select group_id from study_group where "group"=$1') \
                    (x)[0][0]
                record['user_id'] = user_id
                user_group_list.append(record)

            self.db.prepare('insert into auth_user_groups (user_id, group_id) values ($1, $2)')(user_id, level)

            for x in user_group_list:
                self.db.prepare('insert into user_group_list ({}) values ($1, $2)'.
                                format(', '.join(x.keys())))(*x.values())
            t.commit()
        return user_id

    def get_project_teams(self, project_id):
        """
        Obtains teams assigned to given project
        :param project_id: id of project to obtain teams
        :return: project's teams in form of list of dicts where
            keys correspond to column names of **team** table
            values correspond to values from this table
        """
        teams = self.db.prepare('select * from team where topic_id in '
                                '(select topic_id from project_topic_list where project_id = $1)')(project_id)
        teams_dict = []
        for row in teams:
            d = {x[0]: x[1] for x in zip(self.team, row[1:])}
            self.de_idfy(d)
            teams_dict.append(d)
        return teams_dict

    def get_team_members(self, team_id):
        """
        Obtains members of given team
        :param team_id: team_id to obtain team members
        :return: list of team members in form of list of dicts,
        where each item is as described in get_user_info method
        """
        query = self.db.prepare('select user_id from student_team_list where team_id=$1')(team_id)
        teammatews = []
        for x in query:
            teammatews.append(self.get_user_info(x[0]))
        return teammatews

    def create_team(self, course_id, team):
        """
        Creates new team from given Team object
        :param team: Team object to insert
        :param course_id: course to create team in
        :return: newly created team id
        """

        insert = 'insert into team (topic_id, course_id) values ($1, $2) returning team_id'
        with self.db.xact() as t:
            t.start()
            team_id = self.db.prepare(insert)(team.topic_id, course_id)[0][0]

            for x in team:
                record = self.student_team_list
                record['user_id'] = x.user_id
                record['team_id'] = team_id
                self.db.prepare('insert into student_team_list ({}) values ($1, $2)'. \
                                format(', '.join(record.keys())))(*record.values())
            t.commit()
        return team_id

    def get_projects(self):
        """
        Obtains all information about all projects
        :return: projects info in form of list of dictionaries, where
            keys correspond to column names of **project** table
            values correspond to values from this table
        """
        projects = self.db.query('select * from project')
        projects_dict = []
        for row in projects:
            d = {x[0]: x[1] for x in zip(self.project, row[1:])}
            self.de_idfy(d)
            projects_dict.append(d)
        return projects_dict

    def get_project_info(self, project_id):
        """
        Obtains all information about project
        :param project_id: project id to obtain information
        :return: project info in form of dictionary, where
            keys correspond to column names of **project** table
            values correspond to values from this table
        """
        project = self.db.prepare("select * from project where project_id = $1")(project_id)[0]
        d = {x[0]: x[1] for x in zip(self.project, project[1:])}
        self.de_idfy(d)
        return d

    def remove_project(self, project_id):
        """
        removes project by it's id
        :param project_id: project id to delete
        :return: None
        """
        self.db.prepare("delete from project where project_id = $1")(project_id)
        self.db.prepare("delete from project_topic_list where project_id = $1")(project_id)
        self.db.prepare("delete from group_project_list where project_id = $1")(project_id)
        self.db.prepare("delete from ta_project_list where project_id = $1")(project_id)

    def __de_idfy_course(self, course_dict):
        if 'course_id' not in course_dict:
            return
        course = self.db.prepare("select name from breakdown_course where course_id=$1")(course_dict['course_id'])
        course_dict['course'] = None if len(course) == 0 else course[0][0]

    def __de_idfy_group_by(self, group_dict):
        if 'group_by' not in group_dict:
            return
        group = self.db.prepare("select group_by.group_by from group_by where grouping_id=$1")(group_dict['group_by'])
        group_dict['group_by'] = None if len(group) == 0 else group[0][0]

    def __de_idfy_project(self, project_dict):
        if 'project_id' not in project_dict:
            return
        group = self.db.prepare("select project_name from project where project_id=$1")(project_dict['project_id'])
        project_dict['project'] = None if len(group) == 0 else group[0][0]

    def __de_idfy_topics(self, topics_dict):
        schema = {x[0]: x[1] for x in topics_dict.items() if x[0].startswith('topic')}
        if len(schema) == 0:
            return
        line = "select topic_name from topic where topic_id in ({})". \
            format(', '.join(['$' + str(x) for x in range(1, len(schema) + 1)]))
        updater = {x[0]: x[1][0] for x in zip(schema.keys(), self.db.prepare(line)(*schema.values()))}
        topics_dict.update(updater)

    def de_idfy(self, dictionary):
        self.__de_idfy_course(dictionary)
        self.__de_idfy_group_by(dictionary)
        self.__de_idfy_project(dictionary)
        self.__de_idfy_topics(dictionary)

    def clear_db(self):
        """
        clears all tables that in clearable_tables list
        :return: None
        """
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
