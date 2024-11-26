
from abc import ABC, abstractmethod
import tkinter as tk

from parameter import *
from Canvas.base_canvas import BaseCanvas

class HUDABC(ABC):
    def __init__(self, canvas: BaseCanvas):
        self.canvas = canvas

    @property
    @abstractmethod
    def tag(self):
        """
        Méthode pour retourner le tag de l'HUD
        """
        pass

    @abstractmethod
    def create(self, geometry_width: int, geometry_height: int) -> None:
        """
        Méthode d'initialisation de la classe HUD
        """
        pass

    @abstractmethod
    def replace(self, event: tk.Event) -> None:
        """
        Méthode de replacement de l'HUD
        """
        pass

    @abstractmethod
    def show_animation(self) -> None:
        """
        Méthode d'animation de révélation des éléments de l'HUD
        """
        pass

    @abstractmethod
    def hide_animation(self) -> None:
        """
        Méthode d'animation de masquage des éléments de l'HUD
        """
        pass

    def show(self, *args) -> None:
        for item_id in self.canvas.find_withtag(self.tag):
            self.canvas.itemconfigure(item_id, state="normal")

    def hide(self, *args) -> None:
        for item_id in self.canvas.find_withtag(self.tag):
            self.canvas.itemconfigure(item_id, state="hidden")

    def hide_show_hud(self, previous_tag: str, new_tag: str, anim: callable):
        """
        Fonction qui servira à switcher de "montrer" à "cacher" (et inversement) les HUD concernés.
        """
        tags = list(self.canvas.gettags(previous_tag))
        tags[TRIGGER_TAG_INDEX] = new_tag

        self.canvas.itemconfigure(previous_tag, tags=tags)
        anim()
