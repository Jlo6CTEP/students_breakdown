import random

from anytree import Node, RenderTree
import xlsxwriter
from Alg.Solution import Solution
from DB.db_manager import db


class Algorithm:
    solution = None
    min_student = None
    max_student = None
    survey_id = None

    def __init__(self, survey_id):
        super().__init__()
        self.solution = Solution()
        self.survey_id = survey_id
        survey = db.get_survey_by_id(survey_id)
        self.min_student, self.max_student = survey['min_student'], survey['max_student']

    def do_the_magic(self):
        records = db.get_survey_polls(self.survey_id)

        for x in range(3, 0, -1):
            records.sort(key=lambda f: f['topic{}'.format(x)])

        groups = []

        for x in records:
            if len(groups) == 0 or groups[len(groups) - 1][0]['topic1'] != x['topic1']:
                groups.append([x])
            else:
                groups[len(groups) - 1].append(x)

        trashcan = []

        for x in range(len(groups)):
            tree = Node("init")
            flag = True
            ret = [Node("init")]
            self.__recurse_tree(tree, len(groups[x]), [flag], ret)
            tree = [x.name for x in ret[0].path[1:]]
            temp = groups[x]
            groups[x] = []
            for f in tree[: len(tree) - 1]:
                groups[x].append(temp[:f])
                temp = temp[f:]
            trashcan += temp

        for max_survey in range(db.max_topic_id):
            team = []
            for x in trashcan:
                if x['topic1'] == max_survey or x['topic2'] == max_survey:
                    team.append(x)
            if self.max_student > len(team) > self.min_student:
                pass
            elif self.max_student < len(team):
                team = team[:(self.max_student + self.min_student) // 2 + 1]
            else:
                for x in trashcan:
                    if x['topic3'] == max_survey:
                        team.append(x)
            if self.max_student < len(team):
                team = team[:(self.max_student + self.min_student) // 2 + 1]

            if self.max_student >= len(team) >= self.min_student:
                for x in team:
                    trashcan.remove(x)
                groups[0].append(team)
            print()

        self.solution = Solution()

        for x in groups:
            if len(x) != 0:
                for f in x:
                    self.solution.add_team(sum(f))

        while len(trashcan) != 0:
            random_team = random.choice(self.solution)
            if len(random_team.team) > self.max_student:
                pass
            else:
                random_team += trashcan.pop(0)

        for x in self.solution:
            x.assign_topic()
        print(self.solution.happiness())

        workbook = xlsxwriter.Workbook('result.xlsx')
        sheet = workbook.add_worksheet('Students teams')

        sheet.write(0, 0, 'topic')
        sheet.write(0, 1, 'users')
        sheet.write(0, 1 + self.max_student, 'happiness')

        for x in range(len(self.solution)):
            print(x)
            sheet.write(x + 1, 0, db.db.prepare('select topic_name from topic where topic_id = $1')\
                (self.solution[x].topic_id)[0][0])
            for f in range(len(self.solution[x].team)):
                s = db.db.prepare('select first_name, last_name from auth_user where id = $1')\
                    (self.solution[x].team[f].user_id)[0]
                sheet.write(x + 1, 1 + f, s[0] + ' ' + s[1])
                sheet.write(x + 1, 1 + self.max_student, self.solution[x].happiness())
        workbook.close()

        return self.solution

    def __recurse_tree(self, node, records, flag, ret):
        if records == 0:
            null_node = Node(0, parent=node)
            ret[0] = null_node
            flag[0] = False
            return
        for x in range(self.min_student, self.max_student + 1):
            next_node = Node(x, parent=node)
            if flag[0]:
                if records - x >= 0:
                    self.__recurse_tree(next_node, records - x, flag, ret)
                else:
                    ret[0] = Node(records, parent=node)
                    flag[0] = False
                    return
