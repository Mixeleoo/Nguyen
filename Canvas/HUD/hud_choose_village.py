
import tkinter as tk

from Canvas.Radiobutton import Radiobutton
from parameter import *
from Canvas.HUD.HUDMobileABC import HUDMobileABC

class HUDChooseVillage(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.background_rectangle_id = 0
        self.ok_button_id = 0
        self.cancel_button_id = 0

        self.radiobutton_village_choix: Radiobutton

    @property
    def tag(self):
        return CHOOSE_VILLAGE_TAG

    def create(self, geometry_width: int, geometry_height: int) -> None:

        height = 60

        title_text = "Où immigrer ces villageois ?"

        # Mesurer la largeur et la hauteur du texte
        # Ici, ajout d'un pad sur la largeur pour éviter d'avoir un rectangle PARFAITEMENT à la largeur du texte
        text_width = get_width_text(title_text)

        # coordonnées du rectangle principal pour l'avoir au milieu de l'écran
        x0_cadre = geometry_width // 2 - text_width // 2
        y0_cadre = geometry_height // 2 - height // 2
        x1_cadre = x0_cadre + text_width
        y1_cadre = y0_cadre + height

        center_x = (x0_cadre + x1_cadre) // 2

        self.background_rectangle_id = self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre, fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,), state="hidden"
        )

        self.canvas.create_text(
            center_x, y0_cadre + 10, text=title_text, tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,), state="hidden"
        )

        # Le seigneur n'a qu'un seul village au début, donc on ne crée qu'une ligne
        village_id = self.canvas.create_text_in_rectangle(
            x0_cadre, y0_cadre + 20, x1_cadre, y0_cadre + 60,
            text="village 1",
            rectangle_tags=set_tags(highlight_tag=TOGGLEABLE_TAG, hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG), state="hidden"
        )

        # Bouton OK qui lance l'immigration
        self.ok_button_id = self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.immigrate,
            trigger_name=IMMIGRATE_TAG, is_temp=True, state="hidden"
        )

        # Radiobutton du choix du village
        self.radiobutton_village_choix = self.canvas.radiobuttons.add((village_id,),
            ok_button_id=self.ok_button_id
        )

        # Bouton Annuler qui annule l'immigration
        self.cancel_button_id = self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.hide,
            trigger_name=CANCEL_CHOOSE_VILLAGE_TO_IMMIGRATE_TAG, is_temp=True, state="hidden"
        )

    def replace(self) -> None:
        pass

    def add_village_update_HUD(self, name: str) -> int:
        """
        Mettre à jour la taille du rectangle en background
        Ajouter la nouvelle option
        Déplacer le bouton OK et le bouton Annuler en bas
        """
        coords = self.canvas.coords(self.background_rectangle_id)

        coords[3] += 40

        self.canvas.coords(self.background_rectangle_id, coords[0], coords[1], coords[2], coords[3])

        # Ajouter la nouvelle option
        new_category_id = self.canvas.create_text_in_rectangle(
            coords[0], coords[3] - 40, coords[2], coords[3],
            text=name,
            rectangle_tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG),
            fill=FILL_ACTION_BOX,
            state="hidden"
        )

        self.canvas.tag_lower(new_category_id, self.ok_button_id)
        self.canvas.tag_lower(self.canvas.text_id_in_rectangle_id[new_category_id], self.ok_button_id)

        # Déplacer vers le bas de la hauteur de la nouvelle catégorie les deux boutons
        self.canvas.move(self.ok_button_id, 0, 40)
        self.canvas.move(self.cancel_button_id, 0, 40)

        self.canvas.move(self.canvas.text_id_in_rectangle_id[self.ok_button_id], 0, 40)
        self.canvas.move(self.canvas.text_id_in_rectangle_id[self.cancel_button_id], 0, 40)

        return new_category_id

    def immigrate(self, event: tk.Event) -> None:
        print(self.canvas.radiobuttons.get_selected_option(self.canvas.gettags("active")[GROUP_TAG_INDEX]))
