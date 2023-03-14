import sqlite3
from contextlib import contextmanager
from psycopg2 import Error



@contextmanager
def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    database = r'C:\Users\nikolay.grishyn\Documents\PythonWEB\Module6\module6\education_db'
    try:
        conn = sqlite3.connect(database)
        yield conn
        conn.commit()
    except Error as error:
        print(error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
