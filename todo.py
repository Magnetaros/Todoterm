import sqlite3

from textual.app import App, ComposeResult
from textual.widgets import Footer, ListView, ListItem
from textual.containers import Vertical

from core import TodoDb
from widgets import TodoTask, TodoTitle, TodoChange


class Todo(App):
    CSS_PATH = "main.tcss"

    BINDINGS = [
        ("a", "create_task", "add task")
    ]
    db = None

    # TODO: first check for existing projects, if non create new
    # else show list of existing projects last 10 as centered list
    def on_mount(self) -> None:
        self.notify("Todo on_mount!")
        self.db = TodoDb()

        failed = self.db.init_db()
        if failed is not None:
            self.notify(failed, "Database error", severity="error")

    def on_focus(self) -> None:
        self.app.BINDINGS = self.BINDINGS

    def on_unmount(self) -> None:
        print("on unmount")
        self.notify("Todo on_unmount!")
        self.db.close_db()

    def compose(self) -> ComposeResult:
        yield Footer()
        with Vertical():
            yield TodoTitle(classes="todo-title")
            # TODO: create another widget for this,
            # I can't seem to find a way passing data through constructors
            with ListView(classes="task-list"):
                yield ListItem(TodoTask(), classes="task-container")
                yield ListItem(TodoTask(), classes="task-container")
                yield ListItem(TodoTask(), classes="task-container")
                yield ListItem(TodoTask(), classes="task-container")
                yield ListItem(TodoTask(), classes="task-container")
                yield ListItem(TodoTask(), classes="task-container")

    def action_create_task(self) -> None:
        self.notify("creating task", title="Action", timeout=0.7)
        self.push_screen(TodoChange(classes="todo-popup"))
        pass
