
import tkinter as tk

from Canvas.HUDs.HUDMobile.HUDRadionbuttonInPage.HUDRadiobuttonInPageABC import HUDRadiobuttonInPageABC
from parameter import *

class HUDChooseVillage(HUDRadiobuttonInPageABC):
    def __init__(self, canvas):
        super().__init__(canvas)

    @property
    def tag(self):
        return CHOOSE_VILLAGE_TAG

    @property
    def title(self):
        return "Quel villages voulez-vous immigrer ?"

    def ok_trigger(self, event: tk.Event) -> None:
        """
        Méthode qui met à jour le dernier choix de l'utilisateur dans l'attribut self.last_choice_made
        """

        if self.selected_option:

            effectif = self.canvas.hudmobile_choose_type_villager.last_choice_made[0]
            type_v = self.canvas.hudmobile_choose_type_villager.last_choice_made[1]
            village_id = self.selected_option

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
