import sqlite3

from textual import log
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Header, Footer, Label, RadioButton
from textual.containers import VerticalScroll, HorizontalGroup


class TodoTask(Widget):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label("Title", id="title")
            yield Label("Description", id="description")
            yield RadioButton(label="Done?", id="is_done")


class Todo(App):
    BINDINGS = [
        ("l", "list_tasks", "view tasks"),
        ("x", "close_app", "close app"),
        ("a", "create_task", "add task")
    ]
    conn = None

    def on_mount(self) -> None:
        try:
            self.conn = sqlite3.connect("todos.db")
        except sqlite3.OperationalError as e:
            pass

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
