
import tkinter as tk
from typing import Literal

from parameter import *
from Canvas.HUD.HUDABC import HUDABC

class HUDActions(HUDABC):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.num_page = 1

        self.state: Literal["normal", "hidden"] = "normal"

    @property
    def tag(self):
        return HUD_BOTTOM

    def create(self, geometry_width, geometry_height):

        # Gros rectangle contenant les 4 rectangles d'actions
        width = 480
        height = HEIGHT_BOTTOM_HUD  # valeurs qui ne bougent pas en fonction de la taille de la fenêtre

        x0_cadre = PADX_BOTTOM_HUD
        x1_cadre = x0_cadre + width
        y1_cadre = geometry_height - PADY_BOTTOM_HUD
        y0_cadre = y1_cadre - height

        centre_x = (x0_cadre + x1_cadre) // 2

        # Comme la création des carrés, on va créer les rectangles d'actions automatiquement,
        # D'abord le rectangle allant de x0_cadre à centre_x et de y0_cadre à centre_y
        # Puis le rectangle allant de centre_x à x1_cadre et de y0_cadre à centre_y, etc.
        x_values = [x0_cadre, centre_x, x1_cadre]
        pad = 5

        # Commentaire numéro 10
        for x_value_i in range(len(x_values) - 1):
            # Commentaire numéro 11 Ok, on est bon
            id_rectangle = self.canvas.create_rectangle(
                x_values[x_value_i], y0_cadre, x_values[x_value_i + 1], y1_cadre,
                fill=FILL_ACTION_BOX,
                tags=set_tags(CLICKABLE_TAG, ACTION_FOR_YOUR_TURN[x_value_i]["do"], hud_tag=self.tag) + (RECTANGLE_ACTION,)
            )

            # Titre de l'action
            id_text = self.canvas.create_text(
                x_values[x_value_i] + pad, y0_cadre + pad,
                text=ACTION_FOR_YOUR_TURN[x_value_i]["text"],
                anchor="nw",
                tags=set_tags(hud_tag=self.tag) + (TEXT_ACTION, TEXT_TAG,)
            )

            self.canvas.text_id_in_rectangle_id[id_text] = id_rectangle

            # Nombre de points d'actions utilisés
            id_text = self.canvas.create_text(
                x_values[x_value_i + 1] - pad, y0_cadre + pad,
                text=ACTION_FOR_YOUR_TURN[x_value_i]["PA"],
                anchor="ne",
                tags=set_tags(hud_tag=self.tag) + (TEXT_ACTION, TEXT_TAG,)
            )

            self.canvas.text_id_in_rectangle_id[id_text] = id_rectangle

            # Coûts supplémentaires potentiels (argent, ressources)
            id_text = self.canvas.create_text(
                x_values[x_value_i + 1] - pad, y0_cadre + pad + 20,
                text=ACTION_FOR_YOUR_TURN[x_value_i]["additionalcost"],
                anchor="ne",
                font=("ateztzerz", SIZE_ACTION_ADDITIONAL_COST_TEXT),
                tags=set_tags(hud_tag=self.tag) + (TEXT_ACTION, TEXT_TAG,)
            )

            self.canvas.text_id_in_rectangle_id[id_text] = id_rectangle

        self.canvas.create_text(
            x0_cadre + 80,
            y0_cadre - 15,
            text=f"page : 1 / {len(ACTION_FOR_YOUR_TURN) // 2}",
            tags=set_tags(hud_tag=self.tag) + (TEXT_PAGE,)
        )

        # Bouton pour changer de page (précédente)
        self.canvas.create_button(
            x0_cadre + 5,
            y0_cadre - 20,
            x0_cadre + 20,
            y0_cadre - 5,
            text="◄",  # ►◄↓↑→←▲▼
            hud_tag=self.tag, func_triggered=self.on_change_page, trigger_name=CHANGE_PAGE_MINUS,
            for_which_game_mode=("basic",)
        )

        # Bouton pour changer de page (suivante)
        self.canvas.create_button(
            x0_cadre + 25,
            y0_cadre - 20,
            x0_cadre + 40,
            y0_cadre - 5,
            text="►",  # ►◄↓↑→←▲▼
            hud_tag=self.tag, func_triggered=self.on_change_page, trigger_name=CHANGE_PAGE_PLUS,
            for_which_game_mode=("basic",)
        )

        # Bouton pour cacher l'hud du bas
        self.canvas.create_button(
            x1_cadre - 20,
            y0_cadre - 20,
            x1_cadre - 5,
            y0_cadre - 5,
            text="▼",
            hud_tag=self.tag, func_triggered=self.show_or_hide, trigger_name=SHOW_OR_HIDE_PAGE_TAG,
            for_which_game_mode=("basic",)
        )

    def replace(self, event: tk.Event):
        """
        Replacer l'HUD du bas:
        - mouvement sur x : Son centre reste au centre de l'image donc on prend la distance entre l'ancien centre et
            le nouveau et on déplace tous les éléments du HUD de cette distance
        - mouvement sur y : On déplace tous les éléments
        """
        self.canvas.move(
            HUD_BOTTOM,
            PADX_BOTTOM_HUD + 5 - self.canvas.coords(self.canvas.find_withtag(CHANGE_PAGE_MINUS)[0])[0],
            event.height - self.canvas.master.previous_geometry[1]
        )

    def show_animation(self):
        self.canvas.move(self.tag, 0,
                         -(abs(self.canvas.master.winfo_height() - HEIGHT_BOTTOM_HUD - 5 - PADY_BOTTOM_HUD - self.canvas.coords(SHOW_OR_HIDE_PAGE_TAG)[3]) // 10 + 1))

        if self.canvas.coords(SHOW_OR_HIDE_PAGE_TAG)[3] != self.canvas.master.winfo_height() - HEIGHT_BOTTOM_HUD - 5 - PADY_BOTTOM_HUD:
            self.canvas.after(DELTA_MS_ANIMATION, self.show_animation)

    def hide_animation(self):
        self.canvas.move(self.tag, 0, abs(self.canvas.master.winfo_height() - 5 - self.canvas.coords(SHOW_OR_HIDE_PAGE_TAG)[3]) // 10 + 1)

        if self.canvas.coords(SHOW_OR_HIDE_PAGE_TAG)[3] != self.canvas.master.winfo_height() - 5:
            self.canvas.after(DELTA_MS_ANIMATION, self.hide_animation)

    def bhide(self):
        """
        La phase before hide, qui consiste à changer l'état du HUD en "hidden" et lancer l'animation
        """
        self.state = "hidden"
        self.hide_animation()

    def bshow(self):
        """
        La phase before show, qui consiste à changer l'état du HUD en "normal" et lancer l'animation
        """
        self.state = "normal"
        self.show_animation()

    def show_or_hide(self, e=None):
        if self.state == "normal":
            self.bhide()

        else:
            self.bshow()

    def on_change_page(self, event: tk.Event):
        # Différienciation entre page précédente (M) et page suivante (P)
        if self.canvas.gettags("active")[TRIGGER_TAG_INDEX][-1] == "M":
            self.num_page = (self.num_page - 1) if self.num_page - 1 >= 1 else 1

        else:
            self.num_page = (self.num_page + 1) if self.num_page + 1 <= NB_ACTIONS // NB_ACTION_PER_PAGE else NB_ACTIONS // NB_ACTION_PER_PAGE

        actions_rectangle_ids = self.canvas.find_withtag(RECTANGLE_ACTION)
        actions_text_ids = self.canvas.find_withtag(TEXT_ACTION)

        for action_id_i in range(len(actions_rectangle_ids)):
            text_i = 0
            for text_category_i in range(len(text_categories)):
                # Modification du texte
                self.canvas.itemconfigure(
                    actions_text_ids[action_id_i * len(text_categories) + text_category_i],
                    text=ACTION_FOR_YOUR_TURN[(self.num_page - 1) * NB_ACTION_PER_PAGE + action_id_i][text_categories[text_category_i]]
                )
                text_i += 1

            # Modification des tags (pour savoir quelles fonctions vont être trigger)
            self.canvas.itemconfigure(
                actions_rectangle_ids[action_id_i],
                tags=set_tags(
                    highlight_tag=CLICKABLE_TAG,
                    trigger_tag=ACTION_FOR_YOUR_TURN[(self.num_page - 1) * NB_ACTION_PER_PAGE + action_id_i]["do"]
                ) + (RECTANGLE_ACTION, HUD_BOTTOM,)
            )

        self.canvas.itemconfigure(self.canvas.find_withtag(TEXT_PAGE)[0], text=f"page : {self.num_page} / {len(ACTION_FOR_YOUR_TURN) // 2}")
