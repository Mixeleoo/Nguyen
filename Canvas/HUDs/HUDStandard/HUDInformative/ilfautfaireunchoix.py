
from PIL import Image, ImageTk, ImageEnhance

from Canvas.HUDs.HUDStandard.HUDInformative.base import HUDInformativeABC
from Canvas.hud_canvas import HUDCanvas
from parameter import *

class IlFautFaireUnChoix(HUDInformativeABC):
    def __init__(self, canvas: HUDCanvas):
        super().__init__(canvas)

    def create(self) -> None:

        text = "Il faut faire un choix"

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