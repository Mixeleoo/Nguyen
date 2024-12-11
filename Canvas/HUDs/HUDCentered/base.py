
from abc import ABC, abstractmethod

from ..HUDMobile import HUDMobileABC
from Canvas.hud_canvas import HUDCanvas

class HUDCenteredABC(HUDMobileABC, ABC):
    def __init__(self, canvas: HUDCanvas):
        super().__init__(canvas)

    @abstractmethod
    def update(self):
        """
        Méthode lancée avant le replace.
        """
        pass

    def replace(self, *args) -> None:

        self.update()

        bbox = self.canvas.bbox(self.tag)

        dx = self.canvas.master.winfo_width() // 2 - (bbox[2] + bbox[0]) // 2
        dy = self.canvas.master.winfo_height() // 2 - (bbox[3] + bbox[1]) // 2

        self.canvas.move(self.tag, dx, dy)
