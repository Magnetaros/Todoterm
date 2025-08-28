import sqlite3

from textual import log
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import VerticalScroll

from widgets import TodoTask


class Todo(App):
    CSS_PATH = "main.tcss"

    BINDINGS = [
        ("l", "list_tasks", "view tasks"),
        ("x", "close_app", "close app"),
        ("a", "create_task", "add task")
    ]
    conn = None

    # TODO: first check for existing projects, if non create new
    # else show list of existing projects last 10 as centered list
    def on_mount(self) -> None:
        self.init_db()

    def on_unmount(self) -> None:
        log("Todo on_unmount!")
        if self.conn is not None:
            self.conn.close()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with VerticalScroll():
            yield TodoTask()

    def action_create_task(self) -> None:
        log("creating task")
        pass

    def action_list_tasks(self) -> None:
        log("Loading list of tasks!")
        pass

    def action_close_app(self) -> None:
        log("Closing app!")
        self.exit()

    def init_db(self):
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
        except sqlite3.OperationalError as e:
            log(f"Failed to open database:{e}")
