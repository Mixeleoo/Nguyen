
from Canvas.HUDs.HUDMobile.HUDCheckbuttonInPage.CheckbuttonInPageABC import CheckbuttonInPageABC


class HUDMobileChooseNoblesForTaxes(CheckbuttonInPageABC):
    def __init__(self, canvas):
        super().__init__(canvas)

    @property
    def tag(self):
        return "HUD_CHOOSE_NOBLES"

    def replace(self, *args) -> tuple[int, int]:
        bbox = self.canvas.bbox(self.tag)

        dx = self.canvas.master.winfo_width() // 2 - (bbox[2] - bbox[0]) // 2 - (bbox[2] + bbox[0]) // 2
        dy = self.canvas.master.winfo_height() // 2 - (bbox[3] + bbox[1]) // 2

        self.canvas.move(self.tag, dx, dy)

        return dx, dy
