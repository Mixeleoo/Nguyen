
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

        """Cette variable servira à savoir dans quel mode de jeu on se trouve
        Par exemple si on est en simple vue de carte (par exemple en fin de tour), alors on sera limité dans les actions
        Alors que si on est en mode construction (village, église, etc...), alors les clics sur la map seront gérés
        Différements, car si en mode construction d'eglise on clique sur un village alors une église sera construite
        Sur le village cliqué, alors que si nous étions en simple vue, les données de ce village se seraient affichées
        """

        # Fonction qui va générer tous les carrés aléatoirement
        self.canvas.generate_game_grid(game_grid_geometry)

        # Créer les HUDs
        self.canvas.create_HUDs(geometry_width, geometry_height)
        self.canvas.add_history_text(f"Année n°{self.canvas.jeu.tour}")
        self.canvas.tag_raise(self.canvas.hudmobile_start_menu.tag)
        self.canvas.hud_history.hide_exceeding_text()

        """# Ajouter l'image au canvas
        # Je mets un self pour éviter que le garbage collector ne supprime la photo
        original_image = Image.open("./assets/shrek.jpg")
        resized_image = original_image.resize((149 - 5, 20))

        # Convertir l'image redimensionnée en format Tkinter
        self.reference = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(423, 16, image=self.reference, tags=(HUD_TAG, NOTHING_TAG))"""

    def on_configure_screen(self, event: tk.Event):
        self.canvas.replace_static_hud(event)
        self.previous_geometry = (event.width, event.height)

    def lancer_partie(self):
        self.mainloop()

if __name__ == "__main__":
    jeu = Interface()
    jeu.lancer_partie()
