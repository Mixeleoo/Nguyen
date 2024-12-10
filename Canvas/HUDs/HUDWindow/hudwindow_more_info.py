
from .base import HUDWindowABC
from Canvas.hud_canvas import HUDCanvas
from parameter import *

class HUDWindowMoreInfo(HUDWindowABC):
    def __init__(self, canvas, village_tag: str):
        super().__init__(canvas)
        self._text = "Plus d'info dans cette fenêtre (ou pas)"
        self._village_tag = village_tag

    @property
    def tag(self):
        return self._village_tag


class HUDWindowMoreInfoSupervisor:
    def __init__(self, canvas: HUDCanvas):
        self.canvas = canvas
        self.current_group_id = 0

        self.windows: dict[str: HUDWindowMoreInfo] = {}

    def add(self, village_name: str | None=None):
        tag = village_name or f"village_{self.current_group_id}"

        self.windows["p" + tag] = HUDWindowMoreInfo(self.canvas, tag)
        self.windows[tag] = self.windows["p" + tag]
        self.windows["p" + tag].create()

        self.current_group_id += 1

    def get_active_window(self) -> HUDWindowMoreInfo: return self.windows[self.canvas.gettags("active")[GROUP_TAG_INDEX]]
