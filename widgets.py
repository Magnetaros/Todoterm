import datetime

from core import Todo

from textual import events
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Label, Input
from textual.containers import HorizontalGroup, VerticalGroup


class TodoTask(HorizontalGroup):
    task: reactive[Todo | None] = reactive(Todo(-1, "", None, ""))

    def __init__(self, task: Todo):
        super().__init__()
        self.task = task
        pass

    def on_focus(self) -> None:
        self.notify("on focus")
        pass

    def on_selected(self) -> None:
        self.notify("on selected")
        pass

    def compose(self) -> ComposeResult:
        match self.task.status:
            case "active":
                self.styles.border = ("heavy", "yellow")
            case "pending":
                self.styles.border = ("heavy", "#9a8c98")
            case "complite":
                self.styles.border = ("heavy", "#a1c181")

        self.border_title = self.task.title
        self.border_subtitle = self.task.status
        self.notify(f"on_compose_task {self.task.id}")

        daysFromCreation = datetime.datetime.now() - self.task.created_at

        with VerticalGroup():
            with HorizontalGroup():
                yield Label(
                    f"Created {daysFromCreation} day(s) ago" if daysFromCreation.days != 0 else "Today",
                    id="Date",
                    classes="date-text"
                )
            if self.task.description is not None:
                yield Label(
                    self.task.description,
                    id="description",
                    classes="standtart-text"
                )


class TodoTitle(VerticalGroup):

    def compose(self) -> ComposeResult:
        yield Label("Planned", classes="standart-text")
        yield Label(
            datetime.datetime.now().strftime('%A %d, %Y'),
            classes="standart-text"
        )


# FIXME: show it as popup, current -> replaces full screen
class TodoChange(ModalScreen):

    BINDINGS = [
        ("escape", "app.pop_screen", "Exit window")
    ]

    def on_mount(self) -> None:
        self.query_one('#dialog').border_title = "Task"

    def on_key(self, event: events.Key) -> None:
        self.notify(f"key pressed {event.key}", timeout=0.3)
        self.notify(f"Current focus {self.selections}", timeout=0.3)
        if event.key == "enter" and self.query_one('#title') == self.focused:
            self.notify("Adding task")
            self.app.pop_screen()
        pass

    def compose(self) -> ComposeResult:
        with VerticalGroup(id="dialog", classes="todo-popup"):
            yield Input(id="title", placeholder="Title", type="text")
            yield Input(placeholder="Description", type="text")
