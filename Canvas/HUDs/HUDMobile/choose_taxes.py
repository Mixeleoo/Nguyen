
from typing import Optional

from .base import HUDMobileABC
from Canvas.Widget.Button import Button
from ..SubHUD import ChooseVillages, ChooseNobles


class ChooseTaxes(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.hudmobile_choose_villages = ChooseVillages(canvas, self.tag)
        self.hudmobile_choose_nobles = ChooseNobles(canvas, self.tag)

        self.add_village = self.hudmobile_choose_villages.add_option
        self.remove_noble = self.hudmobile_choose_villages.remove_option

        self.add_noble = self.hudmobile_choose_nobles.add_option
        self.remove_noble = self.hudmobile_choose_nobles.remove_option

        self.ok_button: Optional[Button] = None
        self.cancel_button: Optional[Button] = None

    @property
    def tag(self):
        return "HUD_CHOOSE_TAXES"

    def create(self):

        x0_cadre, y0_cadre, x1_cadre, y1_cadre = self.hudmobile_choose_nobles.create(0, 0)

        # Bouton Annuler qui annule l'immigration
        self.cancel_button = self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.bhide, is_temp=True, state="hidden"
        )

        x0_cadre, y0_cadre, x1_cadre, y1_cadre = self.hudmobile_choose_villages.create(x1_cadre, 0)

        # Bouton OK qui lance l'immigration
        self.ok_button = self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.imposer, is_temp=True, state="hidden"
        )

    def replace(self, *args) -> None:

        bbox = self.canvas.bbox(self.tag)

        dx = self.canvas.master.winfo_width() // 2 - (bbox[2] + bbox[0]) // 2
        dy = self.canvas.master.winfo_height() // 2 - (bbox[3] + bbox[1]) // 2

        self.canvas.move(self.tag, dx, dy)

    def imposer(self, *args):
        # self.canvas.jeu.imposer(self.hudmobile_choose_villages.selected_option)
        print(self.hudmobile_choose_nobles.selected_option)
        print(self.hudmobile_choose_villages.selected_option)

    def bhide(self, *args):
        self.hudmobile_choose_villages.setup_before_display()
        self.hudmobile_choose_nobles.setup_before_display()
        self.hide()