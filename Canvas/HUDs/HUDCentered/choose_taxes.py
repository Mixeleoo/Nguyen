
from typing import Optional

from .base import HUDCenteredABC
from Canvas.Widget.Button import Button
from Canvas.HUDs.SubHUD import ChooseVillages, ChooseNobles


class ChooseTaxes(HUDCenteredABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.choose_villages = ChooseVillages(canvas, self.tag)
        self.choose_nobles = ChooseNobles(canvas, self.tag)

        self.add_village = self.choose_villages.add_option
        self.remove_noble = self.choose_villages.remove_option

        self.add_noble = self.choose_nobles.add_option
        self.remove_noble = self.choose_nobles.remove_option

        self.ok_button: Optional[Button] = None
        self.cancel_button: Optional[Button] = None

    @property
    def tag(self):
        return "HUD_CHOOSE_TAXES"

    def create(self):

        x0_cadre, y0_cadre, x1_cadre, y1_cadre = self.choose_nobles.create(0, 0)

        # Bouton Annuler qui annule l'immigration
        self.cancel_button = self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.bhide, is_temp=True, state="hidden"
        )

        x0_cadre, y0_cadre, x1_cadre, y1_cadre = self.choose_villages.create(x1_cadre, 0)

        # Bouton OK qui lance l'immigration
        self.ok_button = self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.ok_trigger, is_temp=True, state="hidden"
        )

    def update(self):
        pass

    def ok_trigger(self, *args):

        if not self.choose_nobles.selected_option and not self.choose_villages.selected_option:
            bbox = self.canvas.bbox(self.tag)
            self.canvas.hudemobile_ilfautfaireunchoixgros.show(bbox[2] + 60, (bbox[3] + bbox[1]) // 2)
            self.shake()

        else:
            self.canvas.imposer(self.choose_villages.selected_option, self.choose_nobles.selected_option)
            self.bhide()

    def bhide(self, *args):
        self.choose_villages.update()
        self.choose_nobles.update()
        self.hide()