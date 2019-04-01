from anytree import Node, RenderTree
from DB.db_manager import db


class Algorithm(list):
    min_student = None
    max_student = None
    course_id = None

    def __init__(self, course_id):
        super().__init__()
        self.course_id = course_id
        self.min_student, self.max_student = \
            db.db.prepare("select min_student, max_student from project where course_id = $1") \
            (self.course_id)[0]

    def do_the_magic(self):
        records = db.get_course_polls(self.course_id)[:100]

        for x in range(3, 0, -1):
            records.sort(key=lambda f: f['project{}'.format(x)])

        tree = Node("init")
        print("recursion start")
        self.__recurse_tree(tree, len(records))

        print("recursion end")
        for pre, fill, node in RenderTree(tree):
            print("%s%s" % (pre, node.name))

    def __recurse_tree(self, node, records):
        for x in range(self.max_student, self.min_student - 1, -1):
            if records < x:
                next_node = Node(records, parent=node)
                return
            else:
                next_node = Node(x, parent=node)
                self.__recurse_tree(next_node, records - x)





