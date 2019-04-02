from Alg.Algorithm import Algorithm
from Alg.Team import Team
from DB.db_manager import DbManager

a = Algorithm()
t = Team()
db = DbManager()

print(db.get_student(email='kek', password='lol'))

a.do_the_magic()
# r1 = db.get_student(student_id=1118)
# r2 = db.get_student(student_id=1119)
# r3 = db.get_student(student_id=1120)
# r4 = db.get_student(student_id=1121)
# r5 = db.get_student(student_id=1122)
# r1['project1'] = 1
# r2['project1'] = 1
# r3['project1'] = 1
# r4['project1'] = 1
# r5['project1'] = 1
# r1['role1'] = 1
# r2['role1'] = 1
# r3['role1'] = 1
# r4['role1'] = 1
# r5['role1'] = 1
# t = t + r1 + r2 + r3 + r4 + r5
#
# print(t)
# print(t.json_dump())
# print(t.happiness())
