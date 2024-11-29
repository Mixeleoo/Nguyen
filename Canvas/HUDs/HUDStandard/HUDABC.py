
from abc import ABC, abstractmethod
import tkinter as tk

from parameter import *
from Canvas.hud_canvas import HUDCanvas

class HUDABC(ABC):
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
    def create(self, geometry_width: int, geometry_height: int) -> None:
        """
        Méthode d'initialisation de la classe HUDs
        """
        pass

    @abstractmethod
    def replace(self, event: tk.Event) -> None:
        """
        Méthode de replacement de l'HUDs
        """
        pass

    @abstractmethod
    def show_animation(self) -> None:
        """
        Méthode d'animation de révélation des éléments de l'HUDs
        """
        pass

    @abstractmethod
    def hide_animation(self) -> None:
        """
        Méthode d'animation de masquage des éléments de l'HUDs
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
