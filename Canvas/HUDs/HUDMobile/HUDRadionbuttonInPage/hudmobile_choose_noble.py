
import tkinter as tk

from Canvas.HUDs.HUDMobile.HUDRadionbuttonInPage.HUDRadiobuttonInPageABC import HUDRadiobuttonInPageABC

class HUDChooseNoble(HUDRadiobuttonInPageABC):
    def __init__(self, canvas):
        super().__init__(canvas)

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
            noble_selected = self.canvas.jeu.get_joueur(self.selected_option)
            if self.canvas.jeu.joueur_actuel.soumettre(noble_selected):
                self.canvas.hudmobile_choose_taxes.add_noble(noble_selected.nom, self.selected_option)
                self.canvas.hud_history.add_text(f"Vous avez vassalisé {noble_selected.nom} !")

            else:
                self.canvas.hud_history.add_text(f"Vous n'avez pas vassalisé {noble_selected.nom}...")

            # Même comportement que si on annulait, mais précédé par la validation
            self.bhide()

        else:
            print("T'as pas choisi de nobles là bro")
