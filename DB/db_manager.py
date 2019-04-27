import hashlib
import postgresql
from itertools import chain
from postgresql.exceptions import WrongObjectTypeError

from django.conf import settings
from django.contrib.auth.hashers import make_password

settings.configure()

DB_url = "pq://zpgkwdlt:M4Ef1T1p8VmvYamieL-JR3ZK4J0hztBy@dumbo.db.elephantsql.com:5432/zpgkwdlt"

clearable_tables = ["poll", "team", "student_team_list", "course_list", "auth_user_groups"]

tables_with_pk = dict.fromkeys(["breakdown_course", "group_by",
                                "poll", "topic", "survey",
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
    max_survey_id = None
    max_lang_id = None

    def __init__(self):
        self.db = postgresql.open(DB_url)
        self.max_survey_id = self.db.query("select max(survey_id) from survey")[0][0]
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
            survey_dict = {x[0]: x[1] for x in zip(self.topic, topic[0])}
            topics.append(survey_dict)
        return topics

    def get_ta_surveys(self, user_id):
        """
        Obtains surveys created by given TA in a list of dictionaries form
        :param user_id: id of TA to obtain surveys
        :return: list of dicts where
            keys correspond to column names of **survey** table
            values correspond to actual values of this column
        :raises AssertionError, if given user is not a TA
        """
        if self.get_priority(user_id) != "ta":
            raise AssertionError("User is not a TA")
        query = self.db.prepare("select survey_id from survey where survey_id in "
                                "(select survey_id from ta_survey_list where user_id = $1)")(user_id)
        if len(query) == 0:
            return None
        surveys = []
        for row in query:
            surveys.append(self.get_survey_by_id(row[0]))
        return surveys

    def get_student_surveys(self, user_id):
        """
        Obtains surveys of given student in a list of dictionaries form
        :param user_id: id of user to obtain surveys
        :return: list of dicts where
            keys correspond to column names of **survey** table
            values correspond to actual values of this column
        :raises AssertionError, if given user is not a student
        """
        if self.get_priority(user_id) != "student":
            raise AssertionError("User is not a student")
        query = self.db.prepare("select survey_id from survey where survey_id in "
                                "(select survey_id from group_survey_list where group_id in "
                                "(select group_id from user_group_list where user_id = $1)) ")(user_id)
        if len(query) == 0:
            return None
        surveys = []
        for row in query:
            surveys.append(self.get_survey_by_id(row[0]))
        return surveys

    def create_survey(self, user_id, survey_info):
        """
        Creates new survey with given initial information
        :param user_id: id of TA who creates the survey
        :param survey_info: info about survey in a dictionary form, where
            keys correspond to column names of **survey** table
            values correspond to values to be inserted
            plus this key and value
            groups : [list_of_groups]
        :return: id of newly created survey
        :raises Various DB exceptions in case of incorrect input
        """
        if self.get_priority(user_id) != "ta":
            raise AssertionError("User is not a TA")
        with self.db.xact() as x:
            x.start()
            groups = survey_info.pop('groups')
            query_line = "insert into survey ({}) values ({}) returning survey_id". \
                format(', '.join(survey_info.keys()),
                       ', '.join(["$" + str(x) for x in range(1, len(survey_info) + 1)]))
            survey_id = self.db.prepare(query_line)(*survey_info.values())[0][0]
            self.db.prepare("insert into ta_survey_list (user_id,survey_id) values ($1,$2)")(user_id, survey_id)
            for f in groups:
                self.db.prepare('insert into group_survey_list values ($1, '
                                '(select group_id from study_group where "group" = $2))')(survey_id, f)
            x.commit()
            return survey_id

    def get_surveys(self):
        """
        Obtains all information about all surveys
        :return: surveys info in form of list of dictionaries, where
            keys correspond to column names of **survey** table
            values correspond to values from this table
        """
        surveys = self.db.query('select * from survey')
        surveys_dict = []
        for row in surveys:
            d = {x[0]: x[1] for x in zip(self.survey, row[1:])}
            self.de_idfy(d)
            surveys_dict.append(d)
        return surveys_dict

    def update_survey(self, survey_id, survey_info):
        line = "update survey set ({}) = ({}) where survey_id = {}". \
            format(','.join(survey_info.keys()),
                   ','.join(["$" + str(x) for x in range(1, len(survey_info) + 1)]), "$" + str(len(survey_info) + 1))
        self.db.prepare(line)(*survey_info.values(), survey_id)

    def get_survey_by_id(self, survey_id):
        """
        Obtains all information about survey
        :param survey_id: survey id to obtain information
        :return: survey info in form of dictionary, where
            keys correspond to column names of **survey** table
            values correspond to values from this table
        """
        survey = self.db.prepare("select * from survey where survey_id = $1")(survey_id)[0]
        d = {x[0]: x[1] for x in zip(self.survey, survey[1:])}
        self.de_idfy(d)
        return d

    def delete_survey(self, survey_id):
        """
        removes survey by it's id
        :param survey_id: survey id to delete
        :return: 0 if nothing was deleted otherwise not 0
        """
        a = self.db.prepare("delete from survey where survey_id = $1")(survey_id)[1]
        a += self.db.prepare("delete from survey_topic_list where survey_id = $1")(survey_id)[1]
        a += self.db.prepare("delete from group_survey_list where survey_id = $1")(survey_id)[1]
        a += self.db.prepare("delete from ta_survey_list where survey_id = $1")(survey_id)[1]
        return a

    def __is_open(self, topics):
        """
        Check if surveys of given topics are open
        :param topics: set of topics id to check
        :return: True if all surveys are open, false otherwise
        """
        query_line = "select * from survey where survey_id in " \
                     "(select survey_id from survey_topic_list where topic_id in ({})) and due_date < now()". \
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
        :raises AssertionError if some of surveys are closed
        :raises Various DB exceptions in case of incorrect input
        """
        if not self.__is_open({x[0]: x[1] for x in poll_info.items() if x[0].startswith("topic")}):
            raise AssertionError("One of surveys is closed")
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
        :raises AssertionError if some of surveys are closed
        :raises AssertionError if poll doesn't belong to user
        """
        if not self.__is_open(poll_info):
            raise AssertionError("One of surveys is closed")
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
                self.db.prepare("update survey_topic_list set survey_id=$1 where topic_id=$2 and survey_id = $3") \
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

    def get_student_polls(self, user_id, survey_id, de_idfy=True):
        """
        Obtains info about polls of given student in given survey
        :param de_idfy: will actual values or ids be returned
        :param user_id: poll owner id
        :param survey_id: id of course
        :return: list of Record(dict) objects of form
            {
                topic1: user_topic1,
                topic2: user_topic2,
                topic3: user_topic2,
                course: user_course,
                survey: user_survey
            }
        :raises Various DB exceptions in case of incorrect input
        :raises AssertionError, if given user is not a student
        """
        if self.get_priority(user_id) != "student":
            raise AssertionError("User is not a student")
        from Alg.Record import Record
        polls = []
        query = self.db.prepare("select * from poll where user_id = $1 and survey_id = $2")(user_id, survey_id)
        if len(query) == 0:
            return None
        for row in query:
            d = Record({x[0]: x[1] for x in zip(self.poll, row[1:])})
            if de_idfy:
                self.de_idfy(d)
            polls.append(d)
        return polls

    def get_survey_polls(self, survey_id):
        """
        Returns list of all polls of survey
        :param survey_id: id of survey to get polls
        :return: all polls in a list of dictionaries form, where
            keys correspond to column names of **poll** table
            values correspond to values of polls
        """
        records = []
        from Alg.Record import Record
        for record in self.db.prepare("select * from poll where survey_id = $1")(survey_id):
            records.append(Record({x[0]: x[1] for x in zip(self.poll, record[1:])}))
        return records

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

    def get_team(self, team_id):
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

    def get_all_teams(self, survey_id):
        """
        Obtains teams assigned to given survey
        :param survey_id: id of survey to obtain teams
        :return: survey's teams in form of list of dicts where
            keys correspond to column names of **team** table
            values correspond to values from this table
        """
        teams = self.db.prepare('select * from team where topic_id in '
                                '(select topic_id from survey_topic_list where survey_id = $1)')(survey_id)
        teams_dict = []
        for row in teams:
            d = {x[0]: x[1] for x in zip(self.team, row[1:])}
            self.de_idfy(d)
            teams_dict.append(d)
        return teams_dict

    def update_team(self, team_id, data):
        """
        updates team info with new values in data
        :param team_id: it of team to update
        :param data: dictionary of key-value pairs where
            keys correspond to column names of **team** table
            values correspond to values to be updated
        :return:
        """
        line = "update team set ({}) = ({}) where team_id = {}". \
            format(','.join(data.keys()),
                   ','.join(["$" + str(x) for x in range(1, len(data) + 1)]), "$" + str(len(data) + 1))
        self.db.prepare(line)(*data.values(), team_id)

    def update_team_member(self, team_id, old_user, new_user):
        self.db.prepare("update student_team_list set user_id = $1 where team_id = $2 and user_id = $3")\
            (new_user, team_id, old_user)

    def delete_team(self, team_id):
        """
        removes team
        :param team_id: id of team to be removed
        :return: 0 if nothing was deleted, otherwise not 0
        """
        a = self.db.prepare("delete from team where team_id = $1")(team_id)[1]
        a += self.db.prepare("delete from student_team_list where team_id = $1")(team_id)[1]
        return a

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

    def __de_idfy_survey(self, survey_dict):
        if 'survey_id' not in survey_dict:
            return
        group = self.db.prepare("select survey_name from survey where survey_id=$1")(survey_dict['survey_id'])
        survey_dict['survey'] = None if len(group) == 0 else group[0][0]

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
        self.__de_idfy_survey(dictionary)
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
