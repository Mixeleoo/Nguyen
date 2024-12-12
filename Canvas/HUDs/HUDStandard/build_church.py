
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance

from .base import HUDABC
from parameter import *

class BuildChurch(HUDABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.background_rect_id = 0

    @property
    def tag(self): return HUD_BUILD_CHURCH

    @property
    def arrival_pos_show(self) -> Position: return Position(0, PADY_BUILD_CITY_HUD)
    @property
    def curr_show_pos(self) -> Position: return Position(0, self.canvas.coords(self.background_rect_id)[1])
    @property
    def arrival_pos_hide(self) -> Position: return Position(0, PADY_BUILD_CITY_HUD_HIDING)
    @property
    def curr_hide_pos(self) -> Position: return Position(0, self.canvas.coords(self.background_rect_id)[3])

    def create(self, geometry_width: int, geometry_height: int):

        text = "Choisissez un village où construire votre Église"

        # Gros rectangle contenant les 4 rectangles d'actions
        width = get_width_text(text)
        height = 80  # valeurs qui ne bougent pas en fonction de la taille de la fenêtre

        x0_cadre = (geometry_width // 2) - (width // 2)
        x1_cadre = x0_cadre + width

        # - car on veut que ça soit affiché en dehors de l'écran
        y0_cadre = - height + PADY_BUILD_CITY_HUD_HIDING
        y1_cadre = PADY_BUILD_CITY_HUD_HIDING

        self.background_rect_id = self.canvas.create_rectangle(x0_cadre, y0_cadre, x1_cadre, y1_cadre,
                              fill="#cccc00", tags=set_tags(hud_tag=self.tag))

        original_image = Image.open("./assets/eglise vitrail.png")

        # Le -1 est un ajustement pck ça dépassait d'un pixel (jsp pk)
        resized_image = original_image.resize((width, height))

        enhancer = ImageEnhance.Brightness(resized_image)
        image_assombrie = enhancer.enhance(0.8)

        # Convertir l'image redimensionnée en format Tkinter
        ref = ImageTk.PhotoImage(image_assombrie)

        # Le +1 est un ajustement pck ça dépassait d'un pixel (jsp pk)
        # Image d'en haut
        self.canvas.create_image(
            (x0_cadre + x1_cadre) // 2, (y0_cadre + y1_cadre) // 2,
            image=ref, tags=set_tags(hud_tag=self.tag)
        )

        self.canvas.create_text(
            (x0_cadre + x1_cadre) // 2, (y0_cadre + y1_cadre) // 2,
            text=text,
            tags=set_tags(hud_tag=self.tag),
            fill="white"
        )

        self.canvas.references += [ref]

        self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.cancel
        )

    def replace(self, event: tk.Event) -> None:
        pass

    def cancel(self, e=None):
        self.canvas.show_hidden_permanant_huds()

        self.hide_animation()
        self.canvas.game_mode = "basic"