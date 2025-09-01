from textual.app import App, ComposeResult
from textual.widgets import Footer, ListView, Static
from textual.events import Focus
from textual.reactive import reactive
from textual.containers import VerticalGroup

from core import TodoDb, Todo
from widgets import TodoTask, TodoTitle, TodoChange


# TODO: no projects, just present day with unfinished tasks
# + what you done today, maybe
class TodoTermApp(App):
    CSS_PATH = "main.tcss"

    BINDINGS = [
        ("c", "create_task", "add task"),
        ("ctrl+c", "complite_task", "complite task"),
        ("p", "switch_pending", "make pending"),
        ("d", "delete_task", "delete item"),
    ]

    tasks: reactive[list[Todo]] = reactive([], recompose=True)
    current: [TodoTask | None] = None
    tasks_stats: list[str] | None = []

    def on_mount(self) -> None:
        db = TodoDb()
        failed = db.init_db()
        if failed is Exception:
            self.notify(str(failed), title="Database error",
                        severity="error")
            pass

        self.tasks_stats = db.get_todo_status__variants()
        self.notify(str(self.tasks_stats))
        res = db.fetch_tasks()
        if res is Exception:
            self.notify(str(res), "DB Error", severity="error")
            pass

        for item in res:
            self.tasks.append(item)
        self.notify(str(len(self.tasks)), title="Task count")
        self.mutate_reactive(TodoTermApp.tasks)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self.notify(f"Selected {event.item.task.id}")

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        self.notify(f"Highlited {event.item.task.id}")
        self.current = event.item

    def compose(self) -> ComposeResult:
        self.notify(f"todo app compose, tasks count {len(self.tasks)}")
        yield Footer()
        with VerticalGroup():
            yield TodoTitle(classes="todo-title")
            if len(self.tasks) > 0:
                with ListView(id="active", classes="task-list") as list_view:
                    for item in self.tasks:
                        yield TodoTask(item)
                    list_view.focus()
            else:
                yield Static("No task found!", classes="no-todo-text")

    def action_create_task(self) -> None:
        def task_check(task: Todo | None):
            if task is None:
                pass

            self.tasks.append(task)
            self.notify(f"Task Created, task count = {len(self.tasks)}")
            self.mutate_reactive(TodoTermApp.tasks)

        self.notify("creating task", title="Action", timeout=0.7)
        self.push_screen(TodoChange(classes="todo-popup"), task_check)

    def action_delete_task(self) -> None:
        self.notify(f"trying to delete {self.current}:{self.current.task.id}")
        if self.current is None:
            pass

        res = TodoDb().delete_task(self.current.task)
        if res is Exception:
            self.notify(str(res), severity="error")
            pass

        self.notify(f"deleting {self.current.task.id}", severity="warning")
        self.tasks.remove(self.current.task)
        del self.current
        self.current = None
        self.mutate_reactive(TodoTermApp.tasks)

    def action_complite_task(self) -> None:
        if self.current is None:
            pass

        self.current.task.status = "complite"

        res = TodoDb().change_task(self.current.task)
        if res is Exception:
            self.notify(str(res), severity="error")
            pass

        self.mutate_reactive(TodoTermApp.tasks)

    # TODO:
    def action_switch_pending(self) -> None:
        if self.current is None:
            pass

        if self.current.task.status == "complite":
            pass

        self.current.task.status = "pending" if self.current.task.status == "active" else "active"
        res = TodoDb().change_task(self.current.task)
        if res is Exception:
            self.notify(str(res), severity="error")
            pass

        self.mutate_reactive(TodoTermApp.tasks)
