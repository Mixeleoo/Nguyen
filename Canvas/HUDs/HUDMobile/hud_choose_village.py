
from typing import Optional
import tkinter as tk

from Canvas.HUDs.Button import Button
from Canvas.Radiobutton import Radiobutton
from parameter import *
from Canvas.HUDs.HUDMobile.HUDMobileABC import HUDMobileABC

class HUDChooseVillage(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.background_rectangle_id = 0
        self.ok_button: Optional[Button] = None
        self.cancel_button: Optional[Button] = None

        # id du dernier village choisi
        self.last_choice_made = 0
        self.radiobutton_village_choix: Optional[Radiobutton] = None

        self.from_radiobutton_item_id_to_city_id: dict[int, int] = {}

    @property
    def tag(self):
        return CHOOSE_VILLAGE_TAG

    def create(self) -> None:

        height = 20

        title_text = "Où immigrer ces villageois ?"

        # Mesurer la largeur et la hauteur du texte
        # Ici, ajout d'un pad sur la largeur pour éviter d'avoir un rectangle PARFAITEMENT à la largeur du texte
        text_width = get_width_text(title_text)

        # coordonnées du rectangle principal pour l'avoir au milieu de l'écran
        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = text_width
        y1_cadre = height

        center_x = (x0_cadre + x1_cadre) // 2

        self.background_rectangle_id = self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre, fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,), state="hidden"
        )

        self.canvas.create_text(
            center_x, y0_cadre + 10,
            text=title_text,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden",
                fill=FILL_TEXT
        )

        # Bouton OK qui lance l'immigration
        self.ok_button = self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.immigrate,
            trigger_name=IMMIGRATE_TAG, is_temp=True, state="hidden"
        )

        # Radiobutton du choix du village
        self.radiobutton_village_choix = self.canvas.add_radiobutton(())

        # Bouton Annuler qui annule l'immigration
        self.cancel_button = self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.bhide,
            trigger_name=CANCEL_CHOOSE_VILLAGE_TO_IMMIGRATE_TAG, is_temp=True, state="hidden"
        )

    def replace(self) -> None:

        bbox = self.canvas.bbox(self.tag)

        dx = self.canvas.master.winfo_width() // 2 - (bbox[2] + bbox[0]) // 2
        dy = self.canvas.master.winfo_height() // 2 - (bbox[3] + bbox[1]) // 2

        self.canvas.move(self.tag, dx, dy)

    def add_village_update_HUD(self, name: str, city_id: int) -> int:
        """
        Mettre à jour la taille du rectangle en background
        Ajouter la nouvelle option graphiquement + dans le radiobutton
        Déplacer le bouton OK et le bouton Annuler en bas
        """
        coords = self.canvas.coords(self.background_rectangle_id)

        coords[3] += 40

        self.canvas.coords(self.background_rectangle_id, coords[0], coords[1], coords[2], coords[3])

        # Ajouter la nouvelle option
        new_category_id = self.canvas.create_text_in_rectangle(
            coords[0], coords[3] - 40, coords[2], coords[3],
            text=name,
            rectangle_tags=set_tags(highlight_tag=TOGGLEABLE_TAG, hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG),
            fill=FILL_ACTION_BOX,
            state="hidden"
        )

        self.canvas.tag_lower(new_category_id, self.ok_button.id)
        self.canvas.tag_lower(self.canvas.text_id_in_rectangle_id[new_category_id], self.ok_button.id)

        # Déplacer vers le bas de la hauteur de la nouvelle catégorie les deux boutons
        self.ok_button.move(0, 40)
        self.cancel_button.move( 0, 40)

        # J'associe l'id du village à l'id du choix (= le rectangle correspondant au choix)
        self.from_radiobutton_item_id_to_city_id[new_category_id] = city_id
        self.radiobutton_village_choix.add_option(new_category_id)

        return new_category_id

    def immigrate(self, event: tk.Event) -> None:
        """
        Méthode qui met à jour le dernier choix de l'utilisateur dans l'attribut self.last_choice_made
        """
        self.last_choice_made = self.radiobutton_village_choix.get_selected_option()

        if self.last_choice_made:

            effectif = self.canvas.hud_paysan_or_artisan.last_choice_made[0]
            type_v = self.canvas.hud_paysan_or_artisan.last_choice_made[1]
            village_id = self.from_radiobutton_item_id_to_city_id[self.last_choice_made]

            # lancer l'immigration du jeu
            self.canvas.jeu.immigrer(
                effectif=effectif,
                type_v=type_v,
                village_id=village_id
            )

            self.canvas.hud_history.add_text(f"Vous avez immigré {effectif} {type_v} dans le village {village_id} !")

            # Même comportement que si on annulait, mais précédé par la validation
            self.bhide()

        else:
            print("T'as pas choisi de village là bro")

    def bhide(self, *args):
        self.radiobutton_village_choix.reset()
        self.hide()
