
from ..RadiobuttonInPageABC import RadiobuttonInPageABC

class ChooseNoble(RadiobuttonInPageABC):
    def __init__(self, canvas, hud_tag: str, title: str):
        super().__init__(canvas, hud_tag)

        self._title = title

    @property
    def title(self):
        return self._title
