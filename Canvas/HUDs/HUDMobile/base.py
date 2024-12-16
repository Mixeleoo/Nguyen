
from abc import ABC, abstractmethod

from Canvas.hud_canvas import HUDCanvas

class HUDMobileABC(ABC):
    def __init__(self, canvas: HUDCanvas):
        self.canvas = canvas

    @property
    def tag(self):
        return self.__class__.__name__

    @abstractmethod
    def create(self, *args):
        """
        Méthode d'initialisation de la classe HUD
        """
        pass

    @abstractmethod
    def replace(self, *args) -> None:
        """
        Méthode de replacement de l'HUD
        """
        pass

    def no_replace_show(self, *args) -> None:
        for item_id in self.canvas.find_withtag(self.tag):
            self.canvas.itemconfigure(item_id, state="normal")

    def show(self, *args) -> None:
        """
        Affiche les éléments de l'HUDs
        """
        self.no_replace_show(*args)

        # IMPORTANT DE LES REPLACER APRES LES AVOIR AFFICHÉS SINON TKINTER NE SAIT PAS LEURS COORDONNEES
        self.replace(*args)

    def hide(self, *args) -> None:
        """
        Cache les éléments de l'HUDs
        """
        for item_id in self.canvas.find_withtag(self.tag):
            self.canvas.itemconfigure(item_id, state="hidden")
