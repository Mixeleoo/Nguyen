
from abc import ABC

from Canvas.HUDs.HUDMobile.base import HUDMobileABC
from Canvas.hud_canvas import HUDCanvas
from .HUDAnimationManager import HUDAnimationManager

class HUDABC(HUDAnimationManager, HUDMobileABC, ABC):
    def __init__(self, canvas: HUDCanvas):
        super().__init__(canvas)
