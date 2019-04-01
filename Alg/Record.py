from DB.db_manager import db


class Record(dict):
    user_id = None

    # record is dictionary of parameter : value pairs
    def __init__(self, d=None):
        if d:
            self.user_id = d.pop("user_id")
            super().__init__(d)
        else:
            super().__init__()

    def poll_info(self):
        return {x[0]: self[x[0]] for x in db.poll}

    def personal_info(self):
        return {x[0]: self[x[0]] for x in set(self) - set(db.poll)}

    def __add__(self, record):
        if isinstance(record, Record):
            from Alg.Team import Team
            t = Team() + self + record
            return t
        else:
            raise ValueError("incorrect addend type : {}".format(type(record)))

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self + other
