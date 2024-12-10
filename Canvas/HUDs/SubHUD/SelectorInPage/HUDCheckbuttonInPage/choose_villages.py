
from ..CheckbuttonInPageABC import CheckbuttonInPageABC


class ChooseVillages(CheckbuttonInPageABC):
    def __init__(self, canvas, hud_tag: str):
        super().__init__(canvas, hud_tag)

    @property
    def title(self):
        return "Quel(s) village(s) imposer ?"
