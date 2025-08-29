import sqlite3


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
