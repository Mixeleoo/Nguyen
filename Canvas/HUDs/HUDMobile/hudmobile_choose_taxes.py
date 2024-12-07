
from typing import Optional

from Canvas.HUDs.Button import Button
from Canvas.HUDs.HUDMobile.HUDMobileABC import HUDMobileABC
from Canvas.HUDs.HUDMobile.HUDCheckbuttonInPage.HUDMobileChooseNoblesForTaxes import HUDMobileChooseNoblesForTaxes
from Canvas.HUDs.HUDMobile.HUDCheckbuttonInPage.HUDMobileChooseVillagesForTaxes import HUDMobileChooseVillagesForTaxes


class HUDMobileChooseTaxes(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.hudmobile_choose_villages = HUDMobileChooseVillagesForTaxes(canvas)
        self.hudmobile_choose_nobles = HUDMobileChooseNoblesForTaxes(canvas)

        self.add_village = self.hudmobile_choose_villages.add_option
        self.add_noble = self.hudmobile_choose_nobles.add_option

        self.ok_button: Optional[Button] = None
        self.cancel_button: Optional[Button] = None

    @property
    def tag(self):
        return "HUD_CHOOSE_TAXES"

    def replace(self, *args) -> None:
        self.hudmobile_choose_nobles.no_replace_show()
        self.hudmobile_choose_villages.no_replace_show()

        dx, dy = self.hudmobile_choose_nobles.replace(*args)
        self.cancel_button.move(dx, dy)

        dx, dy = self.hudmobile_choose_villages.replace(*args)
        self.ok_button.move(dx, dy)

    def create(self):

        x0_cadre, y0_cadre, x1_cadre, y1_cadre = self.hudmobile_choose_villages.create()

        # Bouton OK qui lance l'immigration
        self.ok_button = self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.imposer, is_temp=True, state="hidden"
        )

        x0_cadre, y0_cadre, x1_cadre, y1_cadre = self.hudmobile_choose_nobles.create()

        # Bouton Annuler qui annule l'immigration
        self.cancel_button = self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.bhide, is_temp=True, state="hidden"
        )

    def imposer(self, *args):
        print(self.hudmobile_choose_villages.selected_option)
        print(self.hudmobile_choose_nobles.selected_option)

    def bhide(self, *args):
        self.hudmobile_choose_villages.bhide()
        self.hudmobile_choose_nobles.bhide()
        self.hide()