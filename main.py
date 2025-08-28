import sqlite3
import widgets


def init_db():
    try:
        sqlite3.connect("tasks.db")
    except sqlite3.OperationalError as e:
        print(f"Failed to open database:{e}")


if __name__ == "__main__":
    # init db, load ui, + - add task, when task focused - set status: active, inactive, done, remove
    # tasks saved in db sqlite
    init_db()
    app = widgets.Todo()
    app.run()
