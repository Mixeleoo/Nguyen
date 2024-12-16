
from PIL import Image, ImageTk
import tkinter as tk

from .base import HUDABC
from parameter import *
from ...Widget.StringVar import StringVar


class Event(HUDABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.ok_button_id = 0
        self._text = StringVar(self.canvas)

    @property
    def arrival_pos_show(self) -> Position: return Position(0, PADY_BUILD_CITY_HUD)
    @property
    def curr_show_pos(self) -> Position: return Position(0, self.canvas.bbox(self.tag)[1])
    @property
    def arrival_pos_hide(self) -> Position: return Position(0, PADY_BUILD_CITY_HUD_HIDING - 20)
    @property
    def curr_hide_pos(self) -> Position: return Position(0, self.canvas.coords(self.ok_button_id)[3])

    def create(self, geometry_width: int, geometry_height: int):

        # Gros rectangle contenant les 4 rectangles d'actions
        width = 500
        height = HEIGHT_EVENT  # valeurs qui ne bougent pas en fonction de la taille de la fenêtre

        x0_cadre = (geometry_width // 2) - (width // 2)
        x1_cadre = x0_cadre + width

        # - car on veut que ça soit affiché en dehors de l'écran
        y0_cadre = - height + PADY_BUILD_CITY_HUD_HIDING
        y1_cadre = PADY_BUILD_CITY_HUD_HIDING

        original_image = Image.open("./assets/parchemin.png").convert("RGBA")

        # La largeur fait la taille du rectangle du fond
        image_width = x1_cadre - x0_cadre + 150

        # La longueur fait 1/4 de la longueur du rectangle du fond
        image_height = (y1_cadre - y0_cadre) + 50

        # Le -1 est un ajustement pck ça dépassait d'un pixel (jsp pk)
        resized_image = original_image.resize((image_width - 1, image_height))

        # Convertir l'image redimensionnée en format Tkinter
        ref = ImageTk.PhotoImage(resized_image)

        self.canvas.references += [ref]

        # Le +1 est un ajustement pck ça dépassait d'un pixel (jsp pk)
        # Image d'en haut
        self.canvas.create_image((x0_cadre + x1_cadre) // 2, (y0_cadre + y1_cadre) // 2, image=ref,
                          tags=set_tags(hud_tag=self.tag), anchor=tk.CENTER)

        self._text.id = self.canvas.create_text(
            (x0_cadre + x1_cadre) // 2, (y0_cadre + y1_cadre) // 2, text="EVENEMENT TITRE",
            tags=set_tags(hud_tag=self.tag), font=self.canvas.custom_font
        )

        # Ok bouton
        self.ok_button_id = self.canvas.create_ok_button(
            x1_cadre + 10, y1_cadre, hud_tag=self.tag, func_triggered=self.hide_animation
        ).id


        # More info bouton
        self.canvas.create_text_in_rectangle(
            x1_cadre - 15, y0_cadre - 10, x1_cadre + 15, y0_cadre + 10, "i", fill=FILL_INFO,
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG,),
            rectangle_tags=set_tags(CLICKABLE_TAG, INFO_EVENT_TAG, color_tag=FILL_INFO, hud_tag=self.tag)
        )

        self.canvas.new_trigger(
            INFO_EVENT_TAG,
            self.canvas.hudmobile_more_info_event.show
        )

    def replace(self, event: tk.Event) -> None:
        pass

    def set_text(self, content: str):
        self._text.set(content)
