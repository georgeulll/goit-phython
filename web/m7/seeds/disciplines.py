import random

from database.db import session
from database.models import Teacher, Discipline



DISCIPLINES = [
    "Малювання",
    "Фізкультура",
    "Читання",
    "Математика",
    "Географія",
    "Історія України",
    "Англійська",
    "Уроки праці"
]


def seed_disciplines():
    teachers = session.query(Teacher).all()

    for discip in DISCIPLINES:
        teacher = random.choice(teachers)
        discipline = Discipline(
            name=discip,
            teacher_id=teacher.id)

        session.add(discipline)
    session.commit()



def seed_students():
    students = [fake.name() for _ in range(NUMBER_STUDENTS)]
    sql = "INSERT INTO students (name, group_id) VALUES(?, ?); "
    cur.executemany(sql, zip(students, iter(randint(1, len(GROUPS)) for _ in range(NUMBER_STUDENTS))))



if __name__ == '__main__':
    seed_disciplines()