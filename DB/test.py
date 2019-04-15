from Alg.Algorithm import Algorithm
from Alg.Solution import Solution
from DB.db_manager import db

print(db.get_team_members(15))
print(db.get_student_polls(772, 15))
print(db.get_project_teams(15))
print(db.get_projects())
print(db.get_project_info(15))
a = db.get_team_members(15)
print(a)
a = db.get_project_polls(15)
print(a[0].de_idfy())
print()
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
