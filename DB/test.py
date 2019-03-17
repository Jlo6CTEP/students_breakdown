from Algorithm.Team import Team
from DB.db_manager import DbManager

#t = Team()
db = DbManager()
#r1 = db.get_student(student_id=505)
#r2 = db.get_student(student_id=504)
#r3 = db.get_student(student_id=503)
#r4 = db.get_student(student_id=502)
#r5 = db.get_student(student_id=501)
#
#t = t + r1 + r2 + r3 + r4 + r5
#print(t)


print(db.get_max_ids())