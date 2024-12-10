
from ..CheckbuttonInPageABC import CheckbuttonInPageABC


class SubHUDChooseVillages(CheckbuttonInPageABC):
    def __init__(self, canvas, hud_tag: str):
        super().__init__(canvas, hud_tag)

    @property
    def title(self):
        return "Quel(s) village(s) imposer ?"
