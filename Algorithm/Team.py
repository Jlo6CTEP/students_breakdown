from Algorithm.Record import Record


class Team:
    record_list = None

    def __init__(self):
        self.record_list = []

    def __add__(self, record):
        if isinstance(record, Record):
            self.record_list.append(record)
        else:
            raise ValueError("incorrect addend type : {}".format(type(record)))
        return self

    def __sub__(self, record):
        if isinstance(record, Record):
            self.record_list.remove(record)
        else:
            raise ValueError("incorrect minuend type : {}".format(type(record)))
        return self

    def __str__(self):
        return ', '.join([str(x) for x in self.record_list])

    def happiness(self):
        pass

    # data dump into moodle
    def dump_data(self):
        pass
