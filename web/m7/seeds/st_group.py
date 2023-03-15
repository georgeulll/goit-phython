from database.db import session
from database.models import StudentGroup


GROUPS = ['Росток', 'Сонечко', 'Бджілка']


def seed_groups():
    for group in GROUPS:
        student_group = StudentGroup(
            name=group)

        session.add(student_group)
    session.commit()


if __name__ == '__main__':
    seed_groups()