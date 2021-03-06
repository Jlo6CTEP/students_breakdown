import Alg

PROJECT_HAPPINESS = 10


class Team(list):
    topic_id = None
    __happiness_var = None

    def __init__(self, f=None):
        if f is not None:
            super().__init__(f)
        else:
            super().__init__()
        self.topic_id = None
        self.__happiness_var = None

    def __add__(self, record):
        if isinstance(record, Alg.Record.Record):
            self.record_list.append(record)
        else:
            raise ValueError("incorrect addend type : {}".format(type(record)))
        return self

    def __sub__(self, record):
        if isinstance(record, Alg.Record.Record):
            self.record_list.remove(record)
        else:
            raise ValueError("incorrect minuend type : {}".format(type(record)))
        return self

    def __get_priority_stack(self):
        if self.__happiness_var:
            return self.__happiness_var
        else:
            values = dict.fromkeys(self[0].keys())

            for rec in self[0].keys():
                values[rec] = list([x[rec] for x in self])

            from DB.db_manager import db
            stack = [0 for x in range(db.max_project_id)]

            multiplier = 1
            for x in values.items():
                if x[0].startswith("topic"):
                    for f in x[1]:
                        stack[f] += PROJECT_HAPPINESS * multiplier
                multiplier /= 2
            return stack

    def assign_topic(self):
            stack = self.__get_priority_stack()
            max_happiness, index = 0, 0
            for x in range(len(stack)):
                if stack[x] > max_happiness:
                    max_happiness = stack[x]
                    index = x
            self.topic_id = index

    def happiness(self):
        stack = self.__get_priority_stack()
        return max(stack)/len(self)
