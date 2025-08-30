from textual.app import App, ComposeResult
from textual.widgets import Footer, ListView, ListItem
from textual.containers import VerticalGroup

from core import TodoDb, Todo
from widgets import TodoTask, TodoTitle, TodoChange


# TODO: no projects, just present day with unfinished tasks
# + what you done today
class Todo(App):
    CSS_PATH = "main.tcss"

    BINDINGS = [
        ("a", "create_task", "add task"),
    ]
    db = None

    tasksAcitve = [
        Todo(1, "Title One", None, "active"),
        Todo(2, "Title Two", None, "active"),
        Todo(3, "Title Three", "Some test text", "active")
    ]

    tasksPending = [
        Todo(4, "Title One", None, "pending"),
        Todo(5, "Title Two", None, "pending"),
        Todo(6, "Title Three", "Some test text", "pending")
    ]

    tasksDone = [
        Todo(7, "Title One", None, "complite"),
        Todo(8, "Title Two", None, "complite"),
        Todo(9, "Title Three", "Some test text", "complite")
    ]

    def on_mount(self) -> None:
        self.db = TodoDb()

        failed = self.db.init_db()
        if failed is not None:
            self.notify(failed, "Database error", severity="error")

    def __del__(self):
        print("todo destructor")
        self.db.close_db()

    def compose(self) -> ComposeResult:
        yield Footer()
        with VerticalGroup():
            yield TodoTitle(classes="todo-title")
            with ListView(id="active", classes="task-list"):
                yield ListItem(TodoTask(self.tasksAcitve[0]), classes="task-container")
                yield ListItem(TodoTask(self.tasksAcitve[1]), classes="task-container")
                yield ListItem(TodoTask(self.tasksAcitve[2]), classes="task-container")
                yield ListItem(TodoTask(self.tasksPending[0]), classes="task-container")
                yield ListItem(TodoTask(self.tasksPending[1]), classes="task-container")
                yield ListItem(TodoTask(self.tasksPending[2]), classes="task-container")
                yield ListItem(TodoTask(self.tasksDone[0]), classes="task-container")
                yield ListItem(TodoTask(self.tasksDone[1]), classes="task-container")
                yield ListItem(TodoTask(self.tasksDone[2]), classes="task-container")

    def action_create_task(self) -> None:
        self.notify("creating task", title="Action", timeout=0.7)
        self.push_screen(TodoChange(classes="todo-popup"))
