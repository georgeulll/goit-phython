from sqlite3 import Error

from db_conection_to_educatio_db import create_connection


def execute_command(conn, command):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param command: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(command)
        c.close()
    except Error as e:
        print(e)


if __name__ == '__main__':

    sql_table_student_DROP = """DROP TABLE IF EXISTS students; """
    sql_table_student = """     
    CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(30),
    group_id VARCHAR(20),
    FOREIGN KEY (group_id) REFERENCES st_groups (id)
); """

    sql_table_groups_DROP = """DROP TABLE IF EXISTS st_groups; """
    sql_table_groups = """
    CREATE TABLE st_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(30)
    ); """

    sql_table_Teachers_DROP = """DROP TABLE IF EXISTS teachers;"""
    sql_table_Teachers = """    
    CREATE TABLE teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    fullname STRING
); """

    sql_table_disciplines_DROP = """DROP TABLE IF EXISTS disciplines;"""
    sql_table_disciplines = """    
    CREATE TABLE disciplines (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(30),
    teacher_id VARCHAR(20),
    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
); """

    sql_table_grades_DROP = '''DROP TABLE IF EXISTS grades;'''
    sql_table_grades = """    
    CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    discipline_id VARCHAR(20),
    student_id VARCHAR(20),
    grade INTEGER,
    date_of DATE,
    FOREIGN KEY (discipline_id) REFERENCES disciplines (id),
    FOREIGN KEY (student_id) REFERENCES students (id)
); """

    with create_connection() as conn:
        if conn is not None:
            execute_command(conn, sql_table_groups_DROP)
            execute_command(conn, sql_table_groups)

            execute_command(conn, sql_table_Teachers_DROP)
            execute_command(conn, sql_table_Teachers)

            execute_command(conn, sql_table_student_DROP)
            execute_command(conn, sql_table_student)

            execute_command(conn, sql_table_disciplines_DROP)
            execute_command(conn, sql_table_disciplines)

            execute_command(conn, sql_table_grades_DROP)
            execute_command(conn, sql_table_grades)

        else:
            print("Error! cannot create the database connection.")