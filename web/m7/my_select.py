from sqlalchemy import func, desc

from pprint import pprint

from database.db import session
from database.models import Student, StudentGroup, Discipline,  Teacher, Grade


def select_1():
    """    Найти 5 студентов с наибольшим средним баллом по всем предметам.
    SELECT ROUND(AVG(g.grade), 2) as Average_Grade, s.name
    FROM grades g
    LEFT JOIN students s ON g.student_id =s.id
    GROUP BY s.name
    ORDER BY Average_Grade DESC
    LIMIT 5"""

    res = session.query(Student.name, func.round(func.avg(Grade.grade), 2).label('Average_grade'))\
    .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('Average_grade')).limit(5).all()
    pprint(res)


def select_2():
    """Найти студента с наивысшим средним баллом по определенному предмету..
    SELECT g.discipline_id, d.name as discipline_name, AVG(g.grade) as Average_grade, s.name
    FROM grades g
    LEFT JOIN students s ON g.student_id = s.id
    LEFT JOIN disciplines d ON g.discipline_id =d.id
    WHERE g.discipline_id = 6
    GROUP BY s.name
    ORDER BY Average_grade DESC
    LIMIT 5"""

    res = session.query(Student.name, func.round(func.avg(Grade.grade), 2).label('Average_grade'), Discipline.name)\
        .select_from(Grade).join(Student)\
        .join(Discipline).filter(Discipline.id == 1)\
        .group_by(Discipline.name).group_by(Student.name)\
        .order_by(desc('Average_grade')).limit(2).all()
    pprint(res)


def select_3():
    """Найти средний балл в группах по определенному предмету.
    SELECT d.name as discipline_name, sg.name as Groups_Name, ROUND(AVG(g.grade),2) as Average_grade
    FROM grades g
    LEFT JOIN students s ON g.student_id = s.id
    LEFT JOIN disciplines d ON g.discipline_id =d.id
    LEFT JOIN st_groups sg ON s.group_id =sg.id
    WHERE d.id = 6
    GROUP BY sg.name
    ORDER BY sg.id
    """
    res = session.query(StudentGroup.name, Discipline.name, func.round(func.avg(Grade.grade), 2).label("AVG_grades"))\
          .select_from(Grade)\
          .join(Discipline).filter(Discipline.id == 1)\
          .join(Student)\
          .join(StudentGroup)\
          .group_by(StudentGroup.name).group_by(Discipline.name)\
          .order_by(desc('AVG_grades')).all()
    pprint(res)


def select_4():
    """Найти средний балл на потоке (по всей таблице оценок).
SELECT ROUND(AVG(g.grade),2) as Average_Grade
FROM grades g
    """
    res = session.query(func.round(func.avg(Grade.grade), 2))\
          .select_from(Grade).all()
    pprint(res)


def select_5():
    """Найти какие курсы читает определенный преподаватель.
SELECT t.id as Teacher_id , t.fullname , d.name as disciplines_name
FROM disciplines d
LEFT JOIN teachers t ON d.teacher_id =t.id
WHERE t.id = 1
GROUP BY d.id
ORDER BY t.id
    """
    res = session.query(Discipline.name, Teacher.fullname)\
          .select_from(Discipline)\
          .join(Teacher).filter(Teacher.id == 1)\
          .group_by(Discipline.name).group_by(Teacher.fullname)\
          .order_by(Discipline.name).all()
    pprint(res)


def select_6():
    """Найти список студентов в определенной группе
    """
    res = session.query(Student.name, StudentGroup.name)\
          .select_from(Student) \
          .join(StudentGroup).filter(StudentGroup.id == 1) \
          .group_by(Student.name).group_by(StudentGroup.name) \
          .order_by(Student.name).all()
    pprint(res)


def select_7():
    """Найти оценки студентов в отдельной группе по определенному предмету.
    """
    res = session.query(Student.name, Grade.grade, Discipline.name, StudentGroup.name) \
          .select_from(Grade) \
          .join(Student) \
          .join(StudentGroup).filter(StudentGroup.id == 2) \
          .join(Discipline).filter(Discipline.id == 2) \
          .group_by(Student.name).group_by(Discipline.name).group_by(Grade.grade, StudentGroup.name) \
          .order_by(desc(Grade.grade)).all()
    pprint(res)


def select_8():
    """Найти средний балл, который ставит определенный преподаватель по своим предметам."""
    res = session.query(Teacher.fullname, Discipline.name, func.round(func.avg(Grade.grade), 2).label('Avg_grade')) \
          .select_from(Grade) \
          .join(Discipline) \
          .join(Teacher).filter(Teacher.id == 5) \
          .group_by(Discipline.id, Teacher.fullname) \
          .order_by(desc('Avg_grade')).all()
    pprint(res)


def select_9():
    """Найти список курсов, которые посещает определенный студент."""
    res = session.query(Discipline.name, Student.name) \
          .select_from(Grade) \
          .join(Student).filter(Student.id == 1) \
          .join(Discipline) \
          .group_by(Student.id, Discipline.id) \
          .order_by(Discipline.name).all()
    pprint(res)


def select_10():
    """Список курсов, которые определенному студенту читает определенный преподаватель"""
    res = session.query(Discipline.name, Student.name, Teacher.fullname) \
          .select_from(Grade) \
          .join(Student).filter(Student.id == 1) \
          .join(Discipline) \
          .join(Teacher).filter(Teacher.id == 1) \
          .group_by(Discipline.id,Student.id,Teacher.id) \
          .order_by(Discipline.name).all()
    pprint(res)

if __name__ == "__main__":
    # select_1()
    # select_2()
    # select_3()
    # select_4()
    # select_5()
    # select_6()
    # select_7()
    # select_8()
    # select_9()
    select_10()