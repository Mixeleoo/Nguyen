
import tkinter as tk

from parameter import *
from Canvas.HUD.HUDMobileABC import HUDMobileABC


class HUDMobileMoreInfo(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.num_page = 1

    @property
    def tag(self):
        return MORE_INFO_WINDOW

    def create(self):

        width = 200
        height = 100

        x0_cadre = 100
        y0_cadre = 100
        x1_cadre = x0_cadre + width
        y1_cadre = y0_cadre + height

        # Gros rectangle contenant toutes les infos
        self.canvas.create_text_in_rectangle(
            x0=x0_cadre, y0=y0_cadre + 20, x1=x1_cadre, y1=y1_cadre,
            fill=FILL_ACTION_BOX,
            text="Toutes les infos du villages (ou pas)",
            rectangle_tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden"
        )

        # Bouton pour fermer
        self.canvas.create_text_in_rectangle(
            x0=x1_cadre - 20,
            y0=y0_cadre,
            x1=x1_cadre,
            y1=y0_cadre + 20,
            fill=FILL_CANCEL,
            text="x",
            rectangle_tags=set_tags(CLICKABLE_TAG, CLOSE_MORE_INFO_WINDOW, color_tag=FILL_CANCEL, hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG,),
            state="hidden"
        )

        # Bouton pour pin
        self.canvas.create_text_in_rectangle(
            x0=x1_cadre - 40,
            y0=y0_cadre,
            x1=x1_cadre - 20,
            y1=y0_cadre + 20,
            fill=FILL_ACTION_BOX,
            text="pin",
            rectangle_tags=set_tags(CLICKABLE_TAG, PIN_MORE_INFO_WINDOW, hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG,),
            state="hidden"
        )

        # Rectangle pour bouger la fenêtre (en haut dcp)
        self.canvas.create_rectangle(
            x0_cadre,
            y0_cadre,
            x1_cadre - 40,
            y0_cadre + 20,
            fill=FILL_ACTION_BOX,
            tags=set_tags(drag_tag=MOVE_WINDOW, hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden"
        )

        # rectangles pour changer la taille de la fenêtre
        # Ils sont créés dans cet ordre : En haut à gauche, en haut à droite
        # En bas à gauche, en bas à droite
        for j in range(2):
            for i in range(2):
                item = self.canvas.create_rectangle(
                    [x0_cadre, x1_cadre][i] - 5,
                    [y0_cadre, y1_cadre][j] - 5,
                    [x0_cadre, x1_cadre][i] + 5,
                    [y0_cadre, y1_cadre][j] + 5,
                    fill=FILL_ACTION_BOX,
                    tags=set_tags(drag_tag=DRAG_CORNER_MORE_INFO_WINDOW_TAG, hud_tag=self.tag) + (TEMP_TAG,),
                    state="hidden"
                )

                self.canvas.tag_lower(item, MAP_TAG)

    def replace(self, event: tk.Event) -> None:
        pass
