
import tkinter as tk
from parameter import *

from Canvas.self_made_canvas import SelfMadeCanvas


class Interface(tk.Tk):
    def __init__(self, game_grid_geometry: tuple[int] = (CARRE_PAR_COLONNE, CARRE_PAR_LIGNE)):
        # Partie tkinter
        super().__init__()

        # sps = la longueur des carrés en pixel (square pixel size)
        self.sps = SPS
        self.title("jeu de bz")

        # canvas_width = le nombre de colonnes total multiplié à la taille d'un carré
        canvas_width = game_grid_geometry[1] * self.sps

        # canvas_height = le nombre de lignes total multiplié à la taille d'un carré
        canvas_height = game_grid_geometry[0] * self.sps

        # Largeur de la fenêtre = largeur du canvas (max 800)
        geometry_width = canvas_width if canvas_width <= MAX_WIDTH else MAX_WIDTH

        # Longueur de la fenêtre = longueur du canvas (max 700)
        geometry_height = canvas_height if canvas_height <= MAX_HEIGHT else MAX_HEIGHT

        self.geometry(f"{geometry_width}x{geometry_height}")
        self.maxsize(canvas_width, canvas_height)

        # La grille du jeu
        self.canvas = SelfMadeCanvas(self, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        # Quand on redimensionne la fenêtre, on veut que les carrés se replacent en fonction de la nouvelle taille
        self.previous_geometry = (geometry_width, geometry_height)
        self.bind("<Configure>", self.on_configure_screen)

        # Fonction qui va générer tous les carrés aléatoirement
        self.canvas.generate_game_grid(game_grid_geometry)

        # Créer les HUDs
        self.canvas.create_HUDs(geometry_width, geometry_height)
        self.canvas.add_history_text(f"Année n°{self.canvas.jeu.tour}")
        self.canvas.tag_raise(self.canvas.hud_start_menu.tag)
        self.canvas.hud_history.hide_exceeding_text()

    def on_configure_screen(self, event: tk.Event):
        self.canvas.replace_static_hud(event)
        self.previous_geometry = (event.width, event.height)

    def lancer_partie(self):
        self.mainloop()

if __name__ == "__main__":
    jeu = Interface()
    jeu.lancer_partie()
