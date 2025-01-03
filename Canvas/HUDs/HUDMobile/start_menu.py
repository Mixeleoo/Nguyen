
from Canvas.HUDs.HUDMobile.base import HUDMobileABC
from parameter import *

class StartMenu(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

    def create(self, geometry_width, geometry_height):

        center_x = geometry_width // 2
        center_y = geometry_height // 2

        self.canvas.create_rectangle(
            0, 0, geometry_width, geometry_height,
            fill=FILL_ACTION_BOX,
            tags=set_tags(hud_tag=self.tag)
        )

        self.canvas.add_button(
            self.tag,
            "HIDE_START_MENU",
            self.hide
        ).draw(
            center_x - 60,
            center_y - 40,
            center_x + 60,
            center_y - 20,
            text="Commencer"
        )

        self.canvas.add_button(
            self.tag,
            "QUIT",
            lambda e: self.canvas.quit()
        ).draw(
            center_x - 60,
            center_y + 20,
            center_x + 60,
            center_y + 40,
            text="Sortez-moi de là"
        )

    def replace(self, *args) -> None:
        self.canvas.tag_raise(self.tag)
