
from ..HUDCenteredABC import HUDCenteredABC
from Canvas.HUDs.SubHUD import QuantitySelector
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

    def create(self):

        width = 500
        height = 100

        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = y0_cadre + width
        y1_cadre = y0_cadre + height

        center_x = (x0_cadre + x1_cadre) // 2
        center_y = (y0_cadre + y1_cadre) // 2

        self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre, fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,), state="hidden"
        )

        self.canvas.create_text(
            center_x, center_y - 20,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            fill=FILL_TEXT,
            text="Veuillez choisir la quantité d'argent et de ressources offertes au noble."
        )

        self.quantity_selector_arg.create(
            center_x - 40, center_y + 20
        )

        self.quantity_selector_res.create(
            center_x + 40, center_y + 20
        )

        # Bouton OK qui lance l'immigration
        self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.ok_trigger, is_temp=True, state="hidden"
        )

        # Bouton Annuler qui annule l'immigration
        self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.bhide, is_temp=True, state="hidden"
        )

    def update(self, *args) -> None:
        self.quantity_selector_arg.update(max_quantity=self.canvas.jeu.joueur_actuel.argent)
        self.quantity_selector_res.update(max_quantity=self.canvas.jeu.joueur_actuel.ressources)

    def ok_trigger(self, *args):
        self.canvas.vassaliser(self.quantity_selector_arg.quantity, self.quantity_selector_res.quantity)
        self.bhide()

    def bhide(self, *args):
        self.quantity_selector_arg.reset()
        self.quantity_selector_res.reset()

        self.hide()
