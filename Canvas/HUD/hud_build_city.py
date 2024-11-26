import tkinter as tk

from PIL import Image, ImageTk, ImageEnhance

from parameter import *
from Canvas.HUD.HUDABC import HUDABC

class HUDBuildCity(HUDABC):
    def __init__(self, canvas):
        super().__init__(canvas)

    @property
    def tag(self):
        return HUD_BUILD_CITY

    def create(self, geometry_width: int, geometry_height: int):

        text = "Choisissez une plaine où construire votre village"

        # Gros rectangle contenant les 4 rectangles d'actions
        width = get_width_text(text)
        height = 80  # valeurs qui ne bougent pas en fonction de la taille de la fenêtre

        x0_cadre = (geometry_width // 2) - (width // 2)
        x1_cadre = x0_cadre + width

        # - car on veut que ça soit affiché en dehors de l'écran
        y0_cadre = -(height + PADY_BUILD_CITY_HUD_HIDING)
        y1_cadre = -PADY_BUILD_CITY_HUD_HIDING

        self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre,
            fill="#cccc00",
            tags=set_tags() + (HUD_BIG_RECTANGLE_BUILD_CITY, HUD_BUILD_CITY,)
        )

        self.canvas.create_text(
            (x0_cadre + x1_cadre) // 2, (y0_cadre + y1_cadre) // 2,
            text=text,
            tags=set_tags() + (HUD_BUILD_CITY,)
        )

        original_image = Image.open("banderoletravaux.png")

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
            image=ref, tags=set_tags() + (HUD_BUILD_CITY,)
        )

        # Image d'en bas
        self.canvas.create_image(
            image_width // 2 + x0_cadre + 1, -image_height // 2 + y1_cadre,
            image=ref, tags=set_tags() + (HUD_BUILD_CITY,)
        )

        self.canvas.references += [ref]

        # Juste pour le côté graphique
        self.canvas.create_line(
            x0_cadre, y0_cadre + image_height, x1_cadre, y0_cadre + image_height, tags=set_tags() + (HUD_BUILD_CITY,)
        )

        # Juste pour le côté graphique
        self.canvas.create_line(
            x0_cadre, y1_cadre - image_height, x1_cadre, y1_cadre - image_height, tags=set_tags() + (HUD_BUILD_CITY,)
        )

        cancel_width = get_width_text("annuler")

        self.canvas.create_text_in_rectangle(
            x1_cadre - cancel_width + 10,
            y1_cadre - 10,
            x1_cadre + 10,
            y1_cadre + 10,
            fill=FILL_CANCEL,
            text="annuler",
            rectangle_tags=set_tags(CLICKABLE_TAG, CANCEL_BUILD_CITY_TAG, color_tag=FILL_CANCEL) + (HUD_BUILD_CITY,),
            text_tags=set_tags() + (TEXT_TAG, HUD_BUILD_CITY,)
        )

    def replace(self, event: tk.Event) -> None:
        pass

    def show_animation(self):
        self.canvas.move(self.tag, 0,
                        abs(PADY_BUILD_CITY_HUD - self.canvas.coords(HUD_BIG_RECTANGLE_BUILD_CITY)[1]) // 10 + 1)

        if self.canvas.coords(HUD_BIG_RECTANGLE_BUILD_CITY)[1] != PADY_BUILD_CITY_HUD:
            self.canvas.after(DELTA_MS_ANIMATION, self.show_animation)

    def hide_animation(self):
        self.canvas.move(self.tag, 0, -(abs(-PADY_BUILD_CITY_HUD_HIDING - self.canvas.coords(HUD_BIG_RECTANGLE_BUILD_CITY)[3]) // 10 + 1))

        if self.canvas.coords(HUD_BIG_RECTANGLE_BUILD_CITY)[3] != -PADY_BUILD_CITY_HUD_HIDING:
            self.canvas.after(DELTA_MS_ANIMATION, self.hide_animation)
