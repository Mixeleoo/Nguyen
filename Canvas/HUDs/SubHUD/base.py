
from abc import ABC, abstractmethod

from Canvas.self_made_canvas import SelfMadeCanvas

class SubHUDABC(ABC):
    def __init__(self, canvas: SelfMadeCanvas, tag: str):
        self.canvas = canvas
        self.tag = tag

    @abstractmethod
    def create(self, *args):
        """
        Méthode d'initialisation du sous HUD.
        """
        pass

    @abstractmethod
    def update(self, *args) -> None:
        """
        Méthode de mise à jour du sous HUD.
        """
        pass
