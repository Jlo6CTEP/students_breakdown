from Alg.Record import Record
from DB.db_manager import MAX_GRADE, NAMES, CREDENTIALS, DbManager
import json

MEMBER_COUNT = 5
db = DbManager()


class Team:
    record_list = None
    name = None

    def __init__(self, name):
        self.name = name
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
        return '\n '.join([str(x) for x in self.record_list])

    def happiness(self, priority_vector):
        for x in range(MEMBER_COUNT):
            self.record_list[x].normalize(self.normalizing_vector())

        arg = [[] for x in range(len(priority_vector))]
        x = 0
        i = 0
        while x < len(self.record_list[0]) - 2:
            for f in range(priority_vector[i][1]):
                arg[i].append([list(self.record_list[z].values())[x] for z in range(MEMBER_COUNT)])
                x += 1
            i += 1

        x = 0
        i = 0
        arg_priority = list(zip(arg, priority_vector))
        for x in range(len(arg_priority)):
            for f in range(len(arg_priority[x][0])):
                temp = arg_priority[x][0][f]

                if arg_priority[x][1][3]:
                    if arg_priority[x][1][0]:
                        arg_priority[x][0][f] = (MAX_GRADE - (max(temp) - min(temp)) ** arg_priority[x][1][2]) / (
                                    f + 1) ** 8
                    else:
                        arg_priority[x][0][f] = ((max(temp) - min(temp)) ** arg_priority[x][1][2]) / (f + 1) ** 8
                else:
                    if not arg_priority[x][1][0]:
                        arg_priority[x][0][f] = ((len(set(temp)) * 10 / len(temp)) ** arg_priority[x][1][2]) / (
                                f + 1) ** 8
                    else:
                        arg_priority[x][0][f] = (((len(temp) - len(set(temp))) * 10 / len(temp))
                                                 ** arg_priority[x][1][2]) / (f + 1) ** 8

        happiness = sum([max(x[0]) for x in arg_priority])
        return happiness

    def normalizing_vector(self):
        return list(map(lambda x: MAX_GRADE / x, db.max_ids))

    def json_dump(self):
        data = {self.name: [{x[1]: x[0] for x in zip([x.name, x.surname], NAMES)}
                for x in self.record_list]}
        return json.dumps(data)

