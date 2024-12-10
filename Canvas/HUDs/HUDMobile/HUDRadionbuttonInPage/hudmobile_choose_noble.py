
import tkinter as tk

from Canvas.HUDs.HUDMobile.HUDRadionbuttonInPage.HUDRadiobuttonInPageABC import HUDRadiobuttonInPageABC

class HUDMobileChooseNoble(HUDRadiobuttonInPageABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.noble_index_selected = 0

    @property
    def tag(self):
        return "CHOOSE_NOBLE"

    @property
    def title(self):
        return "Quel noble voulez-vous vassaliser ?"

    def ok_trigger(self, event: tk.Event) -> None:
        """
        Méthode qui met à jour le dernier choix de l'utilisateur dans l'attribut self.last_choice_made
        """

        if self.selected_option:
            self.noble_index_selected = self.selected_option

            self.bhide()
            self.canvas.hudmobile_choose_arg_res.show()

        else:
            print("T'as pas choisi de nobles là bro")
