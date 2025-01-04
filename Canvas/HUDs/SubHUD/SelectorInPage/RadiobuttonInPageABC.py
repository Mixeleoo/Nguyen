
from abc import ABC

from Canvas.Widget.Radiobutton import Radiobutton
from ..selectorinpageabc import SelectorInPageABC

class RadiobuttonInPageABC(SelectorInPageABC, ABC):
    def __init__(self, canvas, hud_tag: str):
        super().__init__(canvas, hud_tag)

        self.last_radiobutton_index_choice = None
        self.radiobuttons: list[Radiobutton] = [self.canvas.add_radiobutton()]

    @property
    def selectors(self) -> list[Radiobutton]:
        return self.radiobuttons

    @property
    def selected_option(self):
        res = None
        for i in range(len(self.radiobuttons)):
            if self.radiobuttons[i].currently_selected:
                res = self.list_selector_choices_to_item[i][self.radiobuttons[i].currently_selected]
        return res

    @property
    def add_selector(self) -> callable:
        return self.canvas.add_radiobutton

    def griser(self, *args) -> None:
        """
        S'il y a un élément sélectionné sur la page actuelle ET que le dernier choix effectué était sur une autre page
            ça veut dire qu'il faut griser le dernier radiobutton dans lequel un choix a été cliqué
        Sinon il faut allumer le choix sélectionné du prochain radiobutton.
        """
        if self.last_radiobutton_index_choice is not None:
            if self.cur_selector.currently_selected and self.last_radiobutton_index_choice != self.cur_selector_index:
                self.radiobuttons[self.last_radiobutton_index_choice].reset()

        if self.cur_selector.currently_selected:
            self.last_radiobutton_index_choice = self.cur_selector_index
            self.cur_selector.griser()

    def degriser(self, *args) -> None:
        self.cur_selector.degriser()
