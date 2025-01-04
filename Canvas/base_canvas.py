
import tkinter as tk
import random
from typing import Literal

from parameter import *
from Canvas.create_biome_map import create_biome_map

class BaseCanvas(tk.Canvas):
    def __init__(self, master=None, cnf=None, **kw):
        # C'est PyCharm qui me dit de mettre ça au lieu de cnf={} directement dans les arguments donc...
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        from jeu import Jeu

        # On instancie le jeu
        self.jeu = Jeu()

        self.custom_font = font.Font(family="Enchanted Land", size=20)
        self.references = []
        self.square_id_to_tag: dict[int, str] = {}

        self.basic_mode_tag_foc: [str, callable] = {}
        self.build_city_mode_tag_foc: [str, callable] = {}
        self.build_church_mode_tag_foc: [str, callable] = {}
        self.tutoriel_mode_tag_foc: [str, callable] = {}

        self.tag_foc = {
            "basic": self.basic_mode_tag_foc,
            "build_city": self.build_city_mode_tag_foc,
            "build_church": self.build_church_mode_tag_foc,
            "tutorial": self.tutoriel_mode_tag_foc
        }

        self.tag_fod: [str, callable] = {}

        self.mouse_coor = ()
        self.font = tk.font.nametofont("TkDefaultFont")
        self.font.config(size=11)

        # Vairblae test
        self.id_village = 0

        from Canvas.Widget.Radiobutton import SelectorSupervisor

        self.radiobuttons = SelectorSupervisor(self)
        self.add_radiobutton = self.radiobuttons.add_radiobutton
        self.add_checkbutton = self.radiobuttons.add_checkbutton

        """
                                                HIGHLIGHT
        """

        self.highlight_tag_on_click = {
            MAP_TAG: self.highlight_square,
            CLICKABLE_TAG: self.highlight_clickable,
            DRAGGABLE_TAG: self.highlight_clickable,
            TOGGLEABLE_TAG: self.highlight_toggleable,
            HIGHLIGHT_BUTTON_TAG: self.highlight_button,
            NOTHING_TAG: dummy
        }

        self.highlight_tag_on_drag = {
            MAP_TAG: self.unhighlight_square,
            CLICKABLE_TAG: self.unhighlight_clickable,
            DRAGGABLE_TAG: dummy,
            TOGGLEABLE_TAG: dummy,
            HIGHLIGHT_BUTTON_TAG: self.unhighlight_button,
            NOTHING_TAG: dummy
        }

        self.highlight_tag_on_release = {
            MAP_TAG: self.unhighlight_square,
            CLICKABLE_TAG: self.unhighlight_clickable,
            DRAGGABLE_TAG: self.unhighlight_clickable,
            TOGGLEABLE_TAG: dummy,
            HIGHLIGHT_BUTTON_TAG: self.unhighlight_button,
            NOTHING_TAG: dummy
        }

        # Cette variable repertoriera tous les id de texts et leur rectangle associé.
        # ça permet de savoir, quand on veut highlight un rectangle après avoir cliqué sur un texte,
        # sur quel rectangle est le texte
        self.text_id_in_rectangle_id = {

        }

        # Comme le dictionnaire qui sert à récupérer le rectangle depuis le texte et inversement. Celui-ci servira
        # à récupérer l'id du rectangle du fond à partir du rectangle par dessus (pour l'highlight du bouton)
        self.get_rect_border_id_from_inner_id = {

        }

    def give_tag_to(self, item_id: int, tag: str, tag_index: int = -1):
        tags = list(self.gettags(item_id))
        if tag_index == -1:
            tags.append(tag)

        else:
            tags[tag_index] = tag

        self.itemconfigure(item_id, tags=tags)

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
            if "drag_corner" == self.gettags(item)[DRAG_TAG_INDEX][:11]:
                id_rectangle = item

        self.addtag_withtag("active", id_rectangle)
        self.addtag_withtag("highlight", id_rectangle)

    def create_text_in_rectangle(self, x0: int | float, y0: int | float, x1: int | float, y1: int | float, text: str,
                                 rectangle_tags: tuple[str], text_tags: tuple[str],
                                 fill: str=FILL_ACTION_BOX, text_font: tk.font.Font=None,
                                 state: Literal["normal", "hidden", "disabled"] = "normal",
                                 outline: str="black", justify: Literal["left", "center", "right"] = "left", radius: int = 20) -> int:
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
            state=state,
            outline=outline
        )

        id_text = self.create_text(
            (x0 + x1) // 2, (y0 + y1) // 2,
            text=text,
            font=text_font,
            tags=text_tags,
            state=state,
            fill=FILL_TEXT,
            justify=justify
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

                self.square_id_to_tag[square_id] = which_type

                # Pour débug les carrés
                # self.create_text((self.sps * row_i + self.sps * (row_i + 1)) / 2, (self.sps * col_i + self.sps * (col_i + 1)) / 2, content=f"{row_i, col_i}")

                all_squares_id += [square_id]

                x0 = x1
                x1 += SPS

            y0 = y1
            y1 += SPS

        self.addtag(MAP_SQUARE_TOP_LEFT_TAG, "withtag", all_squares_id[0])
        self.addtag(MAP_SQUARE_BOTTOM_RIGHT_TAG, "withtag", all_squares_id[-1])

    def engine_build_city(self, square_id: int=None, tags: tuple | list=None) -> int:
        """
        Méthode qui créera un village en fonction des paramètres
        """

        if square_id is None:
            square_id = random.choice(self.find_withtag(PLAINE_TAG))
            while self.villages_around(square_id):
                square_id = random.choice(self.find_withtag(PLAINE_TAG))
            tags = list(self.gettags(square_id))

        # Configurer les villages concernés
        tags[TRIGGER_TAG_INDEX] = VILLAGE_TAG
        tags.insert(GROUP_TAG_INDEX, f"pvillage_{self.id_village}")
        self.id_village += 1

        self.itemconfigure(square_id, tags=tags)

        return square_id

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

    def new_trigger(self, tag: str, func: callable, which_game_mode: tuple[str] = ("basic", "build_city", "build_church")):
        """
        Méthode pour généraliser la création de nouveaux comportements d'highlight.
        """

        # Pour chaque mode de jeu existant
        for game_mode in ("basic", "build_city", "build_church", "tutorial"):

            # Si la fonction est censée être trigger durant ce mode de jeu
            if game_mode in which_game_mode:

                # Si le nom du trigger apparaît dores et déjà dans le dictionnaire, c'est pas bon
                if tag in game_mode:
                    raise TypeError(
                        f"{tag} a déjà une fonction attribuée dans le mode de jeu {game_mode}.")

                else:
                    self.tag_foc[game_mode][tag] = func

    """
                                        HIGHLIGHT
    """

    def highlight_square(self, toward_coor: tuple = None):
        """
        J'aimerai que le carré se raptessisse, jusqu'à être de moitié de la taille initiale, mais progressivement
        :return:
        """
        coords = tuple(self.coords("highlight"))
        if not coords:
            return

        x0, y0, x1, y1 = coords
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)

        if not toward_coor:
            # Facteur de rapetissage
            k = 0.7
            center_x = int(x0 + x1) >> 1
            center_y = int(y0 + y1) >> 1

            new_x0 = int(center_x - (center_x - x0) * k)
            new_y0 = int(center_y - (center_y - y0) * k)

            # Sans le + 1 c'est disproportionné c'est bizarre
            new_x1 = int(center_x + (x1 - center_x) * k) + 1
            new_y1 = int(center_y + (y1 - center_y) * k) + 1
            toward_coor = (new_x0, new_y0, new_x1, new_y1)

        self.coords(
            "highlight",
            abs(toward_coor[0] - x0) // 2 + 1 + x0,
            abs(toward_coor[1] - y0) // 2 + 1 + y0,
            -(abs(toward_coor[2] - x1) // 2 + 1) + x1,
            -(abs(toward_coor[3] - y1) // 2 + 1) + y1
        )

        """self.coords(
            "active",
            (toward_coor[0] + x0) // 2 + 1,
            (toward_coor[1] + y0) // 2 + 1,
            (toward_coor[2] + x1) // 2 + 1,
            (toward_coor[3] + y1) // 2 + 1
        )"""

        if coords != toward_coor:
            self.after(DELTA_MS_ANIMATION, self.highlight_square, toward_coor)

    def unhighlight_square(self):
        """
        On récupère les coordonnées du carré au dessus, et grâce à ça on sait où placer le carré sélectionné
        :return:
        """
        # Si un carré est tout en haut est cliqué, alors prendre le carré d'en dessous
        id_carre_clicked = self.find_withtag("highlight")[0]

        if id_carre_clicked <= CARRE_PAR_LIGNE:
            # Carré du dessous
            x0, y0, x1, y1 = self.coords(id_carre_clicked + CARRE_PAR_LIGNE)
            self.coords("highlight", x0, y0 - SPS, x1, y0)

        else:
            # Coordonnées du carré au dessus, et on rajoute juste 50 aux ordonnées pour le placer en dessous
            x0, y0, x1, y1 = self.coords(id_carre_clicked - CARRE_PAR_LIGNE)
            self.coords("highlight", x0, y1, x1, y1 + SPS)

        self.dtag("highlight", "highlight")

    def highlight_clickable(self):
        color_tag = self.gettags("highlight")[COLOR_TAG_INDEX]
        if color_tag in fill_brighter:
            self.itemconfigure("highlight", fill=fill_brighter[color_tag])
        else:
            self.itemconfigure("highlight", fill=eclaircir_couleur(color_tag, 0.2))

    def unhighlight_clickable(self): self.itemconfigure("highlight", fill=self.gettags("highlight")[COLOR_TAG_INDEX])
    def highlight_toggleable(self): self.radiobuttons.toggle_switch_option(self.gettags("highlight")[GROUP_TAG_INDEX], self.find_withtag("highlight")[0])

    def highlight_button(self):
        """
        Méthode qui va être trigger lors de l'highlight du bouton
        """
        self.itemconfig(self.get_rect_border_id_from_inner_id[self.find_withtag("highlight")[0]], outline="#CCCCCC")     # Bord éclairé
        self.itemconfig("highlight", outline="grey")       # Bord interne clair
        self.itemconfigure("highlight", fill=self.gettags("highlight")[COLOR_TAG_INDEX])

    def unhighlight_button(self):
        """
        Méthode qui va être trigger lors de l'unhighlight du bouton
        """
        self.itemconfig(self.get_rect_border_id_from_inner_id[self.find_withtag("highlight")[0]], outline="darkgrey")  # Bord plus sombre
        self.itemconfig("highlight", outline="black")      # Bord interne foncé
        self.itemconfig("highlight", fill=fill_brighter[self.gettags("highlight")[COLOR_TAG_INDEX]])      # Bord interne foncé

    def new_highlight(self, tag: str, on_click: callable=dummy, on_drag: callable=dummy, on_release: callable=dummy):
        """
        Méthode pour généraliser la création de nouveaux comportements d'highlight.
        """
        self.highlight_tag_on_click[tag] = on_click
        self.highlight_tag_on_drag[tag] = on_drag
        self.highlight_tag_on_release[tag] = on_release
