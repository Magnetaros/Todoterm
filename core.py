import sqlite3
import datetime


class Todo():

    def __init__(self,
                 id: int,
                 title: str,
                 description: None | str,
                 status: str,
                 created_at: None | datetime.datetime = None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at if created_at is not None else datetime.datetime.now()


class TodoDb():
    conn = None

    def __init__(self):
        print("Db created!")

    def close_db(self):
        self.conn.close()

    def init_db(self) -> None | sqlite3.OperationalError:
        try:
            self.conn = sqlite3.connect("todos.db")
            cursor = self.conn.cursor()
            cursor.executescript('''
                CREATE TABLE IF NOT EXISTS todos(
                    id INTEGER PRIMARY KEY,
                    project_id INTEGER,
                    title VARCHAR(255) NOT NULL,
                    description VARCHAR(2048) NULL,
                    status INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS projects(
                    id INTEGER PRIMARY KEY,
                    title VARCHAR(255) NOT NULL
                );
            ''')
            cursor.fetchall()
            cursor.close()
            return None
        except sqlite3.OperationalError as e:
            return e
