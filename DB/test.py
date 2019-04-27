from Alg.Algorithm import Algorithm
from Alg.Solution import Solution
from DB.db_manager import db

from datetime import datetime

dt = datetime.now()
"""Db manager"""
#b.create_new_project(36, {'project_name': 'test', 'course_id': 3,
#                          'min_student': 3, 'max_student': 5, 'group_by': 5,
#                          'due_date': dt,
#                          'groups': ['bs17-2', 'bs17-3']})

#db.get_ta_projects(36)


#a = db.force_insert_user({"password": '1488', "mail": 'c.sucker@innopolis.ru',
#                            "name": 'john', "surname": 'smith',
#                            "study_group": ['bs17-2'], "username": 'johnsmith',
#                            "priv_name": "student"})
#print(a)
a = 22

#db.fill_poll(a, {"topic1": 1, "topic2": 3, "topic3": 2, "course_id": 3, "project_id": 15})
print(db.get_student_projects(a))
#print(db.get_student_polls(a, 15))
#print(db.get_project_teams(15))
#print(db.get_projects())
#print(db.get_project_info(15))
#a = db.get_project_polls(15)
#print(a)
#print(a[0].de_idfy())
#print()

"""Algorithm"""
# a = Algorithm(15)
# print(a.do_the_magic())

# r1 = db.get_student_polls(830, 15)[0]
# r2 = db.get_student_polls(831, 15)[0]
# r3 = db.get_student_polls(852, 15)[0]
# r4 = db.get_student_polls(853, 15)[0]
# r5 = db.get_student_polls(834, 15)[0]
# r6 = db.get_student_poll(855, 3)
# r7 = db.get_student_poll(836, 3)
# r8 = db.get_student_poll(837, 3)
# r9 = db.get_student_poll(838, 3)
# r10 = db.get_student_poll(840, 3)
# r11 = db.get_student_poll(841, 3)
# r12 = db.get_student_poll(842, 3)
# r13 = db.get_student_poll(843, 3)
# r14 = db.get_student_poll(844, 3)
# r15 = db.get_student_poll(845, 3)
#
# t1 = sum([r1, r2, r3, r4, r5])
# t1.assign_topic()
# print(db.create_team(3, t1))
# t2 = sum([r6, r7, r8, r9, r10])
# t3 = sum([r11, r12, r13, r14, r15])
#
# print(t1.happiness())
#
# solution = Solution()
# solution.add_team(t1)
# solution.add_team(t2)
# solution.add_team(t3)
# print()
