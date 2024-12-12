
import tkinter as tk

from parameter import *
from Canvas.function_on_drag_canvas import FunctionOnDragCanvas
from Canvas.function_on_click_canvas import FunctionOnClickCanvas


class SelfMadeCanvas(FunctionOnClickCanvas, FunctionOnDragCanvas):
    def __init__(self, master=None, cnf=None, **kw):
        # C'est PyCharm qui me dit de mettre ça au lieu de cnf={} directement dans les arguments donc...
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        self.has_mouse_moved = False

        # Coordonnées de la souris lors d'un clic (pour initier le déplacement de la map)
        self.bind("<Button-1>", self.on_click_left)  # Reset au clic
        self.bind("<Button-3>", self.on_click_right)

        # Fonction lancée lors d'un drag de la souris
        self.bind("<B1-Motion>", self.on_drag)

        self.bind("<Motion>", self.on_motion)

        # Fonction lancée lors d'un relâchement du click gauche, ne se lance que si la souris n'a pas été déplacée
        # Pendant le clic (grâce à la variable self.has_mouse_moved)
        self.bind("<ButtonRelease-1>", self.on_release)  # Relâchement

    #                                               CLIC GAUCHE #
    def on_click_left(self, event: tk.Event) -> None:

        self.has_mouse_moved = False

        # On donne le tag active à la forme qu'on veut, comme ça, les fonctions responsables de lancer les actions
        # Sauront sur quoi le joueur a voulu cliquer, donc devront se fier à "active" et pas "current"
        self.give_active_tag(event)

        # Pour du débug, on print sur ce qu'on clique
        print("Tags de l'élément clické :", self.gettags("current"))
        print("Tags de l'élément gardé :", self.gettags("active"))
        print("Id de l'élément gardé :", self.find_withtag("active")[0])

        # On initialise les coordonnées de départ de la souris
        self.mouse_coor = (event.x, event.y)

        tags = self.gettags("active")

        # Si ce n'est pas sur les actions qu'on a cliqué, alors on les delete
        if TEMP_TAG not in tags:
            for item_id in self.find_withtag(TEMP_TAG):
                self.itemconfigure(item_id, state="hidden")

        # Lancement de l'highlight
        self.highlight_tag_on_click[tags[HIGHLIGHT_TAG_INDEX]]()

    #                                          GLISSEMENT CLIC GAUCHE                                            #
    def on_drag(self, event: tk.Event) -> None:

        # Premier instant où on bouge la souris
        if not self.has_mouse_moved:
            self.has_mouse_moved = True

            tags = self.gettags("highlight")
            if tags:
                self.highlight_tag_on_drag[tags[HIGHLIGHT_TAG_INDEX]]()
                self.dtag("highlight", "highlight")

        tags = self.gettags("active")

        # Ici ça drague (LOL PCK ON_DRAG T'AS COMPRIS ????)
        self.tag_fod[tags[DRAG_TAG_INDEX]](event)

        # Met à jour la position de départ pour le prochain mouvement
        self.mouse_coor = (event.x, event.y)

    #                                          RELACHEMENT CLIC GAUCHE                                           #
    def on_release(self, event: tk.Event) -> None:

        tags = self.gettags("active")

        # Arrêter l'after trigger des quantityselector
        if self.after_quantity_selector_id is not None:
            self.after_cancel(self.after_quantity_selector_id)
            self.after_quantity_selector_id = None

        # Si la souris n'a pas bougé entre le clic et le relâchement,
        # on considère que c'est un clic gauche simple.
        if not self.has_mouse_moved:
            try:
                # On lance le trigger associé
                print("Mode de jeu :", self.game_mode)
                self.tag_foc[self.game_mode][tags[TRIGGER_TAG_INDEX]](event)

            except Exception as e:
                raise e

            finally:
                self.dtag("active", "active")

        # Animation stylée si le joueur s'amuse à sortir de la map
        else:
            self.move_back_square()

        self.dtag("active", "active")

        tags = self.gettags("highlight")
        if tags:
            # On unhighlight l'objet actif
            self.highlight_tag_on_release[tags[HIGHLIGHT_TAG_INDEX]]()
            self.dtag("highlight", "highlight")

        # Sauter une ligne
        print()

    #                                                 CLIC DROIT                                                 #
    def on_click_right(self, event: tk.Event) -> None:
        for item_id in self.find_withtag(TEMP_TAG):
            self.itemconfigure(item_id, state="hidden")

        self.hud_event.show_animation()

    def on_motion(self, event: tk.Event) -> None:

        on_corner = False

        # On vérifie pour chaque item qui se chevauchent à l'endroit clické
        for item in self.find_overlapping(event.x, event.y, event.x, event.y):
            # Si il y a le rectangle de drag sous la souris, alors on rend le rectangle qui gère tout ça sous la souris
            if "drag_corner" == self.gettags(item)[DRAG_TAG_INDEX][:11]:
                self.config(cursor="heart")
                on_corner = True

        if not on_corner:
            self.config(cursor="arrow")