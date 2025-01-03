
from abc import ABC, abstractmethod

from Canvas.HUDs.HUDStandard.base import HUDStandardABC
from Canvas.hud_canvas import HUDCanvas
from Canvas.HUDs.HUDStandard.HUDAnimationManagerABC import HUDAnimationManager

class HUDStaticABC(HUDAnimationManager, ABC):
    def __init__(self, canvas: HUDCanvas):
        super().__init__(canvas)

    @abstractmethod
    def create(self, geometry_width: int, geometry_height: int):
        pass
