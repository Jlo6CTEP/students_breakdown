from DB import db_manager
from DB.db_manager import MAX_GRADE, DbManager

db = DbManager()


class Record(dict):
    student_id = None
    name = None
    surname = None
    email = None
    password = None

    # record is dictionary of parameter : value pairs
    def __init__(self, sid, name, surname, email, password, record=None):
        self.student_id = sid
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        # will raise an exception in case of incorrect input schema
        if record is not None:
            for x in db_manager.SHORT_SCHEMA:
                f = record[x]
            super().__init__(record)
        else:
            super().__init__({x: None for x in db_manager.SHORT_SCHEMA})

    def normalize(self):
        [self.update({x[0]: round(self[x[0]] * x[1]) if self[x[0]] is not None else 0}) for x in
         zip(self.keys(), self.normalizing_vector())]

    def normalizing_vector(self):
        return list(map(lambda x: MAX_GRADE / x, db.max_ids))
