
from .base import HUDInformativeABC
from parameter import *


class CityFull(HUDInformativeABC):
    def __init__(self, canvas):
        super().__init__(canvas)

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

        self.canvas.create_text(
            (x0_cadre + x1_cadre) // 2,
            (y0_cadre + y1_cadre) // 2,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            fill=FILL_TEXT,
            text="Plus de place dans le village choisi",
            state="hidden"
        )

        # Bouton OK qui lance l'immigration
        self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.hide, is_temp=True, state="hidden"
        )

    def show(self) -> None:
