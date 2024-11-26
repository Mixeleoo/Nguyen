
import tkinter as tk

from parameter import *

class FunctionOnDragCanvas(tk.Canvas):
    def __init__(self, master=None, cnf=None, **kw):
        # C'est PyCharm qui me dit de mettre ça au lieu de cnf={} directement dans les arguments donc...
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)
        self.tag_fod = {
            MAP_TAG: self.on_drag_map,
            SCROLLBAR_TAG: self.on_drag_scrollbar,
            MOVE_WINDOW: self.on_drag_window,
            DRAG_CORNER_MORE_INFO_WINDOW_TAG: self.drag_corner_more_info_window,
            NOTHING_TAG: lambda *args: None
        }

    def on_drag_map(self, event: tk.Event):
        dx = event.x - self.mouse_coor[0]
        dy = event.y - self.mouse_coor[1]

        # Déplace tous les carrés avec le tag "square"
        self.move(MAP_TAG, dx, dy)

    def on_drag_scrollbar(self, event: tk.Event):

        dy = event.y - self.mouse_coor[1]
        rectangle_history_id = self.find_withtag(HUD_RIGHT_SIDE)[0]
        scrollbar_id = self.find_withtag(SCROLLBAR_TAG)[0]

        if self.coords(scrollbar_id)[1] + dy < self.coords(rectangle_history_id)[1] + 25 or \
            self.coords(scrollbar_id)[3] + dy > self.coords(rectangle_history_id)[3] - 25:
            dy = 0

        # Déplace tous les carrés avec le tag "square"
        self.move("active", 0, dy)

        self.drag_history_text(dy)

    def drag_history_text(self, dy: int):
        self.move(HISTORY_TEXT, 0, -dy)
        self.hide_exceeding_text()

    def hide_exceeding_text(self):
        text_history_ids = self.find_withtag(HISTORY_TEXT)
        rectangle_history_id = self.find_withtag(HUD_RIGHT_SIDE)[0]
        i = 0

        # Tous les textes en haut du rectangle deviennent hidden
        while self.coords(text_history_ids[i])[1] < self.coords(rectangle_history_id)[1] + 10:
            self.itemconfigure(text_history_ids[i], state="hidden")
            i += 1

        # Ceux au milieu on les laisse
        while self.coords(text_history_ids[i])[1] < self.coords(rectangle_history_id)[3] - 10:
            self.itemconfigure(text_history_ids[i], state="normal")
            i += 1

        # Ceux en bas du rectangle deviennent hidden
        while i < len(text_history_ids):
            self.itemconfigure(text_history_ids[i], state="hidden")
            i += 1

    def on_drag_window(self, event: tk.Event):
        dx = event.x - self.mouse_coor[0]
        dy = event.y - self.mouse_coor[1]

        # Déplace tous les carrés avec le tag "square"
        self.move(MORE_INFO_WINDOW, dx, dy)

    def replace_more_info_window(self, x0_cadre: int, y0_cadre: int, x1_cadre: int, y1_cadre: int):
        """
        Dans la fenêtre,
        la croix et le pin ne changent pas de dimension, ils bougent quand x0 ou y1 est modifié.
        Le rectangle pour mouvoir la fenêtre est à l'index 10, il n'a que y0 qui est variable pour lui.
        Le gros rectangle peut modifier toutes ses dimensions, et il est à l'index 4, (je sais pas pk c'est tkinter qui met dans cet ordre
        """
        print(x0_cadre, y0_cadre, x1_cadre, y1_cadre)
        window_items = self.find_withtag(MORE_INFO_WINDOW)

        # Gros rectangle contenant toutes les infos
        self.coords(window_items[4], x0_cadre, y0_cadre + 20, x1_cadre, y1_cadre)
        self.coords(window_items[5], (x0_cadre + x1_cadre) // 2, (y0_cadre + 20 + y1_cadre) // 2)

        # Bouton pour fermer
        self.coords(window_items[6], x1_cadre - 20, y0_cadre, x1_cadre, y0_cadre + 20)
        self.coords(window_items[7], (x1_cadre - 20 + x1_cadre) // 2, (y0_cadre + y0_cadre + 20) // 2)

        # Bouton pour pin
        self.coords(window_items[8], x1_cadre - 40, y0_cadre, x1_cadre - 20, y0_cadre + 20)
        self.coords(window_items[9], (x1_cadre - 40 + x1_cadre - 20) // 2, (y0_cadre + y0_cadre + 20) // 2)

        # Rectangle pour bouger la fenêtre (en haut dcp)
        self.coords(window_items[10], x0_cadre, y0_cadre, x1_cadre - 40, y0_cadre + 20)

        # rectangles pour changer la taille de la fenêtre
        # Ils sont créés dans cet ordre : En haut à gauche, en haut à droite
        # En bas à gauche, en bas à droite
        k = 0
        for j in range(2):
            for i in range(2):
                self.coords(
                    window_items[k],
                    [x0_cadre, x1_cadre][i] - 5,
                    [y0_cadre, y1_cadre][j] - 5,
                    [x0_cadre, x1_cadre][i] + 5,
                    [y0_cadre, y1_cadre][j] + 5
                )
                k += 1

    def drag_corner_more_info_window(self, event: tk.Event):
        """
        Je veux récupérer les coordonnées de la grande fenêtre, pour la coordonnée :
        - x0, il faut la coordonnée x0 de soit le rectangle movible, soit le grand rectangle
        - y0, il faut la coordonnée y0 de soit les boutons, soit le rectangle movible
        - x1, il faut la coordonnée x1 de soit le bouton cancel, soit le grand rectangle
        - y1, il faut la coordonnée y1 du grand rectangle

        Index:
        - Rectangle movible : 10
        - Rectangle pin : 8
        - Rectangle cancel : 6
        - Grand rectangle : 4
        """
        corners = self.find_withtag(DRAG_CORNER_MORE_INFO_WINDOW_TAG)

        # On récupère la place du coin
        # 0 = en haut à gauche
        # 1 = en haut à droite
        # 2 = en bas à gauche
        # 3 = en bas à droite (voir la création des coins)
        corner_nb = (self.find_withtag("active")[0] - corners[0]) % 4

        # On prend les coordonnées du grand rectangle auquel on va remplacer son y0 qui deviendra celui des éléments
        # Au dessus, construisant la fenêtre entière
        coords = self.coords(self.find_withtag(MORE_INFO_WINDOW)[4])
        coords[1] -= 20

        new_coords = [(event.x, event.y, coords[2], coords[3]),
                      (coords[0], event.y, event.x, coords[3]),
                      (event.x, coords[1], coords[2], event.y),
                      (coords[0], coords[1], event.x, event.y)][corner_nb]
        """
        329.0 -11.0 554 256
        329.0 29.0 554 257
        329.0 69.0 554 258
        329.0 109.0 553 258
        329.0 149.0 553 259
        329.0 189.0 553 260
        """
        self.replace_more_info_window(*new_coords)
