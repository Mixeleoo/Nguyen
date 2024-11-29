
from abc import ABC, abstractmethod

from Canvas.hud_canvas import HUDCanvas

class HUDMobileABC(ABC):
    def __init__(self, canvas: HUDCanvas):
        self.canvas = canvas

    @property
    @abstractmethod
    def tag(self):
        """
        Méthode pour retourner le tag de l'HUDs
        """
        pass

    @abstractmethod
    def create(self, *args):
        """
        Méthode d'initialisation de la classe HUDs
        """
        pass

    @abstractmethod
    def replace(self, *args) -> None:
        """
        Méthode de replacement de l'HUDs
        """
        pass

    def show(self, *args) -> None:
        self.replace(*args)

        for item_id in self.canvas.find_withtag(self.tag):
            self.canvas.itemconfigure(item_id, state="normal")

    def hide(self, *args) -> None:
        for item_id in self.canvas.find_withtag(self.tag):
            self.canvas.itemconfigure(item_id, state="hidden")
