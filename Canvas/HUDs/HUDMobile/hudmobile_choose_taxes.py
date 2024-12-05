
import tkinter as tk

from parameter import *
from Canvas.HUDs.HUDMobile.HUDMobileABC import HUDMobileABC

class HUDMobileChooseTaxes(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.num_page_villages = 1
        self.num_page_vassals = 1

        self.text_page_villages_id = 0
        self.text_page_vassals_id = 0

    @property
    def tag(self):
        return HUD_CHOOSE_TAXES

    def create(self):

        # Gros rectangle contenant les 4 rectangles d'actions
        width = 480
        height = HEIGHT_BOTTOM_HUD  # valeurs qui ne bougent pas en fonction de la taille de la fenêtre

        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = x0_cadre + width
        y1_cadre = y0_cadre + height

        centre_x = (x0_cadre + x1_cadre) // 2
        pad = 5

        self.text_page_vassals_id = self.canvas.create_text(
            x0_cadre + 80,
            y0_cadre - 15,
            text=f"page : 1 / {len(ACTION_FOR_YOUR_TURN) // 2}",
            tags=set_tags(hud_tag=self.tag)
        )

        self.text_page_villages_id = self.canvas.create_text(
            x0_cadre + 80,
            y0_cadre - 15,
            text=f"page : 1 / {len(ACTION_FOR_YOUR_TURN) // 2}",
            tags=set_tags(hud_tag=self.tag)
        )

        # Bouton pour changer de page (précédente)
        self.canvas.add_button(
            hud_tag=self.tag,
            trigger_name=CHANGE_PAGE_MINUS,
            func_triggered=self.on_change_page,
            for_which_game_mode=("basic",)
        ).draw(
            x0_cadre + 5,
            y0_cadre - 20,
            x0_cadre + 20,
            y0_cadre - 5,
            text="◄",  # ►◄↓↑→←▲▼
        )

        # Bouton pour changer de page (suivante)
        self.canvas.add_button(
            hud_tag=self.tag,
            trigger_name=CHANGE_PAGE_PLUS,
            func_triggered=self.on_change_page,
            for_which_game_mode=("basic",)
        ).draw(
            x0_cadre + 25,
            y0_cadre - 20,
            x0_cadre + 40,
            y0_cadre - 5,
            text="►",  # ►◄↓↑→←▲▼
        )

    def replace(self, event: tk.Event):
        """
        Méthode qui replace l'HUD au centre de la fenêtre
        """

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

    def on_change_vassals_page(self, event: tk.Event):
        # Différienciation entre page précédente (M) et page suivante (P)
        if self.canvas.gettags("active")[TRIGGER_TAG_INDEX][-1] == "M":
            self.num_page_vassals = (self.num_page_vassals - 1) if self.num_page_vassals - 1 >= 1 else 1

        else:
            self.num_page_vassals = (self.num_page_vassals + 1) if self.num_page_vassals + 1 <= NB_ACTIONS // NB_ACTION_PER_PAGE else NB_ACTIONS // NB_ACTION_PER_PAGE

        for action_id_i in range(len(actions_rectangle_ids)):
            text_i = 0
            for text_category_i in range(len(text_categories)):
                # Modification du texte
                self.canvas.itemconfigure(
                    actions_text_ids[action_id_i * len(text_categories) + text_category_i],
                    text=ACTION_FOR_YOUR_TURN[(self.num_page_vassals - 1) * NB_ACTION_PER_PAGE + action_id_i][text_categories[text_category_i]]
                )
                text_i += 1

            # Modification des tags (pour savoir quelles fonctions vont être trigger)
            self.canvas.itemconfigure(
                actions_rectangle_ids[action_id_i],
                tags=set_tags(
                    highlight_tag=CLICKABLE_TAG,
                    trigger_tag=ACTION_FOR_YOUR_TURN[(self.num_page_vassals - 1) * NB_ACTION_PER_PAGE + action_id_i]["do"]
                ) + (RECTANGLE_ACTION, HUD_BOTTOM,)
            )

        self.canvas.itemconfigure(
            self.canvas.find_withtag(self.text_page_vassals_id)[0],
            text=f"page : {self.num_page_vassals} / {len(ACTION_FOR_YOUR_TURN) // 2}"
        )
