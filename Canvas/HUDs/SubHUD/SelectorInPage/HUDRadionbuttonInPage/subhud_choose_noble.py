
from Canvas.HUDs.SubHUD.SelectorInPage.RadiobuttonInPageABC import RadiobuttonInPageABC

class SubHUDChooseNoble(RadiobuttonInPageABC):
    def __init__(self, canvas, hud_tag: str):
        super().__init__(canvas, hud_tag)

    @property
    def title(self):
        return "Quel noble voulez-vous vassaliser ?"
