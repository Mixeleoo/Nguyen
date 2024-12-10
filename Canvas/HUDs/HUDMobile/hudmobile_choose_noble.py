
import tkinter as tk
from typing import Optional

from Canvas.Widget.Button import Button
from Canvas.HUDs.HUDMobileABC import HUDMobileABC
from Canvas.HUDs.SubHUD.SelectorInPage.HUDRadionbuttonInPage.subhud_choose_noble import SubHUDChooseNoble


class HUDMobileChooseNoble(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.choose_noble = SubHUDChooseNoble(canvas, self.tag)
        self.noble_index_selected = 0

        self.ok_button: Optional[Button] = None
        self.cancel_button: Optional[Button] = None

    @property
    def tag(self):
        return "CHOOSE_NOBLE"

    def create(self, *args):

        x0_cadre, y0_cadre, x1_cadre, y1_cadre = self.choose_noble.create(0, 0)

        # Bouton OK qui lance l'immigration
        self.ok_button = self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.ok_trigger, is_temp=True, state="hidden"
        )

        # Bouton Annuler qui annule l'immigration
        self.cancel_button = self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.bhide, is_temp=True, state="hidden"
        )

    def replace(self, *args) -> None:

        bbox = self.canvas.bbox(self.tag)

        dx = self.canvas.master.winfo_width() // 2 - (bbox[2] + bbox[0]) // 2
        dy = self.canvas.master.winfo_height() // 2 - (bbox[3] + bbox[1]) // 2

        self.canvas.move(self.tag, dx, dy)

    def ok_trigger(self, event: tk.Event) -> None:
        """
        Méthode qui met à jour le dernier choix de l'utilisateur dans l'attribut self.last_choice_made
        """

        if self.choose_noble.selected_option:
            self.noble_index_selected = self.choose_noble.selected_option

            self.bhide()
            self.canvas.hudmobile_choose_arg_res.show()

        else:
            print("T'as pas choisi de nobles là bro")

    def bhide(self, *args):
        self.choose_noble.setup_before_display()
        self.hide()
