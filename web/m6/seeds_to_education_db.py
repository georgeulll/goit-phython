from datetime import datetime, timedelta
import sqlite3
from psycopg2 import Error
from faker import Faker
from random import randint, randrange
from pprint import pprint

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

GROUPS = ['Росток', 'Сонечко', 'Бджілка']
NUMBER_TEACHERS = 5
NUMBER_STUDENTS = 50
fake = Faker()

connect = sqlite3.connect('education_db')
cur = connect.cursor()



def execute_command(conn, sql, param):
    try:
        c = conn.cursor()
        c.executemany(sql, param)
        c.close()
    except Error as e:
        print(e)


def seed_teachers():
    teachers = [fake.name() for _ in range(NUMBER_TEACHERS)]
    sql = "INSERT INTO teachers(fullname) VALUES(?);"
    cur.executemany(sql, zip(teachers, ))


def seed_disciplines():
    sql = "INSERT INTO disciplines(name, teacher_id) VALUES(?, ?);"
    cur.executemany(sql, zip(DISCIPLINES, iter(randint(1, NUMBER_TEACHERS) for _ in range(len(DISCIPLINES)))))


def seed_students():
    students = [fake.name() for _ in range(NUMBER_STUDENTS)]
    sql = "INSERT INTO students (name, group_id) VALUES(?, ?); "
    cur.executemany(sql, zip(students, iter(randint(1, len(GROUPS)) for _ in range(NUMBER_STUDENTS))))


def seed_groups():
    sql = "INSERT INTO st_groups(name) VALUES (?);"
    cur.executemany(sql, zip(GROUPS, ))


def seed_grades():
    sql = "INSERT INTO grades(discipline_id, student_id, grade, date_of) VALUES (?, ?, ?, ?);"
    def random_date(start, end):
        """
        This function will return a random datetime between two datetime
        objects.
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        new_date = start + timedelta(seconds=random_second)
        return new_date.date()
    res = []
    i = 0
    start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-06-15", "%Y-%m-%d")

    for student in range(1, NUMBER_STUDENTS+1):
        for item in range(1, len(DISCIPLINES)+1):
            grade = randint(1, 100)
            date_of = random_date(start_date, end_date)
            res.append((item, student, grade, date_of))
    cur.executemany(sql, res)




if __name__ == '__main__':
    try:
        seed_teachers()
        seed_disciplines()
        seed_students()
        seed_groups()
        seed_grades()

        connect.commit()
    except Error as error:
        print(error)
    finally:
        connect.close()
