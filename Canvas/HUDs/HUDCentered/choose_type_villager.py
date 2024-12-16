
from typing import Optional

from .base import HUDCenteredABC
from Canvas.Widget.Radiobutton import Radiobutton
from Canvas.HUDs.SubHUD.quantityselector import QuantitySelector
from parameter import *

class ChooseTypeVillager(HUDCenteredABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.artisan_choice_id = 0
        self.paysan_choice_id = 0
        self.soldat_choice_id = 0

        self.quantity_selector_hum = QuantitySelector(
            self.canvas, self.tag, "Effectif souhaité : ",
            1, 10, self.callback_quantity_selector
        )

        # tableau qui contiendra le dernier effectif choisi puis le dernier type de villageois choisi
        self.last_choice_made = []

        self.radiobutton_choice: Optional[Radiobutton] = None

    def create(self):

        height = 150
        width = 400

        title_text = "Quelle sera la profession du villageois ?"

        # coordonnées du rectangle principal pour l'avoir au milieu de l'écran
        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = width
        y1_cadre = height

        center_x = (x0_cadre + x1_cadre) // 2

        # Rectangle qui englobe tout ça
        self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre,
            fill=FILL_ACTION_BOX,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden"
        )

        # Titre choix
        self.canvas.create_text(
            center_x, y0_cadre + pad_from_borders,
            text=title_text,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden",
            fill=FILL_TEXT
        )

        self.quantity_selector_hum.create(
            center_x - 20, y0_cadre + pad_from_borders + 25,
        )

        # Paysan choix
        self.paysan_choice_id = self.canvas.create_text_in_rectangle(
            x0_cadre + pad_from_borders,
            y0_cadre + pad_from_borders + 40,
            (x0_cadre + x1_cadre + pad_from_borders) // 3,
            y1_cadre - 20,
            text="Paysan 1 PA",
            rectangle_tags=set_tags(TOGGLEABLE_TAG, hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG),
            state="hidden"
        )

        # Artisan choix
        self.artisan_choice_id = self.canvas.create_text_in_rectangle(
            (x0_cadre + x1_cadre + pad_from_borders) // 3,
            y0_cadre + pad_from_borders + 40,
            (x0_cadre + x1_cadre) // 3 * 2,
            y1_cadre - 20,
            text="Artisan 2 PA",
            rectangle_tags=set_tags(TOGGLEABLE_TAG, hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG,),
            state="hidden"
        )

        # Soldat choix
        self.soldat_choice_id = self.canvas.create_text_in_rectangle(
            (x0_cadre + x1_cadre) // 3 * 2,
            y0_cadre + pad_from_borders + 40,
            x1_cadre - pad_from_borders,
            y1_cadre - 20,
            text="Soldat 2 PA",
            rectangle_tags=set_tags(TOGGLEABLE_TAG, hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG,),
            state="hidden"
        )

        self.radiobutton_choice = self.canvas.add_radiobutton(
            self.paysan_choice_id, self.artisan_choice_id, self.soldat_choice_id
        )

        # Ok bouton
        self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.ok_trigger, state="hidden", is_temp=True
        )

        # Annuler bouton
        self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.cancel, state="hidden", is_temp=True
        )

    def update(self):
        self.callback_quantity_selector(self.quantity_selector_hum.quantity)

    def ok_trigger(self, e=None):
        qt = self.quantity_selector_hum.quantity
        type_v = self.radiobutton_choice.get_selected_option()

        if type_v:
            self.canvas.save_villager_choice(type_v, qt)

            # Même comportement que si on ne voulait pas construire l'église, sauf qu'ici, on la construit
            self.cancel()

        else:
            bbox = self.canvas.bbox(self.tag)
            self.canvas.hudmobile_ilfautfaireunchoixgros.show(bbox[2] + 60, (bbox[3] + bbox[1]) // 2)
            self.shake()

    def cancel(self, e=None):

        # On reset l'effectif
        self.quantity_selector_hum.reset()

        # On reset les choix
        self.radiobutton_choice.reset()

        # On dégrise les options grisables
        self.degriser(self.artisan_choice_id)
        self.degriser(self.soldat_choice_id)

        # On met à jour le texte (sa valeur par défaut vu l'effectif a été reset)
        self.refresh_text()

        # On cache l'HUD
        self.hide()

    def callback_quantity_selector(self, old_quantity: int):

        new_quantity = self.quantity_selector_hum.quantity

        if self.canvas.jeu.joueur_actuel.pa < new_quantity * 2:
            # Si le joueur a selectionné ce choix
            if self.radiobutton_choice.get_selected_option() in [self.artisan_choice_id, self.soldat_choice_id]:
                self.radiobutton_choice.reset()

            # Griser le bouton artisan et ne le rendre plus clickable
            self.griser(self.artisan_choice_id)
            self.griser(self.soldat_choice_id)

            if self.canvas.jeu.joueur_actuel.pa < new_quantity:
                # Si le joueur a selectionné ce choix
                if self.radiobutton_choice.get_selected_option() == self.paysan_choice_id:
                    self.radiobutton_choice.reset()

                # Griser le bouton paysan et ne le rendre plus clickable
                self.griser(self.paysan_choice_id)

        # Si le nombre de PA du joueur dépasse le nouveau coût de l'effectif désiré d'artisan (donc affordable)
        # ET qu'avant ce n'était pas le cas, alors il faut dégriser.
        # if PA >= new_desired_workforce * 2 and PA < self.desired_workforce * 2:
        if new_quantity * 2 <= self.canvas.jeu.joueur_actuel.pa < old_quantity * 2:

            # Degriser le choix artisan et le rendre clickable
            self.degriser(self.artisan_choice_id)
            self.degriser(self.soldat_choice_id)

        if self.canvas.jeu.joueur_actuel.pa >= new_quantity:
            self.degriser(self.paysan_choice_id)

        self.refresh_text()

    def refresh_text(self):
        qt = self.quantity_selector_hum.quantity

        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.paysan_choice_id],
                      text=f"Paysan {qt} PA")
        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.artisan_choice_id],
                       text=f"Artisan {qt * 2} PA")
        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.soldat_choice_id],
                       text=f"Soldat {qt * 2} PA")

    def griser(self, button_id: int):
        tags = list(self.canvas.gettags(button_id))
        tags[HIGHLIGHT_TAG_INDEX] = NOTHING_TAG
        self.canvas.itemconfigure(button_id, fill=fill_darker[tags[3]])
        self.canvas.itemconfigure(button_id, tags=tags)

    def degriser(self, button_id: int):
        tags = list(self.canvas.gettags(button_id))
        tags[HIGHLIGHT_TAG_INDEX] = TOGGLEABLE_TAG
        self.canvas.itemconfigure(button_id, fill=tags[3])
        self.canvas.itemconfigure(button_id, tags=tags)

