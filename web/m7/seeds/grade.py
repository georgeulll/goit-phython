from faker import Faker

import random
from datetime import datetime, timedelta

from database.db import session
from database.models import Discipline, Student, Grade


fake = Faker('uk_UA')


def seed_grades():

    def random_date(start, end):
            """
            This function will return a random datetime between two datetime
            objects.
            """
            delta = end - start
            int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
            random_second = random.randrange(int_delta)
            new_date = start + timedelta(seconds=random_second)
            return new_date.date()

    start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-06-15", "%Y-%m-%d")

    disciplines = session.query(Discipline).all()
    students = session.query(Student).all()

    for student in students:
        for discipline in disciplines:
            grade_data = Grade(discipline_id=discipline.id,
                               student_id=student.id,
                               grade=random.randint(1, 100),
                               date_of=random_date(start_date, end_date)
                               )

            session.add(grade_data)
    session.commit()


if __name__=='__main__':
    seed_grades()