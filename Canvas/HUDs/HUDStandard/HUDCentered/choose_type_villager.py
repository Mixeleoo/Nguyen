
from typing import Optional

from ..HUDCenteredABC import HUDCenteredABC
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
            state="hidden",
            justify="center"
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
            state="hidden",
            justify="center"
        )

        # Soldat choix
        self.soldat_choice_id = self.canvas.create_text_in_rectangle(
            (x0_cadre + x1_cadre) // 3 * 2,
            y0_cadre + pad_from_borders + 40,
            x1_cadre - pad_from_borders,
            y1_cadre - 20,
            text="Soldat 2 PA\n💰 : 20",
            rectangle_tags=set_tags(TOGGLEABLE_TAG, hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG,),
            state="hidden",
            justify="center"
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

    def update(self, *args):
        if self.canvas.jeu.joueur_actuel.pa < 2:
            # Griser le bouton et ne le rendre plus clickable
            self.griser(self.artisan_choice_id)
            self.griser(self.soldat_choice_id)

            if self.canvas.jeu.joueur_actuel.pa < 1:
                # Griser le bouton et ne le rendre plus clickable
                self.griser(self.paysan_choice_id)

        elif self.canvas.jeu.joueur_actuel.argent < 20:
            # Griser le bouton et ne le rendre plus clickable
            self.griser(self.soldat_choice_id)

        self.quantity_selector_hum.set_max_quantity(self.canvas.jeu.joueur_actuel.pa)

    def ok_trigger(self, e=None):
        qt = self.quantity_selector_hum.quantity
        type_v = self.radiobutton_choice.get_selected_option()

        if type_v:
            self.canvas.save_villager_choice(type_v, qt)

            # Même comportement que si on ne voulait pas construire l'église, sauf qu'ici, on la construit
            self.cancel()

        else:
            bbox = self.canvas.bbox(self.tag)
            self.canvas.hud_ilfautfaireunchoix.show(bbox[2] + 60, (bbox[3] + bbox[1]) // 2)
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

    def check_choice_affordable(self, choice_id: int, previous_pa_cost: int, pa_cost: int, money_cost: int = 0, previous_money_cost: int = 0):
        """
        Quand je clique sur +:
            Si j'ai dépassé le CAP de PA et/ou argent pour immigrer/recruter:
                Si j'ai préalablement sélectionné le choix:
                    Déselectionner le choix
                Griser le choix

        Quand je clique sur -:
            Si j'ai de nouveau assez pour immigrer/recruter:
                Degriser le choix
        """
        if previous_pa_cost <= self.canvas.jeu.joueur_actuel.pa < pa_cost or previous_money_cost <= self.canvas.jeu.joueur_actuel.argent < money_cost:
            # Si le joueur a selectionné ce choix
            if self.radiobutton_choice.get_selected_option() == choice_id:
                self.radiobutton_choice.reset()

            # Griser le bouton et ne le rendre plus clickable
            self.griser(choice_id)

        # Si précédemment il y avait pas assez de PA ou d'argent ET que la nouvelle quantité d'argent et de PA est affordable.
        elif (previous_pa_cost > self.canvas.jeu.joueur_actuel.pa or previous_money_cost > self.canvas.jeu.joueur_actuel.argent) and self.canvas.jeu.joueur_actuel.pa >= pa_cost and self.canvas.jeu.joueur_actuel.argent >= money_cost:
            self.degriser(choice_id)

    def callback_quantity_selector(self, previous_quantity: int):

        new_quantity = self.quantity_selector_hum.quantity

        self.check_choice_affordable(self.paysan_choice_id, previous_quantity, new_quantity)
        self.check_choice_affordable(self.artisan_choice_id, previous_quantity * 2, new_quantity * 2)
        self.check_choice_affordable(
            self.soldat_choice_id,
            previous_quantity * 2,
            new_quantity * 2,
            previous_money_cost=previous_quantity * 20,
            money_cost=new_quantity * 20
        )

        self.refresh_text()

    def refresh_text(self):
        qt = self.quantity_selector_hum.quantity

        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.paysan_choice_id],
                      text=f"Paysan {qt} PA")
        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.artisan_choice_id],
                       text=f"Artisan {qt * 2} PA")
        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.soldat_choice_id],
                       text=f"Soldat {qt * 2} PA\n💰 : {qt * 20}")

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

