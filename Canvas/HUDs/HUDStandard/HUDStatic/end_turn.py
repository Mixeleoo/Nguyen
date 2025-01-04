from typing import Literal

from Canvas.Widget.Button import Button
from ..HUDStaticABC import HUDStaticABC
from parameter import *

class EndTurn(HUDStaticABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.state: Literal["hidden", "normal"] = "normal"

    @property
    def curr_show_pos(self) -> Position:
        bbox = self.canvas.bbox(self.tag)
        return Position(bbox[2], bbox[3])

    @property
    def curr_hide_pos(self) -> Position:
        bbox = self.canvas.bbox(self.tag)
        return Position(bbox[0], bbox[1])

    @property
    def arrival_pos_show(self) -> Position: return Position(self.canvas.master.winfo_width() - 10, self.canvas.master.winfo_height() - 10)
    @property
    def arrival_pos_hide(self) -> Position: return Position(self.canvas.master.winfo_width(), self.canvas.master.winfo_height())

    def create(self, geometry_width, geometry_height):

        width = WIDTH_HISTORY_HUD
        height = HEIGHT_BOTTOM_HUD + PADY_BOTTOM_HUD

        Button(
            self.canvas,
            hud_tag=self.tag,
            trigger_name="end_turn",
            func_triggered=self.trigger,
            for_which_game_mode=("basic",)
        ).draw(
            x0=geometry_width - width,
            y0=geometry_height - height,
            x1=geometry_width,
            y1=geometry_height,
            text="Fin de tour"
        )

    def replace(self, *args) -> None:
        bbox = self.bbox()
        dx = self.canvas.winfo_width() - bbox[2]
        dy = self.canvas.winfo_height() - bbox[3]

        self.canvas.move(self.tag, dx, dy)

    def trigger(self, *args):
        self.canvas.end_turn_trigger()

    def bhide(self):
        self.state = "hidden"
        self.hide_animation()

    def bshow(self):
        self.state = "normal"
        self.show_animation()
