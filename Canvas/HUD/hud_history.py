
import tkinter as tk

from parameter import *
from Canvas.HUD.HUDABC import HUDABC

class HUDHistory(HUDABC):
    def __init__(self, canvas):
        super().__init__(canvas)

    @property
    def tag(self):
        return HUD_RIGHT_SIDE

    def create(self, geometry_width: int, geometry_height: int):

        pady_from_top = 5
        # Gros rectangle contenant l'historique
        width = 145  # valeurs qui ne bouge pas en fonction de la taille de la fenêtre
        height = geometry_height - HEIGHT_BOTTOM_HUD - pady_from_top  # valeur qui ne bouge pas en fonction de la taille de la fenêtre

        x1_cadre = geometry_width - pady_from_top
        x0_cadre = x1_cadre - width
        y0_cadre = 5
        y1_cadre = y0_cadre + height

        # Rectangle de l'historique
        self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre,
            fill=FILL_ACTION_BOX, tags=set_tags() + (HUD_RIGHT_SIDE,)
        )

        # Rectangle pour ranger l'historique
        self.canvas.create_rectangle(
            x0_cadre - 20,
            y1_cadre - 20,
            x0_cadre - 5,
            y1_cadre - 5,
            fill=FILL_ACTION_BOX, tags=set_tags(CLICKABLE_TAG, HIDE_HISTORY) + (HUD_RIGHT_SIDE,)
        )

        # Scrollbar
        self.canvas.create_rectangle(
            geometry_width - 5 - 15,
            5 + 25,
            geometry_width - 5 - 5,
            5 + 45,
            fill=FILL_ACTION_BOX, tags=set_tags(CLICKABLE_TAG, drag_tag=SCROLLBAR_TAG) + (HUD_RIGHT_SIDE,)
        )

        for i in range(60):
            self.canvas.create_text((geometry_width - 150 + geometry_width - 5) // 2, - 50 + i * 20,
                                    text=f"slt je suis le n°{('0' + str(i)) if i < 10 else i}",
                                    tags=set_tags() + (HISTORY_TEXT, HUD_RIGHT_SIDE))


        # to_hide_text_rectangle
        to_hide_text_rectangle_haut = self.canvas.create_rectangle(
            x0_cadre + 1,
            y0_cadre + 1,
            x1_cadre,
            y0_cadre + 20,
            fill=FILL_ACTION_BOX, tags=set_tags() + (HUD_RIGHT_SIDE, RECTANGLE_HIDING_TOP_HISTORY_TEXT,), width=0
        )

        to_hide_text_rectangle_bas = self.canvas.create_rectangle(
            x0_cadre + 1,
            y1_cadre - 20,
            x1_cadre,
            y1_cadre,
            fill=FILL_ACTION_BOX, tags=set_tags() + (HUD_RIGHT_SIDE,), width=0
        )

        self.canvas.tag_lower(HISTORY_TEXT, to_hide_text_rectangle_haut)
        self.canvas.tag_lower(to_hide_text_rectangle_haut, to_hide_text_rectangle_bas)

    def replace(self, event: tk.Event):
        """
        Replacer l'HUD du bas:
        - mouvement sur x : L'ensemble reste à gauche de l'écran.
        - mouvement sur y : L'ensemble reste en haut de la fenêtre et
            il faut faire un homotéthie de l'historique en fonction de l'agrandissement de la fenêtre
        """
        self.canvas.move(
            HUD_RIGHT_SIDE,
            event.width - self.canvas.master.previous_geometry[0],
            5 - self.canvas.coords(self.canvas.find_withtag(RECTANGLE_HIDING_TOP_HISTORY_TEXT)[0])[1]
        )

    def show_animation(self):
        self.canvas.move(self.tag,
                         -(abs(self.canvas.master.winfo_width() - 155 - self.canvas.coords(HIDE_HISTORY)[2]) // 10 + 1), 0)

        if self.canvas.coords(HIDE_HISTORY)[2] != self.canvas.master.winfo_width() - 155:
            self.canvas.after(DELTA_MS_ANIMATION, self.show_animation)

    def hide_animation(self):
        self.canvas.move(self.tag, abs(self.canvas.master.winfo_width() - 5 - self.canvas.coords(SHOW_HISTORY)[2]) // 10 + 1, 0)

        if self.canvas.coords(SHOW_HISTORY)[2] != self.canvas.master.winfo_width() - 5:
            self.canvas.after(DELTA_MS_ANIMATION, self.hide_animation)

    def hide_history(self, e=None): self.hide_show_hud(HIDE_HISTORY, SHOW_HISTORY, self.hide_animation)
    def show_history(self, e=None): self.hide_show_hud(SHOW_HISTORY, HIDE_HISTORY, self.show_animation)
