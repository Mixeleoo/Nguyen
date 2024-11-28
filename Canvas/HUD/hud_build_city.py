import tkinter as tk

from PIL import Image, ImageTk, ImageEnhance

from parameter import *
from Canvas.HUD.HUDABC import HUDABC

class HUDBuildCity(HUDABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.background_rect_id = 0

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
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.cancel,
            trigger_name=CANCEL_BUILD_CITY_TAG
        )

    def replace(self, event: tk.Event) -> None:
        pass

    def show_animation(self):
        self.canvas.move(self.tag, 0,
                        abs(PADY_BUILD_CITY_HUD - self.canvas.coords(self.background_rect_id)[1]) // 10 + 1)

        if self.canvas.coords(self.background_rect_id)[1] != PADY_BUILD_CITY_HUD:
            self.canvas.after(DELTA_MS_ANIMATION, self.show_animation)

    def hide_animation(self):
        self.canvas.move(self.tag, 0, -(abs(PADY_BUILD_CITY_HUD_HIDING - self.canvas.coords(self.background_rect_id)[3]) // 10 + 1))

        if self.canvas.coords(self.background_rect_id)[3] != PADY_BUILD_CITY_HUD_HIDING:
            self.canvas.after(DELTA_MS_ANIMATION, self.hide_animation)

    def choose_plain_to_build(self, event: tk.Event):
        """
        Uniquement s'il y a la possibilité, on cache les HUD, et on affiche le texte disant : Où voulez-vous construire
        votre village ? Passage en mode citybuilding mgl
        """
        # On eclairci la zone
        self.canvas.hide_all_permanant_huds()

        # On affiche le rectangle de construction
        self.show_animation()

        self.canvas.game_mode = "build_city"

    def cancel(self, e=None):
        self.canvas.show_hidden_permanant_huds()

        self.hide_animation()
        self.canvas.game_mode = "basic"

    def build_city_on_plain(self, event: tk.Event):
        """
        Cette fonction crée un village si le joueur clique sur une plaine qui n'a pas de villages aux alentours.
        Elle affiche également les HUD qui étaient précédemment affichés avant de construire le village.
        """
        # Modifier la case en village
        square_id = self.canvas.find_withtag("active")[0]
        village_around_id = self.canvas.villages_around(square_id)

        if village_around_id:
            self.canvas.hudmobile_yavillagegros.show(village_around_id)

        else:
            # Même comportement que si on annulait la construction, sauf que là, on construit
            self.cancel()

            tags = list(self.canvas.gettags(square_id))

            # Comme il y a un nouveau village, il faut update l'HUD qui permet de choisir le village
            new_option_id = self.canvas.hud_choose_village.add_village_update_HUD("village 2")
            self.canvas.radiobuttons.add_option(tags[GROUP_TAG_INDEX], new_option_id)

            # On change son tag de trigger de fonction
            tags[TRIGGER_TAG_INDEX] = VILLAGE_TAG
            self.canvas.itemconfigure(square_id, fill="orange", tags=tags)
