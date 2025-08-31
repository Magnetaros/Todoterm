import sqlite3
import datetime

TASK_TITLE_LENGTH_LIMIT = 20


class Todo():

    def __init__(self,
                 id: int,
                 title: str,
                 description: None | str,
                 status: str,
                 created_at: None | datetime.datetime = None,
                 complited_date: None | datetime.datetime = None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at if created_at is not None else datetime.datetime.now()
        self.complited = complited_date


class TodoDb():

    def __init__(self):
        print("Db created!")

    def __del__(self):
        print("Db cloased")

    def create_task(self, title: str, description: None | str) -> object | sqlite3.OperationalError:
        try:
            with sqlite3.connect("todos.db") as conn:
                date = datetime.datetime.now()
                cursor = conn.cursor()
                cursor.execute(f'''
INSERT INTO todos(title, description, status_id, created_at)
VALUES ('{title}', "{description}", 1, '{date}');
    ''')
                conn.commit()
                return Todo(cursor.lastrowid, title, description, "active", date)
        except sqlite3.OperationalError as err:
            return err

    def fetch_tasks(self) -> object | Exception:
        try:
            with sqlite3.connect("todos.db") as conn:
                cursor = conn.cursor()
                cursor.execute('''
SELECT todos.id AS id, title, description, todo_status.status AS status, created_at FROM todos
INNER JOIN todo_status ON todo_status.id = todos.status_id
                ''')
                data = cursor.fetchall()
                res: list[Todo] = []
                for item in data:
                    id, title, description, status, created_at = item
                    res.append(Todo(
                        int(id),
                        title,
                        description,
                        status,
                        datetime.datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S.%f')))
                return res
        except Exception as err:
            return err

    def close_db(self):
        self.conn.close()

    def init_db(self) -> None | sqlite3.OperationalError:
        try:
            with sqlite3.connect("todos.db") as conn:
                cursor = conn.cursor()
                cursor.executescript(f'''
CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    title VARCHAR({TASK_TITLE_LENGTH_LIMIT}) NOT NULL,
    description VARCHAR(2048) NULL,
    status_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(status_id)
    REFERENCES todo_status(id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS todo_status(
    id INTEGER PRIMARY KEY,
    status VARCHAR(255) NOT NULL
);
INSERT OR REPLACE INTO todo_status(id, status)
VALUES
(1, 'active'),
(2, 'pending'),
(3, 'complite');
                ''')
                cursor.fetchall()
                cursor.close()
                return None
        except sqlite3.OperationalError as e:
            return e
