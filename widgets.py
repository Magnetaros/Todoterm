import datetime

from textual.app import ComposeResult
from textual.widgets import Label, Rule, ListItem
from textual.containers import HorizontalGroup, VerticalGroup


class TodoTask(HorizontalGroup):
    # FIXME: this is not changing when focused in a footer widget.
    # This must replace existing bindings
    BINDINGS = [
        ("c", "complite", "complite task"),
    ]

    def on_focus(self) -> None:
        self.notify("on focus")
        self.app.BINDINGS = self.BINDINGS
        pass

    def on_selected(self) -> None:
        self.notify("on selected")
        pass

    # TODO: make it one line or find example how it will look like
    def compose(self) -> ComposeResult:
        with VerticalGroup():
            with HorizontalGroup():
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
                "Thats a long and multilined \nstring",
                id="description",
                classes="standtart-text"
            )

        def action_complite(self) -> None:
            pass


class TodoTitle(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Planned")
        yield Label(
            datetime.datetime.now().strftime('%A %d, %Y'),
            classes="standart-text"
        )
