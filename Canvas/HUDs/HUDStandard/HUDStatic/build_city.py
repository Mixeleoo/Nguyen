
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance

from ..HUDHideable import HUDHideableABC
from ..HUDStaticABC import HUDStaticABC
from parameter import *

class BuildCity(HUDStaticABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.background_rect_id = 0

    @property
    def arrival_pos_show(self) -> Position: return Position(0, PADY_BUILD_CITY_HUD)
    @property
    def curr_show_pos(self) -> Position: return Position(0, self.canvas.coords(self.background_rect_id)[1])
    @property
    def arrival_pos_hide(self) -> Position: return Position(0, PADY_BUILD_CITY_HUD_HIDING)
    @property
    def curr_hide_pos(self) -> Position: return Position(0, self.canvas.coords(self.background_rect_id)[3])

    def create(self, geometry_width: int, geometry_height: int):

        text = "Choisissez une plaine où construire votre village"

        # Gros rectangle contenant les 4 rectangles d'actions
        width = get_width_text(text)
        height = 80  # valeurs qui ne bougent pas en fonction de la taille de la fenêtre

        x0_cadre = (geometry_width // 2) - (width // 2)
        x1_cadre = x0_cadre + width

        # - car on veut que ça soit affiché en dehors de l'écran
        y0_cadre = -height + PADY_BUILD_CITY_HUD_HIDING
        y1_cadre = PADY_BUILD_CITY_HUD_HIDING

        self.background_rect_id = self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre,
            fill="#cccc00",
            tags=set_tags(hud_tag=self.tag)
        )

        self.canvas.create_text(
            (x0_cadre + x1_cadre) // 2, (y0_cadre + y1_cadre) // 2,
            text=text,
            tags=set_tags(hud_tag=self.tag)
        )

        original_image = Image.open("./assets/banderoletravaux.png")

        # La largeur fait la taille du rectangle du fond
        image_width = x1_cadre - x0_cadre

        # La longueur fait 1/4 de la longueur du rectangle du fond
        image_height = (y1_cadre - y0_cadre) // 4

        # Le -1 est un ajustement pck ça dépassait d'un pixel (jsp pk)
        resized_image = original_image.resize((image_width - 1, image_height))

        enhancer = ImageEnhance.Brightness(resized_image)
        image_assombrie = enhancer.enhance(0.8)

        # Convertir l'image redimensionnée en format Tkinter
        ref = ImageTk.PhotoImage(image_assombrie)

        # Le +1 est un ajustement pck ça dépassait d'un pixel (jsp pk)
        # Image d'en haut
        self.canvas.create_image(
            image_width // 2 + x0_cadre + 1, image_height // 2 + y0_cadre + 1,
            image=ref, tags=set_tags(hud_tag=self.tag)
        )

        # Image d'en bas
        self.canvas.create_image(
            image_width // 2 + x0_cadre + 1, -image_height // 2 + y1_cadre,
            image=ref, tags=set_tags(hud_tag=self.tag)
        )

        self.canvas.references += [ref]

        # Juste pour le côté graphique
        self.canvas.create_line(
            x0_cadre, y0_cadre + image_height, x1_cadre, y0_cadre + image_height, tags=set_tags(hud_tag=self.tag)
        )

        # Juste pour le côté graphique
        self.canvas.create_line(
            x0_cadre, y1_cadre - image_height, x1_cadre, y1_cadre - image_height, tags=set_tags(hud_tag=self.tag)
        )

        self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.cancel
        )

    def replace(self, event: tk.Event) -> None:
        bbox = self.bbox()
        if bbox is not None:
            dx = self.canvas.master.winfo_width() // 2 - (bbox[2] + bbox[0]) // 2

            self.canvas.move(self.tag, dx, 0)

    def cancel(self, e=None):
        HUDHideableABC.show_all_hidden()

        self.hide_animation()
        self.canvas.game_mode = "basic"
