
import tkinter as tk

from parameter import *
from Canvas.HUDs.HUDABC import HUDABC

class HUDTopSide(HUDABC):
    def __init__(self, canvas):
        super().__init__(canvas)

    @property
    def tag(self):
        return HUD_TOP_SIDE

    @property
    def arrival_pos_show(self) -> Position: return Position(0, 0)
    @property
    def curr_show_pos(self) -> Position: return Position(0, 0)
    @property
    def arrival_pos_hide(self) -> Position: return Position(0, 0)
    @property
    def curr_hide_pos(self) -> Position: return Position(0, 0)

    def create(self, geometry_width: int, geometry_height: int) -> None:

        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = geometry_width
        y1_cadre = HEIGHT_HUD_TOP_SIDE

        self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre, fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag)
        )

        #self.canvas.create_text()

    def replace(self, event: tk.Event) -> None:
        pass

    def _show_animation(self) -> None:
        pass

    def _hide_animation(self) -> None:
        pass