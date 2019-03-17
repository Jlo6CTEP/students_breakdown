from DB import db_manager


class Record(dict):

    # record is dictionary of parameter : value pairs
    def __init__(self, record=None, **kwargs):
        # will raise an exception in case of incorrect input schema
        super().__init__(**kwargs)
        if record is not None:
            for x in db_manager.SHORT_SCHEMA:
                f = record[x]
        else:
            record = {x: None for x in db_manager.SCHEMA}

    def normalize(self, bitmask, vector):
        pass
