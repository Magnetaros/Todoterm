import sqlite3
import widgets


def init_db():
    try:
        conn = sqlite3.connect("todos.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS todos(
            id INTEGER PRIMARY KEY,
            project_id INTEGER,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(2048) NULL,
            status INTEGER NOT NULL
        );''')
        cursor.fetchall()
        cursor.close()
        conn.close()
    except sqlite3.OperationalError as e:
        print(f"Failed to open database:{e}")


if __name__ == "__main__":
    # init db, load ui, + - add task, when task focused - set status: active, inactive, done, remove
    # tasks saved in db sqlite
    init_db()
    app = widgets.Todo()
    app.run()
