import Alg

PROJECT_HAPPINESS = 10


class Team:
    team = None
    topic_id = None
    __happiness_var = None

    def __init__(self, f=None):
        if f is not None:
            super().__init__(f)
        else:
            super().__init__()
        self.topic_id = None
        self.__happiness_var = None
        self.team = []

    def __add__(self, record):
        if isinstance(record, Alg.Record.Record):
            self.team.append(record)
        else:
            raise ValueError("incorrect addend type : {}".format(type(record)))
        self.__happiness_var = None
        return self

    def __sub__(self, record):
        if isinstance(record, Alg.Record.Record):
            self.team.remove(record)
        else:
            raise ValueError("incorrect minuend type : {}".format(type(record)))
        self.__happiness_var = None
        return self

    def __get_priority_stack(self):
        if self.__happiness_var:
            return self.__happiness_var
        else:
            values = dict.fromkeys([x for x in self.team[0].keys() if x.startswith('topic')])

            for rec in self.team[0].keys():
                values[rec] = list([x[rec] for x in self.team])

            from DB.db_manager import db
            stack = [0 for x in range(db.max_topic_id + 1)]

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
        return max(stack)/len(self.team)
