
from ..HUDCenteredABC import HUDCenteredABC
from Canvas.Widget.StringVar import StringVar
from parameter import *


class ResultsWar(HUDCenteredABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self._text = StringVar(self.canvas)

    def create(self):

        width = 380
        height = 60

        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = y0_cadre + width
        y1_cadre = y0_cadre + height

        self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre, fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,), state="hidden"
        )

        self._text.id = self.canvas.create_text(
            (x0_cadre + x1_cadre) // 2,
            (y0_cadre + y1_cadre) // 2,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            fill=FILL_TEXT
        )

        # Bouton OK qui lance l'immigration
        self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.hide, is_temp=True, state="hidden"
        )

    def update(self, results: str) -> None:
        self._text.set("Les résultats de la guerre sont : " + results + "perte(s).")

    def replace(self, results: str) -> None: HUDCenteredABC.replace(self, results)
    def show(self, results: str) -> None: HUDCenteredABC.show(self, results)
