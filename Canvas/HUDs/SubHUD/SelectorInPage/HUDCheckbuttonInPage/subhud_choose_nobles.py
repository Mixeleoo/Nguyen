
from Canvas.HUDs.SubHUD.SelectorInPage.CheckbuttonInPageABC import CheckbuttonInPageABC


class SubHUDChooseNobles(CheckbuttonInPageABC):
    def __init__(self, canvas, hud_tag: str):
        super().__init__(canvas, hud_tag)

    @property
    def title(self):
        return "Quel(s) noble(s) imposer ?"
