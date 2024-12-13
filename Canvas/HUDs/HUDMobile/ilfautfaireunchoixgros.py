
from PIL import Image, ImageTk, ImageEnhance

from .base import HUDMobileABC
from parameter import *

class IlFautFaireUnChoixGros(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.id = 0
        self.after_hide_id = None

    @property
    def tag(self):
        return "IlFautFaireUnChoixGros"

    def create(self) -> None:

        text = "Il faut faire un choix gros"

        width = get_width_text(text)
        height = 20

        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = width
        y1_cadre = height

        self.id = self.canvas.create_text_in_rectangle(
            x0=x0_cadre,
            y0=y0_cadre,
            x1=x1_cadre,
            y1=y1_cadre,
            rectangle_tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            text=text,
            state="hidden"
        )

        original_image = Image.open("./assets/pointing-hand.png")

        # La longueur fait 1/4 de la longueur du rectangle du fond
        image_height = int(y1_cadre - y0_cadre)

        # La largeur fait la taille du rectangle du fond (produit en croix pour garder le ratio de l'ancienne taille)
        image_width = image_height * original_image.width // original_image.height

        # Le -1 est un ajustement pck ça dépassait d'un pixel (jsp pk)
        resized_image = original_image.resize((image_width - 1, image_height))

        enhancer = ImageEnhance.Brightness(resized_image)
        image_assombrie = enhancer.enhance(0.8)

        # Convertir l'image redimensionnée en format Tkinter
        ref = ImageTk.PhotoImage(image_assombrie)

        # Le +1 est un ajustement pck ça dépassait d'un pixel (jsp pk)
        # Image d'en haut
        self.canvas.create_image(
            x0_cadre - ref.width() // 2 - 1, image_height // 2 + y0_cadre + 1,
            image=ref, tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,), state="hidden"
        )

        self.canvas.references += [ref]

    def replace(self, x0: float, y0: float) -> None:

        dx = x0 - self.canvas.coords(self.id)[0]
        dy = y0 - self.canvas.coords(self.id)[1]

        self.canvas.move(self.tag, dx, dy)

        # On cache après trois seconde
        if self.after_hide_id is not None:
            self.canvas.after_cancel(self.after_hide_id)

        self.after_hide_id = self.canvas.after(3000, self.bhide)

    def show(self, x0: float, y0: float) -> None: super().show(x0, y0)

    def bhide(self):
        self.after_hide_id = None
        self.hide()
