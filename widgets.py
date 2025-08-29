import datetime

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label, RadioButton
from textual.containers import Vertical, Horizontal, HorizontalGroup, VerticalGroup


class TodoTask(HorizontalGroup):
    # FIXME: this is not changing when focused in a footer widget
    BINDINGS = [
        ("c", "complite", "complite task"),
    ]

    def on_focus(self) -> None:
        self.app.BINDINGS = self.BINDINGS
        pass

    # TODO: make it one line or find example how it will look like
    def compose(self) -> ComposeResult:
        with VerticalGroup(classes="debug-bounds"):
            with HorizontalGroup(classes="debug-bounds"):
                yield Label(
                    "Title",
                    id="title",
                    classes="important-text"
                )
                yield Label(
                    " 28.08.25",
                    id="Date",
                    classes="date-text"
                )
            yield Label(
                '''
                Thats a long and multilined
                string
                ''',
                id="description",
                classes="standtart-text"
            )
        yield RadioButton(button_first=False, id="is_done")

        def action_complite(self) -> None:
            pass


class TodoTitle(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Planned")
        yield Label(
            str(datetime.datetime.now()),
            classes="date-text"
        )
