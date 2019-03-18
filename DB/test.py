from Alg.Algorithm import Algorithm
from Alg.Team import Team
from DB.db_manager import DbManager

t = Team()
db = DbManager()
a = Algorithm()
r1 = db.get_student(student_id=618)
r2 = db.get_student(student_id=619)
r3 = db.get_student(student_id=620)
r4 = db.get_student(student_id=621)
r5 = db.get_student(student_id=622)

t = t + r1 + r2 + r3 + r4 + r5

print(t)
print(t.happiness(a.priority_vector()))
