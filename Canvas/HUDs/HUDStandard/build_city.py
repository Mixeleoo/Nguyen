
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance

from .base import HUDABC
from parameter import *

class BuildCity(HUDABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.background_rect_id = 0

    @property
    def tag(self):
        return HUD_BUILD_CITY

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
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.cancel
        )

    def replace(self, event: tk.Event) -> None:
        pass

    def choose_plain_to_build(self, event: tk.Event):
        """
        Uniquement s'il y a la possibilité, on cache les HUDs, et on affiche le texte disant : Où voulez-vous construire
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
        Elle affiche également les HUDs qui étaient précédemment affichés avant de construire le village.
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

            # Comme il y a un nouveau village, il faut update les HUDs qui permet de choisir le village
            nom = nom_aleatoire_village()
            self.canvas.hudmobile_choose_village.add_option(nom, square_id)
            self.canvas.hudmobile_choose_taxes.add_village(nom, square_id)

            # On lance la méthode qui influera sur le jeu
            self.canvas.jeu.construire_village(village_id=square_id, nom=nom)

            # On change son tag de trigger de fonction
            self.canvas.engine_build_city(square_id, tags)

            # On affiche dans l'historique son action
            self.canvas.hud_history.add_text("Le joueur a crée un village !")
