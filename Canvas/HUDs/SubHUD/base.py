
from abc import ABC, abstractmethod

from Canvas.hud_canvas import HUDCanvas

class SubHUDABC(ABC):
    def __init__(self, canvas: HUDCanvas, tag: str):
        self.canvas = canvas
        self.tag = tag

    @abstractmethod
    def create(self, *args):
        """
        Méthode d'initialisation du sous HUD.
        """
        pass

    @abstractmethod
    def setup_before_display(self, *args) -> None:
        """
        Méthode de mise à jour du sous HUD.
        """
        pass
