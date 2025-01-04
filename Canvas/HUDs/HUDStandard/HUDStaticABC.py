
from abc import ABC, abstractmethod
import tkinter as tk

from Canvas.self_made_canvas import SelfMadeCanvas
from Canvas.HUDs.HUDStandard.HUDAnimationManagerABC import HUDAnimationManager

class HUDStaticABC(HUDAnimationManager, ABC):
    _instances_static: list["HUDStaticABC"] = []

    @classmethod
    def replace_all(cls, event: tk.Event):
        for instance in cls._instances_static:
            instance.replace(event)

    def __init__(self, canvas: SelfMadeCanvas):
        super().__init__(canvas)
        HUDStaticABC._instances_static.append(self)

    @abstractmethod
    def create(self, geometry_width: int, geometry_height: int):
        pass
