
from dataclasses import dataclass
from decimal import DivisionImpossible
from tkinter import font

from Canvas.HUDs.HUDMobile.base import HUDMobileABC
from Perso import Vassal
from parameter import set_tags, FILL_ACTION_BOX, FILL_TEXT, TOGGLEABLE_TAG, TEXT_TAG, COLOR_TAG_INDEX

@dataclass
class Difficulty:
    name: str
    nb_nobles: int
    description: str
    color: str

ldifficulties: list[Difficulty] = [
    Difficulty("Facile", 3, "3 nobles à vaincre", "#4bb02c"),
    Difficulty("Normal", 5, "5 nobles à vaincre", "#b06c2c"),
    Difficulty("Difficile", 10, "10 nobles à vaincre", "#ad2128")
]

class StartMenu(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.radiobutton_color = self.canvas.add_radiobutton()
        self.radiobutton_difficulty = self.canvas.add_radiobutton()

        self.dict_difficulty: [int, Difficulty] = {}

    def create(self, geometry_width, geometry_height):

        center_x = geometry_width // 2
        center_y = geometry_height // 2

        custom_font = font.nametofont("TkDefaultFont").copy()
        custom_font.configure(size=18)

        self.canvas.create_rectangle(
            0, 0, geometry_width, geometry_height,
            fill=FILL_ACTION_BOX,
            tags=set_tags(hud_tag=self.tag)
        )

        self.canvas.create_text(
            center_x, center_y - 180, tags=set_tags(hud_tag=self.tag),
            text="Voilà notre jeu !!!\n",
            fill=FILL_TEXT,
            font=custom_font,
            justify="center"
        )

        self.canvas.create_text(
            center_x, center_y - 160, tags=set_tags(hud_tag=self.tag),
            text="Hum hum *bruit de corbeau*, un peu vide ici...",
            fill=FILL_TEXT,
            justify="center"
        )

        self.canvas.create_text(
            center_x, center_y - 140, tags=set_tags(hud_tag=self.tag),
            text="Choissiez un niveau de difficulté.",
            fill=FILL_TEXT,
            justify="center"
        )

        x = int(center_x * 0.5)
        xstep = int(center_x) // len(ldifficulties)
        rect_id = 0
        for difficulty in ldifficulties:
            nx = x + xstep
            rect_id = self.canvas.create_rectangle(
                x,
                center_y - 110,
                nx,
                center_y - 70,
                tags=set_tags(TOGGLEABLE_TAG, hud_tag=self.tag, color_tag=difficulty.color),
                fill=difficulty.color
            )

            t_id = self.canvas.create_text(
                (x + nx) // 2, (center_y - 110 + center_y - 70) // 2,
                text=difficulty.name + "\n" + difficulty.description,
                tags=set_tags(hud_tag=self.tag) + (TEXT_TAG,),
                fill=FILL_TEXT,
                justify="center"
            )

            self.dict_difficulty[rect_id] = difficulty
            self.canvas.text_id_in_rectangle_id[t_id] = rect_id

            x = int(nx)
            self.radiobutton_difficulty.add_option(rect_id)

        # On simule un clic sur la difficulté Facile
        self.canvas.give_tag_to(rect_id, "highlight")
        self.radiobutton_difficulty.toggle_switch_option(rect_id)
        self.canvas.dtag("highlight", "highlight")

        self.canvas.create_text(
            center_x, center_y - 40, tags=set_tags(hud_tag=self.tag),
            text="Choisissez une couleur ou on choisira pour vous.",
            fill=FILL_TEXT
        )

        x = int(center_x * 0.25)
        xstep = int(center_x * 1.5) // len(Vassal.couleurs)
        for couleur in Vassal.couleurs:
            nx = x + xstep
            rect_id = self.canvas.create_rectangle(
                x,
                center_y + 20,
                nx,
                center_y - 20,
                tags=set_tags(TOGGLEABLE_TAG, hud_tag=self.tag, color_tag=couleur),
                fill=couleur
            )

            x = int(nx)
            self.radiobutton_color.add_option(rect_id)

        self.canvas.add_button(
            self.tag,
            "HIDE_START_MENU",
            self.canvas.start
        ).draw(
            center_x - 60,
            center_y + 60,
            center_x + 60,
            center_y + 80,
            text="Commencer"
        )

        self.canvas.add_button(
            self.tag,
            "QUIT",
            lambda e: self.canvas.quit()
        ).draw(
            center_x - 60,
            center_y + 120,
            center_x + 60,
            center_y + 140,
            text="Sortez-moi de là"
        )

    def replace(self, *args) -> None:
        self.canvas.tag_raise(self.tag)

    def get_color_choice(self):
        if self.radiobutton_color.currently_selected is not None:
            return self.canvas.gettags(self.radiobutton_color.currently_selected)[COLOR_TAG_INDEX]

        else: return None

    def get_difficulty_choice(self):
        return self.dict_difficulty[self.radiobutton_difficulty.currently_selected].nb_nobles
