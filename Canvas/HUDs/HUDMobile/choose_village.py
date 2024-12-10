
import tkinter as tk
from typing import Optional

from .base import HUDMobileABC
from Canvas.Widget.Button import Button
from ..SubHUD import SubHUDChooseVillage
from parameter import *

class ChooseVillage(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.choose_village = SubHUDChooseVillage(canvas, self.tag)

        self.ok_button: Optional[Button] = None
        self.cancel_button: Optional[Button] = None

    @property
    def tag(self):
        return CHOOSE_VILLAGE_TAG

    def create(self, *args):

        x0_cadre, y0_cadre, x1_cadre, y1_cadre = self.choose_village.create(0, 0)

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

        if self.choose_village.selected_option:

            effectif = self.canvas.hudmobile_choose_type_villager.last_choice_made[0]
            type_v = self.canvas.hudmobile_choose_type_villager.last_choice_made[1]
            village_id = self.choose_village.selected_option

            # lancer l'immigration du jeu
            self.canvas.jeu.immigrer(
                effectif=effectif,
                type_v=type_v,
                village_id=village_id
            )

            self.canvas.add_history_text(f"Vous avez immigré {effectif} {type_v} dans le village {village_id} !")

            # Même comportement que si on annulait, mais précédé par la validation
            self.bhide()

        else:
            print("T'as pas choisi de village là bro")

    def bhide(self, *args):
        self.choose_village.setup_before_display()
        self.hide()
