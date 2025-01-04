
from abc import ABC, abstractmethod

from Canvas.self_made_canvas import SelfMadeCanvas

class HUDStandardABC(ABC):
    _instance_counter = 0
    _instances: list["HUDStandardABC"] = []

    @classmethod
    def create_all(cls, geometry_width: int, geometry_height: int) -> None:
        for instance in cls._instances:
            instance.create(geometry_width, geometry_height)

    def __init__(self, canvas: SelfMadeCanvas):
        self.canvas = canvas
        self._index = HUDStandardABC._instance_counter
        HUDStandardABC._instance_counter += 1
        HUDStandardABC._instances.append(self)

    @property
    def tag(self):
        return self.__class__.__name__ + str(self._index)

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

    def bbox(self):
        return self.canvas.bbox(self.tag)


def replace_coords(self: HUDStandardABC, x: int, y: int) -> None:
    dx = x - self.canvas.coords(self.canvas.find_withtag(self.tag)[0])[0]
    dy = y - self.canvas.coords(self.canvas.find_withtag(self.tag)[0])[1]

    self.canvas.move(self.tag, dx, dy)
