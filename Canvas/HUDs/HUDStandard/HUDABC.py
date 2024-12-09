
from abc import ABC, abstractmethod
import tkinter as tk

from Canvas.hud_canvas import HUDCanvas
from Canvas.HUDs.HUDStandard.HUDAnimationManager import HUDAnimationManager

class HUDABC(HUDAnimationManager, ABC):
    def __init__(self, canvas: HUDCanvas):
        super().__init__(canvas)

        self.canvas = canvas
        self.animating = False

    @abstractmethod
    def create(self, geometry_width: int, geometry_height: int) -> None:
        """
        Méthode d'initialisation graphique de la classe HUD
        """
        pass

    @abstractmethod
    def replace(self, event: tk.Event) -> None:
        """
        Méthode de replacement de l'HUD
        """
        pass

    def show(self, *args) -> None:
        """
        Affiche les éléments de l'HUDs
        """
        for item_id in self.canvas.find_withtag(self.tag):
            self.canvas.itemconfigure(item_id, state="normal")

    def hide(self, *args) -> None:
        """
        Cache les éléments de l'HUDs
        """
        for item_id in self.canvas.find_withtag(self.tag):
            self.canvas.itemconfigure(item_id, state="hidden")
