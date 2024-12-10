
from ..RadiobuttonInPageABC import RadiobuttonInPageABC

class SubHUDChooseVillage(RadiobuttonInPageABC):
    def __init__(self, canvas, hud_tag: str):
        super().__init__(canvas, hud_tag)

    @property
    def title(self):
        return "Quel villages voulez-vous immigrer ?"
