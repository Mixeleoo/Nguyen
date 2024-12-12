
import tkinter as tk
from typing import Optional

from .base import HUDCenteredABC
from Canvas.Widget.Button import Button
import Canvas.HUDs.SubHUD as SubHUD

class ChooseNobleWar(HUDCenteredABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.choose_noble = SubHUD.ChooseNoble(canvas, self.tag, "Contre quel noble voulez-vous entrer en guerre ?")
        self.add_noble = self.choose_noble.add_option
        self.remove_noble = self.choose_noble.remove_option

        self.ok_button: Optional[Button] = None
        self.cancel_button: Optional[Button] = None

    @property
    def tag(self):
        return "CHOOSE_NOBLE_WAR"

    def create(self):

        x0_cadre, y0_cadre, x1_cadre, y1_cadre = self.choose_noble.create(0, 0)

        # Bouton OK qui lance l'immigration
        self.ok_button = self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.ok_trigger, is_temp=True, state="hidden"
        )

        # Bouton Annuler qui annule l'immigration
        self.cancel_button = self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.bhide, is_temp=True, state="hidden"
        )

    def update(self):
        self.choose_noble.update()

    def ok_trigger(self, event: tk.Event) -> None:
        """
        Méthode qui met à jour le dernier choix de l'utilisateur dans l'attribut self.last_choice_made
        """
        noble_index = self.choose_noble.selected_option
        if noble_index:
            self.canvas.war(noble_index)
            self.bhide()

        else:
            bbox = self.canvas.bbox(self.tag)
            self.canvas.hudemobile_ilfautfaireunchoixgros.show(bbox[2] + 60, (bbox[3] + bbox[1]) // 2)
            self.shake()

    def bhide(self, *args):
        self.choose_noble.update()
        self.hide()
