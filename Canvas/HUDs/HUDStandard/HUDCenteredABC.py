
from abc import ABC, abstractmethod

from Canvas.HUDs.HUDStandard import HUDStandardABC
from Canvas.self_made_canvas import SelfMadeCanvas
from parameter import *

class HUDCenteredABC(HUDStandardABC, ABC):
    def __init__(self, canvas: SelfMadeCanvas):
        super().__init__(canvas)

        self.shake_it = 0

    @abstractmethod
    def update(self, *args):
        """
        Méthode lancée avant le replace.
        """
        pass

    def replace(self, *args) -> None:

        super().replace(*args)
        self.update(*args)

        bbox = self.bbox()
        if bbox is not None:
            dx = self.canvas.master.winfo_width() // 2 - (bbox[2] + bbox[0]) // 2
            dy = self.canvas.master.winfo_height() // 2 - (bbox[3] + bbox[1]) // 2

            self.canvas.move(self.tag, dx, dy)

    def shake(self):
        self.canvas.move(self.tag, randint(-3, 3), randint(-3, 3))

        if self.shake_it < 30:
            self.shake_it += 1
            self.canvas.after(DELTA_MS_ANIMATION, self.shake)

        else:
            self.shake_it = 0
