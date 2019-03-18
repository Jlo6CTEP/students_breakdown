from DB import db_manager


class Record(dict):
    student_id = None
    name = None
    surname = None

    # record is dictionary of parameter : value pairs
    def __init__(self, sid, name, surname, record=None):
        self.student_id = sid
        self.name = name
        self.surname = surname
        # will raise an exception in case of incorrect input schema
        if record is not None:
            for x in db_manager.SHORT_SCHEMA:
                f = record[x]
            super().__init__(record)
        else:
            super().__init__({x: None for x in db_manager.SCHEMA})

    def normalize(self, vector):
        [self.update({x[0]: self[x[0]] * x[1] if self[x[0]] is not None else 0}) for x in zip(self.keys(), vector)]
