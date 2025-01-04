
from ..HUDCenteredABC import HUDCenteredABC
from Perso.noble import Noble
from Canvas.Widget.StringVar import StringVar
from parameter import *


class AcceptVassal(HUDCenteredABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self._text = StringVar(self.canvas)
        self.noble_proposal: Noble | None = None

    def create(self, *args):

        width = 380
        height = 60

        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = y0_cadre + width
        y1_cadre = y0_cadre + height

        self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre, fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,), state="hidden"
        )

        self._text.id = self.canvas.create_text(
            (x0_cadre + x1_cadre) // 2,
            (y0_cadre + y1_cadre) // 2,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            fill=FILL_TEXT
        )

        # Bouton OK qui lance l'immigration
        self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.ok_trigger, is_temp=True, state="hidden"
        )

        # Bouton Annuler qui annule l'immigration
        self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.hide, is_temp=True, state="hidden"
        )

    def update(self, noble: Noble) -> None:
        self._text.set(noble.nom + " veut devenir votre vassal, acceptez-vous ?")
        self.noble_proposal = noble

    def replace(self, noble: Noble) -> None: HUDCenteredABC.replace(self, noble)
    def show(self, noble: Noble) -> None: HUDCenteredABC.show(self, noble)

    def ok_trigger(self, *args):
        self.canvas.event_accept_vassal(self.noble_proposal)
        self.hide()
