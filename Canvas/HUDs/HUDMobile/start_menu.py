
from Canvas.HUDs.HUDMobile.base import HUDMobileABC
from Perso import Vassal
from parameter import *

class StartMenu(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.radiobutton = self.canvas.add_radiobutton()

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
            self.canvas.start
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

        self.canvas.create_text(
            center_x, center_y + 80, tags=set_tags(hud_tag=self.tag),
            text="Choisissez une couleur ou on choisira pour vous.",
            fill=FILL_TEXT
        )

        x = int(center_x * 0.25)
        xstep = int(center_x * 1.5) // len(Vassal.couleurs)
        for couleur in Vassal.couleurs:
            nx = x + xstep
            rect_id = self.canvas.create_rectangle(
                x,
                center_y + 120,
                nx,
                center_y + 160,
                tags=set_tags(TOGGLEABLE_TAG, hud_tag=self.tag, color_tag=couleur),
                fill=couleur
            )

            t_id = self.canvas.create_text(
                (x + nx) // 2, (center_y + 120 + center_y + 160) // 2,
                text=couleur, tags=set_tags(hud_tag=self.tag) + (TEXT_TAG,), fill=FILL_TEXT
            )

            self.canvas.text_id_in_rectangle_id[t_id] = rect_id

            x = int(nx)
            self.radiobutton.add_option(rect_id)

    def replace(self, *args) -> None:
        self.canvas.tag_raise(self.tag)

    def get_color_choice(self):
        if self.radiobutton.currently_selected is not None:
            # Quand je récupère les tags ça me renvoie même pas une liste, ça me renvoie les tags avec des espaces ?? c'est vraiment pourri tkinter
            return self.canvas.itemcget(self.radiobutton.currently_selected, "tags").split(" ")[COLOR_TAG_INDEX]

        else: return None
