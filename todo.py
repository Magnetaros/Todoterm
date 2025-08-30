from datetime import datetime, timedelta

from textual.app import App, ComposeResult
from textual.widgets import Footer, ListView, ListItem
from textual.reactive import reactive
from textual.containers import VerticalGroup

from core import TodoDb, Todo
from widgets import TodoTask, TodoTitle, TodoChange


# TODO: no projects, just present day with unfinished tasks
# + what you done today
# TODO: start implementing logic
class TodoTermApp(App):
    CSS_PATH = "main.tcss"

    BINDINGS = [
        ("a", "create_task", "add task"),
    ]

    db = None

    tasks: reactive[list[Todo]] = reactive([
        Todo(1, "Title One", None, "active"),
        Todo(2, "Title Two", None, "active"),
        Todo(3, "Title Three", "Some test text", "active"),
        Todo(4, "Title One", None, "pending"),
        Todo(5, "Title Two", None, "pending"),
        Todo(6, "Title Three", "Some test text", "pending"),
        Todo(7, "Title One", None, "complite",
             created_at=datetime.now() - timedelta(days=4)),
        Todo(8, "Title Two", None, "complite"),
        Todo(9, "Title Three", "Some test text", "complite")
    ], recompose=True)

    def on_mount(self) -> None:
        self.db = TodoDb()

        failed = self.db.init_db()
        if failed is not None:
            self.notify(failed, "Database error", severity="error")

    def __del__(self):
        print("todo destructor")
        self.db.close_db()

    def compose(self) -> ComposeResult:
        self.notify(f"todo app compose, tasks count {len(self.tasks)}")
        yield Footer()
        with VerticalGroup():
            yield TodoTitle(classes="todo-title")
            with ListView(id="active", classes="task-list"):
                for item in self.tasks:
                    yield ListItem(TodoTask(item), classes="task-container")

    def action_create_task(self) -> None:
        def task_check(task: Todo | None):
            if task is not None:
                self.tasks.append(task)
                self.notify(f"Task Created, task count = {len(self.tasks)}")
                self.mutate_reactive(TodoTermApp.tasks)

        self.notify("creating task", title="Action", timeout=0.7)
        self.push_screen(TodoChange(classes="todo-popup"), task_check)
