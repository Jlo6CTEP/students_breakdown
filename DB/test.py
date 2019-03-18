from Alg.Algorithm import Algorithm
from Alg.Team import Team
from DB.db_manager import DbManager

t = Team()
db = DbManager()
a = Algorithm()
r1 = db.get_student(student_id=1118)
r2 = db.get_student(student_id=1119)
r3 = db.get_student(student_id=1120)
r4 = db.get_student(student_id=1121)
r5 = db.get_student(student_id=1122)

t = t + r1 + r2 + r3 + r4 + r5

print(t)
print(t.happiness(a.priority_vector()))
