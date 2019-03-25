from DB.db_manager import *


def normalizing_vector():
    return list(map(lambda x: MAX_GRADE / x, db.max_ids))


class Record(dict):
    student_id = None
    name = None
    surname = None
    email = None
    password = None

    # record is dictionary of parameter : value pairs
    def __init__(self, name, surname, email, password, record=None,  sid=None):
        self.student_id = sid
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        # will raise an exception in case of incorrect input schema
        if record is not None:
            for x in SHORT_SCHEMA:
                f = record[x]
            super().__init__(record)
        else:
            super().__init__({x: None for x in SHORT_SCHEMA})

    def normalize(self):
        [self.update({x[0]: round(self[x[0]] * x[1]) if self[x[0]] is not None else 0}) for x in
         zip(self.keys(), normalizing_vector())]
