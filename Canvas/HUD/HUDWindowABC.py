
import tkinter as tk
from abc import ABC, abstractmethod

from parameter import *
from Canvas.HUD.HUDMobileABC import HUDMobileABC


class HUDWindowABC(HUDMobileABC, ABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        # Liste des coins permettant de pouvoir agrandir la fenêtre
        self.drag_corners = []

        self.item_text_id = 0
        self._text = ""

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.canvas.itemconfigure(self.item_text_id, text=value)

    def create(self):

        width = 200
        height = 100

        x0_cadre = 100
        y0_cadre = 100
        x1_cadre = x0_cadre + width
        y1_cadre = y0_cadre + height

        # Gros rectangle contenant toutes les infos
        self.item_text_id = self.canvas.create_text_in_rectangle(
            x0=x0_cadre, y0=y0_cadre + 20, x1=x1_cadre, y1=y1_cadre,
            fill=FILL_ACTION_BOX,
            text=self.text,
            rectangle_tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden"
        )

        # Bouton pour fermer
        self.canvas.create_text_in_rectangle(
            x0=x1_cadre - 20,
            y0=y0_cadre,
            x1=x1_cadre,
            y1=y0_cadre + 20,
            fill=FILL_CANCEL,
            text="x",
            rectangle_tags=set_tags(CLICKABLE_TAG, CLOSE_MORE_INFO_WINDOW, color_tag=FILL_CANCEL, hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG,),
            state="hidden"
        )

        # Bouton pour pin
        self.canvas.create_text_in_rectangle(
            x0=x1_cadre - 40,
            y0=y0_cadre,
            x1=x1_cadre - 20,
            y1=y0_cadre + 20,
            fill=FILL_ACTION_BOX,
            text="⌂",
            rectangle_tags=set_tags(CLICKABLE_TAG, PIN_MORE_INFO_WINDOW, hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG,),
            state="hidden"
        )

        # Rectangle pour bouger la fenêtre (en haut dcp)
        self.canvas.create_text_in_rectangle(
            x0=x0_cadre,
            y0=y0_cadre,
            x1=x1_cadre - 40,
            y1=y0_cadre + 20,
            fill=FILL_ACTION_BOX,
            rectangle_tags=set_tags(drag_tag=MOVE_WINDOW, hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG,),
            text=self.tag,
            state="hidden"
        )

        # Rectangles pour changer la taille de la fenêtre.
        # Ils sont créés dans cet ordre : En haut à gauche, en haut à droite
        # En bas à gauche, en bas à droite.
        for j in range(2):
            for i in range(2):
                item = self.canvas.create_rectangle(
                    [x0_cadre, x1_cadre][i] - 5,
                    [y0_cadre, y1_cadre][j] - 5,
                    [x0_cadre, x1_cadre][i] + 5,
                    [y0_cadre, y1_cadre][j] + 5,
                    fill=FILL_ACTION_BOX,
                    tags=set_tags(drag_tag=DRAG_CORNER_MORE_INFO_WINDOW_TAG, hud_tag=self.tag) + (TEMP_TAG,),
                    state="hidden"
                )

                self.canvas.tag_lower(item, MAP_TAG)

                self.drag_corners.append(item)

    def replace(self, *args) -> None:
        pass

    def on_drag(self, event: tk.Event):
        dx = event.x - self.canvas.mouse_coor[0]
        dy = event.y - self.canvas.mouse_coor[1]

        # Déplace tous les carrés avec le tag "square"
        self.canvas.move(self.tag, dx, dy)

    def resize(self, x0_cadre: int, y0_cadre: int, x1_cadre: int, y1_cadre: int):
        """
        Dans la fenêtre,
        la croix et le pin ne changent pas de dimension, ils bougent quand x0 ou y1 est modifié.
        Le rectangle pour mouvoir la fenêtre est à l'index 10, il n'a que y0 qui est variable pour lui.
        Le gros rectangle peut modifier toutes ses dimensions, et il est à l'index 4, (je sais pas pk c'est tkinter qui met dans cet ordre
        """
        window_items = self.canvas.find_withtag(self.tag)

        # Gros rectangle contenant toutes les infos
        self.canvas.coords(window_items[4], x0_cadre, y0_cadre + 20, x1_cadre, y1_cadre)
        self.canvas.coords(window_items[5], (x0_cadre + x1_cadre) // 2, (y0_cadre + 20 + y1_cadre) // 2)

        # Bouton pour fermer
        self.canvas.coords(window_items[6], x1_cadre - 20, y0_cadre, x1_cadre, y0_cadre + 20)
        self.canvas.coords(window_items[7], (x1_cadre - 20 + x1_cadre) // 2, (y0_cadre + y0_cadre + 20) // 2)

        # Bouton pour pin
        self.canvas.coords(window_items[8], x1_cadre - 40, y0_cadre, x1_cadre - 20, y0_cadre + 20)
        self.canvas.coords(window_items[9], (x1_cadre - 40 + x1_cadre - 20) // 2, (y0_cadre + y0_cadre + 20) // 2)

        # Rectangle pour bouger la fenêtre (en haut dcp)
        self.canvas.coords(window_items[10], x0_cadre, y0_cadre, x1_cadre - 40, y0_cadre + 20)

        # Rectangles pour changer la taille de la fenêtre.
        # Ils sont créés dans cet ordre :
        # En haut à gauche, en haut à droite
        # En bas à gauche, en bas à droite.
        k = 0
        for j in range(2):
            for i in range(2):
                self.canvas.coords(
                    window_items[k],
                    [x0_cadre, x1_cadre][i] - 5,
                    [y0_cadre, y1_cadre][j] - 5,
                    [x0_cadre, x1_cadre][i] + 5,
                    [y0_cadre, y1_cadre][j] + 5
                )
                k += 1

    def on_drag_corner_window(self, event: tk.Event):
        """
        Je veux récupérer les coordonnées de la grande fenêtre, pour la coordonnée :
        - x0, il faut la coordonnée x0 de, soit le rectangle movible, soit le grand rectangle
        - y0, il faut la coordonnée y0 de, soit les boutons, soit le rectangle movible
        - x1, il faut la coordonnée x1 de, soit le bouton cancel, soit le grand rectangle
        - y1, il faut la coordonnée y1 du grand rectangle.

        Index:
        - Rectangle movible : 10
        - Rectangle pin : 8
        - Rectangle cancel : 6
        - Grand rectangle : 4
        """

        # On récupère la place du coin
        # 0 = en haut à gauche
        # 1 = en haut à droite
        # 2 = en bas à gauche
        # 3 = en bas à droite (voir la création des coins)
        corner_nb = (self.canvas.find_withtag("active")[0] - self.drag_corners[0]) % 4

        # On prend les coordonnées du grand rectangle auquel on va remplacer son y0 qui deviendra celui des éléments
        # Au-dessus, construisant la fenêtre entière.
        coords = self.canvas.coords(self.canvas.find_withtag(self.tag)[4])
        coords[1] -= 20

        new_coords = [(event.x, event.y, coords[2], coords[3]),
                      (coords[0], event.y, event.x, coords[3]),
                      (event.x, coords[1], coords[2], event.y),
                      (coords[0], coords[1], event.x, event.y)][corner_nb]

        self.resize(*new_coords)

    def pin(self):
        if TEMP_TAG in self.canvas.gettags(self.tag):
            # On empêche d'unhighlight l'objet
            self.canvas.dtag("highlight", "highlight")

            # La fenêtre ne devient plus temporaire
            self.canvas.dtag(self.tag, TEMP_TAG)

        else:
            self.canvas.addtag_withtag(TEMP_TAG, self.tag)
