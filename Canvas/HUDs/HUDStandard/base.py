
from abc import ABC, abstractmethod

from Canvas.HUDs.HUDMobile.base import HUDMobileABC
from Canvas.hud_canvas import HUDCanvas
from .HUDAnimationManager import HUDAnimationManager

class HUDABC(HUDAnimationManager, HUDMobileABC, ABC):
    def __init__(self, canvas: HUDCanvas):
        super().__init__(canvas)

    @abstractmethod
    def create(self, geometry_width: int, geometry_height: int):
        pass
