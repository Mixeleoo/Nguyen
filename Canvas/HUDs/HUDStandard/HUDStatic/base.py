
from abc import ABC, abstractmethod

from Canvas.HUDs.HUDStandard.base import HUDStandardABC
from Canvas.hud_canvas import HUDCanvas
from .HUDAnimationManager import HUDAnimationManager

class HUDStaticABC(HUDAnimationManager, HUDStandardABC, ABC):
    def __init__(self, canvas: HUDCanvas):
        super().__init__(canvas)

    @property
    def tag(self):
        return self.__class__.__name__

    @abstractmethod
    def create(self, geometry_width: int, geometry_height: int):
        pass
