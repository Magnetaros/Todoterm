from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label, RadioButton
from textual.containers import Container, Vertical, Horizontal


# FIXME: make container fit content
class TodoTask(Widget):

    # TODO: make it one line or find example how it will look like
    def compose(self) -> ComposeResult:
        # FIXME: this is not changing when focused in a footer widget
        BINDINGS = [
            ("c", "complite", "complite task"),
        ]

        with Horizontal(classes="task-container"):
            with Vertical():
                with Horizontal():
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


class TodoTitle(Widget):
    pass
