
from abc import ABC

from Canvas.self_made_canvas import SelfMadeCanvas
from Canvas.HUDs.HUDStandard.base import HUDStandardABC

class HUDTemporaryABC(HUDStandardABC, ABC):
    def __init__(self, canvas: SelfMadeCanvas):
        super().__init__(canvas)

        self.after_hide_id = None

    def replace(self, *args) -> None:

        super().replace(*args)

        self.canvas.tag_raise(self.tag)

        # On cache après trois seconde
        if self.after_hide_id is not None:
            self.canvas.after_cancel(self.after_hide_id)

        self.after_hide_id = self.canvas.after(3000, self.bhide)

    def bhide(self):
        self.after_hide_id = None
        self.hide()

