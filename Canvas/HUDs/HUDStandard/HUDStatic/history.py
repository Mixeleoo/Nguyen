
import tkinter as tk

from Canvas.Widget.Button import Button
from Canvas.Widget.Scrollbar import Scrollbar
from ..HUDHideable import HUDHideableABC
from ..HUDStaticABC import HUDStaticABC
from parameter import HISTORY_TEXT, Position, HEIGHT_BOTTOM_HUD, WIDTH_HISTORY_HUD, SHOW_OR_HIDE_HISTORY_TAG, PADY_BUILD_CITY_HUD, FILL_ACTION_BOX, set_tags

class History(HUDStaticABC, HUDHideableABC):
    def __init__(self, canvas):
        HUDHideableABC.__init__(self, canvas)
        HUDStaticABC.__init__(self, canvas)

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
    @property
    def hide_symbol(self) -> str: return "►"
    @property
    def show_symbol(self) -> str: return "◄"

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
        self.hide_button_id = Button(
            self.canvas,
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
            0
        )
