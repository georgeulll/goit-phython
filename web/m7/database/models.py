from sqlalchemy import Column, Integer, String, Boolean, func, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()


# class Teacher(Base):
#     __tablename__ = "teachers"
#     id = Column(Integer, primary_key=True)
#     first_name = Column(String(150), nullable=False)
#     last_name = Column(String(150), nullable=False)
#     email = Column(String(150), nullable=False)
#     phone = Column('cell_phone', String(150), nullable=False)
#     address = Column(String(150), nullable=True)
#     start_work = Column(Date,nullable=True)
#     created_at = Column(DateTime, default=func.now())
#
#     students = relationship("Student", secondary='teachers_to_students',
#                             back_populates="teachers",
#                             passive_deletes=True) #з*язки

class Discipline(Base):
    __tablename__ = "disciplines"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers.id', ondelete='CASCADE'))

    students = relationship("Student", secondary='grades',
                            back_populates="disciplines",
                            passive_deletes=True) #з*язки
    teachers = relationship("Teacher", back_populates='disciplines')


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    group_id = Column('group_id', ForeignKey('st_group.id', ondelete='CASCADE'))

    disciplines = relationship("Discipline", secondary='grades', back_populates="students", passive_deletes=True)
    st_group = relationship("StudentGroup", back_populates="students")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    discipline_id = Column('discipline_id', ForeignKey('disciplines.id', ondelete='CASCADE'))
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    grade = Column(Integer)
    date_of = Column(Date)


class StudentGroup(Base):
    __tablename__ = "st_group"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    students = relationship("Student", back_populates="st_group")


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)

    disciplines = relationship("Discipline", back_populates="teachers")