
from abc import ABC, abstractmethod
from typing import Literal

from Canvas.self_made_canvas import SelfMadeCanvas

class HUDHideableABC(ABC):
    _instances: list["HUDHideableABC"] = []
    _instances_hidden_to_show: list["HUDHideableABC"] = []

    @classmethod
    def all_hidden(cls):
        hidden = False
        for instance in cls._instances:
            if instance.state == "hidden":
                hidden = True

        return hidden

    @classmethod
    def hide_all(cls):
        for instance in cls._instances:
            if instance.state == "normal":
                cls._instances_hidden_to_show.append(instance)
                instance.bhide()

    @classmethod
    def show_all_hidden(cls):
        for instance in cls._instances_hidden_to_show:
            instance.bshow()

    def __init__(self, canvas: SelfMadeCanvas):
        self.canvas = canvas
        self.state: Literal["normal", "hidden"] = "normal"
        self.hide_button_id = 0

        HUDHideableABC._instances.append(self)

    @abstractmethod
    def hide_animation(self):
        pass

    @abstractmethod
    def show_animation(self):
        pass

    @property
    @abstractmethod
    def hide_symbol(self) -> str:
        pass

    @property
    @abstractmethod
    def show_symbol(self) -> str:
        pass

    def bhide(self):
        """
        La phase before hide, qui consiste à changer l'état du HUDs en "hidden" et lancer l'animation
        """
        if HUDHideableABC.all_hidden():
            self.canvas.hud_end_turn.bhide()

        self.state = "hidden"
        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.hide_button_id], text=self.show_symbol)
        self.hide_animation()

    def bshow(self):
        """
        La phase before show, qui consiste à changer l'état du HUDs en "normal" et lancer l'animation
        """
        if self.canvas.hud_end_turn.state == "hidden":
            self.canvas.hud_end_turn.bshow()

        self.state = "normal"
        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.hide_button_id], text=self.hide_symbol)
        self.show_animation()

    def show_or_hide(self, e=None):
        if self.state == "normal":
            self.bhide()

        else:
            self.bshow()
