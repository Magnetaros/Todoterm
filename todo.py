from datetime import datetime, timedelta

from textual.app import App, ComposeResult
from textual.widgets import Footer, ListView, ListItem, Static
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

    tasks: reactive[list[Todo]] = reactive([], recompose=True)

    def on_mount(self) -> None:
        db = TodoDb()
        failed = db.init_db()
        if failed is not None:
            self.notify(str(failed), title="Database error",
                        severity="error")
        else:
            res = db.fetch_tasks()
            if res is Exception:
                self.notify(str(res), "DB Error", severity="error")
            else:
                for item in res:
                    self.tasks.append(item)
                self.notify(str(len(self.tasks)), title="Task count")
                self.mutate_reactive(TodoTermApp.tasks)
        del db

    def __del__(self):
        print("todotermapp destructor")

    def compose(self) -> ComposeResult:
        self.notify(f"todo app compose, tasks count {len(self.tasks)}")
        yield Footer()
        with VerticalGroup():
            yield TodoTitle(classes="todo-title")
            if len(self.tasks) > 0:
                with ListView(id="active", classes="task-list"):
                    for item in self.tasks:
                        yield ListItem(TodoTask(item), classes="task-container")
            else:
                yield Static("No task found!", classes="no-todo-text")

    def action_create_task(self) -> None:
        def task_check(task: Todo | None):
            if task is not None:
                self.tasks.append(task)
                self.notify(f"Task Created, task count = {len(self.tasks)}")
                self.mutate_reactive(TodoTermApp.tasks)

        self.notify("creating task", title="Action", timeout=0.7)
        self.push_screen(TodoChange(classes="todo-popup"), task_check)
