
from Canvas.hud_canvas import HUDCanvas
from parameter import *

class AnimationCanvas(HUDCanvas):
    def __init__(self, master=None, cnf=None, **kw):
        # C'est PyCharm qui me dit de mettre ça au lieu de cnf={} directement dans les arguments donc...
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

    def move_back_square(self):
        # On prend les coordonnées en haut (y0) à gauche (x0) du carré le plus en haut à gauche
        # Pour avoir le point le plus en haut à gauche de la totalité de la grille de carrés
        coor_square_top_left = self.coords(MAP_SQUARE_TOP_LEFT_TAG)
        x0 = coor_square_top_left[0]
        y0 = coor_square_top_left[1]

        # On prend les coordonnées en bas (y1) à droite (x1) du carré le plus en bas à droite
        # Pour avoir le point le plus en bas à droite de la totalité de la grille de carrés
        coor_square_bottom_right = self.coords(MAP_SQUARE_BOTTOM_RIGHT_TAG)
        x1 = coor_square_bottom_right[2]
        y1 = coor_square_bottom_right[3]

        dx, dy = 0, 0

        # Si les carrés sont trop à droite, on les reme vers la gauche
        if x0 > 0:
            dx = -1 * (x0 // 5 + 1)

        # Si les carrés sont trop à gauche, on les remet vers la droite
        # La distance entre (donc la valeur absolue de) le bord droit de la fenêtre et les carrés les plus à droite
        # // 10 Pour dire qu'à chaque pixel, on augmente la vélocité d'un pixel
        # + 1 pour que quand la distance est < 10, qu'il y ait quand même un déplacement d'un pixel pour bien replacer
        # Les carrés au pixel près.
        elif x1 < self.master.winfo_width():
            dx = 1 * (abs(self.master.winfo_width() - x1) // 5 + 1)

        # Si les carrés sont trop en bas, on les remet vers le haut
        if y0 > 0:
            dy = -1 * (y0 // 5 + 1)

        # Si les carrés sont trop en haut, on les remet vers le bas
        elif y1 < self.master.winfo_height():
            dy = 1 * (abs(self.master.winfo_height() - y1) // 5 + 1)

        # S'il y a un décalage à faire, alors on le répète toutes les 50ms le temps que nécessaire
        # En accelérant la vélocité à chaque répétition
        if dx or dy:
            # Déplace tous les carrés avec le tag "square"
            self.move(MAP_TAG, dx, dy)
            self.after(DELTA_MS_ANIMATION, self.move_back_square)
