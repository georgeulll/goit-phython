from faker import Faker

from database.db import session
from database.models import Teacher


NUMBER_TEACHERS = 5

fake = Faker('uk_UA')


def seed_teachers():
    for _ in range(NUMBER_TEACHERS):
        teacher = Teacher(fullname=fake.name())

        session.add(teacher)
    session.commit()


if __name__ == '__main__':
    seed_teachers()