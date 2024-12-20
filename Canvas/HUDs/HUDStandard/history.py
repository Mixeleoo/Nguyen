
import tkinter as tk
from typing import Literal

from Canvas.Widget.Scrollbar import Scrollbar
from .base import HUDABC
from parameter import *

class History(HUDABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.state: Literal["normal", "hidden"] = "normal"
        self.hide_button_id = None
        self.background_rect_id = None

        self.scrollbar = Scrollbar(self.canvas, self.tag, HISTORY_TEXT)
        self.add_text = self.scrollbar.add_text
        self.hide_exceeding_text = self.scrollbar.hide_exceeding_text

    @property
    def arrival_pos_show(self) -> Position: return Position(self.canvas.master.winfo_width() - 15, 0)
    @property
    def curr_show_pos(self) -> Position: return Position(self.canvas.coords(self.background_rect_id)[2], 0)
    @property
    def arrival_pos_hide(self) -> Position: return Position(self.canvas.master.winfo_width() - 5, 0)
    @property
    def curr_hide_pos(self) -> Position: return Position(self.canvas.coords(SHOW_OR_HIDE_HISTORY_TAG)[2], 0)

    def create(self, geometry_width: int, geometry_height: int):

        pady_from_top = 5

        # Gros rectangle contenant l'historique
        height = geometry_height - HEIGHT_BOTTOM_HUD - pady_from_top - 70  # valeur qui ne bouge pas en fonction de la taille de la fenêtre

        x1_cadre = geometry_width - pady_from_top
        x0_cadre = x1_cadre - WIDTH_HISTORY_HUD
        y0_cadre = PADY_BUILD_CITY_HUD
        y1_cadre = y0_cadre + height

        # Rectangle de l'historique
        self.background_rect_id = self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre,
            fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag)
        )

        # Rectangle pour ranger l'historique
        self.hide_button_id = self.canvas.add_button(
            hud_tag=self.tag,
            trigger_name=SHOW_OR_HIDE_HISTORY_TAG,
            func_triggered=self.show_or_hide
        ).draw(
            x0=x0_cadre - 20,
            y0=y1_cadre - 20,
            x1=x0_cadre - 5,
            y1=y1_cadre - 5,
            text="►"
        )

        self.scrollbar.create(x0_cadre, y0_cadre, x1_cadre, y1_cadre)

    def replace(self, event: tk.Event):
        """
        Replacer l'HUDs du bas:
        - mouvement sur x : L'ensemble reste à gauche de l'écran.
        - mouvement sur y : L'ensemble reste en haut de la fenêtre et
            il faut faire un homotéthie de l'historique en fonction de l'agrandissement de la fenêtre
        """
        self.canvas.move(
            self.tag,
            event.width - self.canvas.master.previous_geometry[0],
            PADY_BUILD_CITY_HUD - self.canvas.coords(self.background_rect_id)[1]
        )

    def bhide(self):
        """
        La phase before hide, qui consiste à changer l'état du HUDs en "hidden" et lancer l'animation
        """
        self.state = "hidden"
        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.hide_button_id], text="◄")
        self.hide_animation()

    def bshow(self):
        """
        La phase before show, qui consiste à changer l'état du HUDs en "normal" et lancer l'animation
        """
        self.state = "normal"
        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.hide_button_id], text="►")
        self.show_animation()

    def show_or_hide(self, e=None):
        if self.state == "normal":
            self.bhide()

        else:
            self.bshow()
