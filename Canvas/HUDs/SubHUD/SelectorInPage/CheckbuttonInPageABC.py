
from abc import ABC

from Canvas.HUDs.SubHUD.selectorinpageabc import SelectorInPageABC
from Canvas.Widget.Radiobutton import Checkbutton


class CheckbuttonInPageABC(SelectorInPageABC, ABC):
    def __init__(self, canvas, hud_tag: str):
        super().__init__(canvas, hud_tag)

        self.checkbuttons: list[Checkbutton] = [self.canvas.add_checkbutton()]

    @property
    def selectors(self) -> list[Checkbutton]:
        return self.checkbuttons

    @property
    def selected_option(self):
        return [
            self.from_selector_index_to_item_id_to_item[i][item_id]
            for i in range(len(self.checkbuttons))
            for item_id in self.checkbuttons[i].currently_selected
        ]

    @property
    def add_selector(self) -> callable:
        return self.canvas.add_checkbutton

    def griser(self, *args) -> None:
        self.cur_selector.griser()

    def degriser(self, *args) -> None:
        self.cur_selector.degriser()
