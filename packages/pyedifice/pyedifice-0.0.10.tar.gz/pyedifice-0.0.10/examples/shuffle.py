import edifice as ed
import random

class App(ed.Component):

    @ed.register_props
    def __init__(self):
        self.order = [1, 2, 3, 4]

    def on_click(self, e):
        with self.render_changes():
            random.shuffle(self.order)

    def render(self):
        return ed.View(layout="column")(
            [ed.Label(str(s)).set_key(str(s)) for s in self.order],
            ed.Button("Shuffle", on_click=self.on_click)
        )
