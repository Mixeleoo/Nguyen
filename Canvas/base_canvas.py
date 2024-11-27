
import tkinter as tk
import random
from typing import Literal

from parameter import *
from Canvas.create_biome_map import create_biome_map
from Canvas.highlight_canvas import HighlightCanvas

class BaseCanvas(HighlightCanvas):
    def __init__(self, master=None, cnf=None, **kw):
        # C'est PyCharm qui me dit de mettre ça au lieu de cnf={} directement dans les arguments donc...
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        self.custom_font = font.Font(family="Enchanted Land", size=20)
        self.references = []

        self.basic_mode_tag_foc = {}
        self.build_city_mode_tag_foc = {}
        self.build_church_mode_tag_foc = {}

        self.tag_foc = {
            "basic": self.basic_mode_tag_foc,
            "build_city": self.build_city_mode_tag_foc,
            "build_church": self.build_church_mode_tag_foc
        }

    def give_active_tag(self, event: tk.Event) -> None:
        """
        Si le current est un texte, alors on donne le tag "active" au rectangle en dessous
        Sinon on donne tout simplement le tag "active" sur ce quoi on a cliqué
        :return:
        """
        # Définir quel rectangle est actif
        id_rectangle = "current"

        # Si c'est un texte, alors c'est le ctangle associé qui devient actif
        if TEXT_TAG in self.gettags("current"):
            # On récupère l'id du rectangle sur lequel le texte est, pour ça :
            # On récupère son deuxième tag, sur lequel est inscrit _{id_rectangle}
            # id_rectangle étant le rectangle sur lequel le texte est.

            id_rectangle = self.text_id_in_rectangle_id[self.find_withtag("current")[0]]

        # On vérifie pour chaque item qui se chevauche à l'endroit clické
        for item in self.find_overlapping(event.x, event.y, event.x, event.y):

            # S'il y a le rectangle de drag sous la souris, alors on rend le rectangle qui gère tout ça sous la souris.
            if DRAG_CORNER_MORE_INFO_WINDOW_TAG in self.gettags(item):
                id_rectangle = item

        self.addtag_withtag("active", id_rectangle)
        self.addtag_withtag("highlight", id_rectangle)

    def create_text_in_rectangle(self, x0: int | float, y0: int | float, x1: int | float, y1: int | float, text: str,
                                 rectangle_tags: tuple[str], text_tags: tuple[str],
                                 fill: str=FILL_ACTION_BOX, text_font: tk.font.Font=None,
                                 state: Literal["normal", "hidden", "disabled"] = "normal", radius: int = 20) -> int:
        """
        On va faire apparaître le rectangle d'action pour un carré, avant ça, il faut savoir où le placer
        La plus part du temps, ça sera sur la droite de la souris, le menu déroulant s'étalant sur le bas
        Mais si on clique sur un carré tout en bas, le rectangle devra s'étaler sur le haut
        Et si on clique sur un carré tout à droite, le rectangle devra se placer sur la gauche de la souris

        retourne l'id du rectangle puis l'id du texte
        """
        # Dessiner les arcs concaves aux coins du rectangle
        """self.create_arc(x0, y0, x0 + 2 * radius, y0 + 2 * radius, start=90, extent=90, fill=FILL_ACTION_BOX,
                          outline="", tags=(HUD_TAG,) + additional_rectangle_tag, width=0)  # Coin supérieur gauche
        self.create_arc(x1 - 2 * radius, y0, x1, y0 + 2 * radius, start=0, extent=90, fill=FILL_ACTION_BOX,
                          outline="", tags=(HUD_TAG,) + additional_rectangle_tag, width=0)  # Coin supérieur droit
        self.create_arc(x1 - 2 * radius, y1 - 2 * radius, x1, y1, start=270, extent=90, fill=FILL_ACTION_BOX,
                          outline="", tags=(HUD_TAG,) + additional_rectangle_tag, width=0)  # Coin inférieur droit
        self.create_arc(x0, y1 - 2 * radius, x0 + 2 * radius, y1, start=180, extent=90, fill=FILL_ACTION_BOX,
                          outline="", tags=(HUD_TAG,) + additional_rectangle_tag, width=0)  # Coin inférieur gauche

        # Dessiner les côtés du rectangle (sans les coins)
        self.create_rectangle(x0 + radius, y0, x1 - radius, y0 + radius + 1, fill=FILL_ACTION_BOX, tags=(HUD_TAG,) + additional_rectangle_tag, width=0)  # Côté supérieur
        self.create_rectangle(x1 - radius, y0 + radius, x1 + 1, y1 - radius, fill=FILL_ACTION_BOX, tags=(HUD_TAG,) + additional_rectangle_tag, width=0)  # Côté droit
        self.create_rectangle(x0 + radius, y1 - radius, x1 - radius, y1 + 1, fill=FILL_ACTION_BOX, tags=(HUD_TAG,) + additional_rectangle_tag, width=0)  # Côté inférieur
        self.create_rectangle(x0, y0 + radius, x0 + radius, y1 - radius, fill=FILL_ACTION_BOX, tags=(HUD_TAG,) + additional_rectangle_tag, width=0)  # Côté gauche

        # Rectangle central
        id_rectangle = self.create_rectangle(x0 + radius, y0 + radius, x1 - radius, y1 - radius, fill=FILL_ACTION_BOX, tags=(HUD_TAG,) + additional_rectangle_tag, width=0)  # Côté gauche
        """
        if text_font == None:
            text_font = tk.font.nametofont("TkDefaultFont")

        id_rectangle = self.create_rectangle(
            x0, y0, x1, y1,
            fill=fill,
            tags=rectangle_tags,
            state=state
        )

        id_text = self.create_text(
            (x0 + x1) // 2, (y0 + y1) // 2,
            text=text,
            font=text_font,
            tags=text_tags,
            state=state
        )

        self.text_id_in_rectangle_id[id_text] = id_rectangle
        self.text_id_in_rectangle_id[id_rectangle] = id_text
        return id_rectangle

    def generate_game_grid(self, geometry: tuple[int]):
        """
        Fonction de génération de la carte, par biome, disposés aléatoirement, de taille limitée.
        """
        all_squares_id = []
        map_grid = create_biome_map(geometry[0], geometry[1])

        y0 = 0
        y1 = SPS
        for row_i in range(geometry[0]):
            x0 = 0
            x1 = SPS
            for col_i in range(geometry[1]):
                which_type = map_grid[row_i][col_i]
                square_id = self.create_rectangle(
                    x0, y0, x1, y1,
                    fill=couleurs[which_type](),
                    tags=set_tags(MAP_TAG, which_type if which_type == PLAINE_TAG else NOTHING_TAG, MAP_TAG),
                    width=0
                )

                # Pour débug les carrés
                # self.create_text((self.sps * row_i + self.sps * (row_i + 1)) / 2, (self.sps * col_i + self.sps * (col_i + 1)) / 2, text=f"{row_i, col_i}")

                all_squares_id += [square_id]

                x0 = x1
                x1 += SPS

            y0 = y1
            y1 += SPS

        # Ajout des villages aléatoirement
        for noble in range(NB_NOBLE_AU_DEPART):
            square_id = random.choice(self.find_withtag(PLAINE_TAG))
            while self.villages_around(square_id):
                square_id = random.choice(self.find_withtag(PLAINE_TAG))

            tags = list(self.gettags(square_id))
            tags[TRIGGER_TAG_INDEX] = VILLAGE_TAG
            tags.insert(GROUP_TAG_INDEX, f"pvillage_{noble}")
            self.itemconfigure(square_id, fill="orange", tags=tags)

        self.addtag(MAP_SQUARE_TOP_LEFT_TAG, "withtag", all_squares_id[0])
        self.addtag(MAP_SQUARE_BOTTOM_RIGHT_TAG, "withtag", all_squares_id[-1])

    def villages_around(self, square_id: int):
        village_id = 0

        deux_lignes = CARRE_PAR_LIGNE << 1
        for square_around_id in [
            -CARRE_PAR_LIGNE - 2, -CARRE_PAR_LIGNE - 1, -CARRE_PAR_LIGNE, -CARRE_PAR_LIGNE + 1, -CARRE_PAR_LIGNE + 2,
            CARRE_PAR_LIGNE - 2, CARRE_PAR_LIGNE - 1, CARRE_PAR_LIGNE, CARRE_PAR_LIGNE + 1, CARRE_PAR_LIGNE + 2,
            -deux_lignes - 2, -deux_lignes - 1, -deux_lignes, -deux_lignes + 1, -deux_lignes + 2,
            deux_lignes - 2, deux_lignes - 1, deux_lignes, deux_lignes + 1, deux_lignes + 2,
            1, -1, -2, 2]:
            if self.gettags(square_id + square_around_id) and self.gettags(square_id + square_around_id)[TRIGGER_TAG_INDEX] == VILLAGE_TAG:
                village_id = square_id + square_around_id

        return village_id

    def create_button(self, x0: int | float, y0: int | float, x1: int | float, y1: int | float, text: str,
                      hud_tag: str, func_triggered: callable = None, fill: str=FILL_ACTION_BOX,
                      state: Literal["normal", "hidden", "disabled"] = "normal",
                      trigger_name: str = NOTHING_TAG, is_temp: bool = False,
                      for_which_game_mode: tuple[Literal["basic", "build_city", "build_church"]] = ("basic", "build_city", "build_church")):
        """
        Méthode qui créerera un texte sur un rectangle, qui agira comme un bouton :
        - Il est clickable (highlight)
        - Trigger une fonction lorsque clické dessus (trigger_name)
        - Peut être temporaire (is_temp)
        """

        if_temp = (TEMP_TAG,) if is_temp else tuple()

        if func_triggered:
            for game_mode in for_which_game_mode:
                if trigger_name in game_mode:
                    raise TypeError(f"{trigger_name} a déjà une fonction attribuée dans le mode de jeu {game_mode}.")

                else:
                    self.tag_foc[game_mode][trigger_name] = func_triggered

        return self.create_text_in_rectangle(
            x0, y0, x1, y1,
            text=text,
            rectangle_tags=set_tags(CLICKABLE_TAG, trigger_name, color_tag=fill, group_tag=hud_tag) + if_temp,
            text_tags=set_tags() + (TEXT_TAG,) + if_temp, fill=fill, state=state
        )
