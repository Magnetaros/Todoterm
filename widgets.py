import datetime
from datetime import date

from core import Todo, TodoDb, TASK_TITLE_LENGTH_LIMIT

from textual import events
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Label, Input, TextArea, Static, ListItem
from textual.containers import HorizontalGroup, VerticalGroup
from textual.validation import Function


class TodoTask(ListItem):
    task: reactive[Todo | None] = reactive(
        None, always_update=True, recompose=True)

    def __init__(self, task: Todo, classes: str | None = None):
        super().__init__(classes=classes)
        self.task = task

    def watch_task(self, old_task: Todo, new_task: Todo) -> None:
        if new_task is None:
            return

        match new_task.status:
            case "active":
                self.styles.border = ("heavy", "yellow")
            case "pending":
                self.styles.border = ("heavy", "#9a8c98")
            case "complite":
                self.styles.border = ("heavy", "#a1c181")

        self.border_title = new_task.title
        self.border_subtitle = new_task.status

    def compose(self) -> ComposeResult:
        daysFromCreation = date.today() - self.task.created_at

        with HorizontalGroup():
            with VerticalGroup():
                with HorizontalGroup():
                    yield Label(
                        f"Created {daysFromCreation.days} day(s) ago" if daysFromCreation.days != 0 else "Today",
                        id="Date",
                        classes="date-text"
                    )
                if self.task.description is not None:
                    yield Static(
                        self.task.description,
                        expand=True,
                        shrink=True,
                        id="description",
                        classes="standart-text"
                    )


class TodoTitle(VerticalGroup):

    # test comment
    def compose(self) -> ComposeResult:
        yield Label("Planned", classes="standart-text")
        yield Label(
            datetime.datetime.now().strftime('(%A) %B %d, %Y'),
            classes="standart-text"
        )


# TODO: show it as popup with transparent background, current -> replaces full screen
class TodoChange(ModalScreen[Todo | None]):

    BINDINGS = [
        ("escape", "cancel", "Exit window")
    ]

    def on_mount(self) -> None:
        self.query_one('#dialog').border_title = "Todo"

    def on_key(self, event: events.Key) -> None:
        input = self.query_one('#title')
        if event.key == "enter" and input == self.focused and self.input_valid:
            self.notify("Adding task", timeout=1.2)
            description_input = self.query_one('#descr', TextArea)

            db = TodoDb()
            res = db.create_task(self.title_input, description_input.text)
            if res is Exception:
                self.notify(str(res), title="Db error", severity="error")
                return

            self.dismiss(res)

    def action_cancel(self) -> None:
        self.dismiss(None)

    def title_validation(self, value: str) -> bool:
        self.input_valid = len(value) > 0 and len(
            value) <= TASK_TITLE_LENGTH_LIMIT
        self.title_input = value
        return self.input_valid

    def compose(self) -> ComposeResult:
        with VerticalGroup(id="dialog", classes="todo-popup"):
            yield Input(id="title", placeholder="Title", type="text", validators=[
                Function(self.title_validation, "Title can't be empty")
            ])
            yield TextArea(id="descr")
