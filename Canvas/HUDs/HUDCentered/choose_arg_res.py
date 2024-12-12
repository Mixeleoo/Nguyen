
from .base import HUDCenteredABC
from ..SubHUD import QuantitySelector
from parameter import *

class ChooseArgRes(HUDCenteredABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.quantity_selector_arg = QuantitySelector(
            self.canvas, self.tag, "💰 : ",
            min_quantity=0,
            max_quantity=0
        )
        self.quantity_selector_res = QuantitySelector(
            self.canvas, self.tag, "🍴 : ",
            min_quantity=0,
            max_quantity=0
        )

    @property
    def tag(self):
        return "ChooseArgRes"

    def create(self):

        width = 300
        height = 100

        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = y0_cadre + width
        y1_cadre = y0_cadre + height

        center_x = (x0_cadre + x1_cadre) // 2

        self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre, fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,), state="hidden"
        )

        custom_font = font.nametofont("TkDefaultFont").copy()
        custom_font.config(size=6)

        self.quantity_selector_arg.create(
            center_x - 40, y0_cadre + pad_from_borders
        )

        self.quantity_selector_res.create(
            center_x + 40, y0_cadre + pad_from_borders
        )

        # Bouton OK qui lance l'immigration
        self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.vassaliser, is_temp=True, state="hidden"
        )

        # Bouton Annuler qui annule l'immigration
        self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.bhide, is_temp=True, state="hidden"
        )

    def update(self, *args) -> None:
        self.quantity_selector_arg.update(max_quantity=self.canvas.jeu.joueur_actuel.argent)
        self.quantity_selector_res.update(max_quantity=self.canvas.jeu.joueur_actuel.ressources)

    def vassaliser(self, *args):

        noble_selected_index = self.canvas.hudmobile_choose_noble_vassaliser.noble_index_selected
        noble_selected = self.canvas.jeu.get_joueur(noble_selected_index)

        if self.canvas.jeu.joueur_actuel.soumettre(
                noble_selected, self.quantity_selector_arg.quantity, self.quantity_selector_res.quantity
        ):
            self.canvas.add_history_text("Vous avez vassalisé " + noble_selected.nom)

            # Ajouter le nouveau choix de noble à imposer
            self.canvas.hudmobile_choose_taxes.add_noble(noble_selected.nom, noble_selected_index)

            # Retirer le choix de noble à vassaliser et guerre
            self.canvas.hudmobile_choose_noble_vassaliser.remove_noble(noble_selected_index)
            self.canvas.hudcentered_choose_noble_war.remove_noble(noble_selected_index)

        self.bhide()

    def bhide(self, *args):
        self.quantity_selector_arg.reset()
        self.quantity_selector_res.reset()

        self.hide()
