
from abc import ABC

from Canvas.hud_canvas import HUDCanvas
from ...HUDMobile.base import HUDMobileABC

class HUDInformativeABC(HUDMobileABC, ABC):
    def __init__(self, canvas: HUDCanvas):
        super().__init__(canvas)

        self.id = 0
        self.after_hide_id = None

    def replace(self, x0: float, y0: float) -> None:

        dx = x0 - self.canvas.coords(self.id)[0]
        dy = y0 - self.canvas.coords(self.id)[1]

        self.canvas.move(self.tag, dx, dy)

        # On cache après trois seconde
        if self.after_hide_id is not None:
            self.canvas.after_cancel(self.after_hide_id)

        self.after_hide_id = self.canvas.after(3000, self.bhide)

    def show(self, x0: float, y0: float) -> None: super().show(x0, y0)

    def bhide(self):
        self.after_hide_id = None
        self.hide()

