from anytree import Node, RenderTree

from Alg.Solution import Solution
from DB.db_manager import db


class Algorithm:
    solution = None
    min_student = None
    max_student = None
    course_id = None

    def __init__(self, course_id):
        super().__init__()
        self.solution = Solution()
        self.course_id = course_id
        self.min_student, self.max_student = \
            db.db.prepare("select min_student, max_student from project where course_id = $1") \
            (self.course_id)[0]

    def do_the_magic(self):
        records = db.get_course_polls(self.course_id)

        for x in range(3, 0, -1):
            records.sort(key=lambda f: f['project{}'.format(x)])
            print()

        tree = Node("init")
        flag = True
        ret = [Node("init")]
        self.__recurse_tree(tree, len(records), [flag], ret)

        for x in ret[0].path[1:]:
            self.solution.add_team(sum(records[:x.name]))
            records = records[x.name - 1:]
        for x in self.solution:
            x.assign_project()
        print(self.solution.happiness())
        return self.solution

    def __recurse_tree(self, node, records, flag, ret):
        if records < 0:
            return
        if records == 0:
            ret[0] = node
            flag[0] = False
            return
        for x in range(self.max_student, self.min_student - 1, -1):
            next_node = Node(x, parent=node)
            if flag[0]:
                self.__recurse_tree(next_node, records - x, flag, ret)





