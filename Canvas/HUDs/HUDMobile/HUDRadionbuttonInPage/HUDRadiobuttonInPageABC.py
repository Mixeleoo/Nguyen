
from typing import Optional
from abc import ABC, abstractmethod
import tkinter as tk

from Canvas.Widget.Button import Button
from Canvas.Widget.Radiobutton import Radiobutton, SelectorsABC
from Canvas.HUDs.HUDMobile.SelectorInPageABC import SelectorInPageABC

class HUDRadiobuttonInPageABC(SelectorInPageABC, ABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.ok_button: Optional[Button] = None
        self.cancel_button: Optional[Button] = None

        self.last_radiobutton_index_choice = None
        self.radiobuttons: list[Radiobutton] = [self.canvas.add_radiobutton()]

    @property
    def selectors(self) -> list[SelectorsABC]:
        return self.radiobuttons

    @property
    def selected_option(self):
        res = None
        for i in range(len(self.radiobuttons)):
            if self.radiobuttons[i].currently_selected:
                res = self.from_selector_index_to_item_id_to_item[i][self.radiobuttons[i].currently_selected]

        return res

    @property
    def add_selector(self) -> callable:
        return self.canvas.add_radiobutton

    @abstractmethod
    def ok_trigger(self, event: tk.Event):
        pass

    def create(self) -> None:

        x0_cadre, y0_cadre, x1_cadre, y1_cadre = SelectorInPageABC.create(self)

        # Bouton OK qui lance l'immigration
        self.ok_button = self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.ok_trigger, is_temp=True, state="hidden"
        )

        # Bouton Annuler qui annule l'immigration
        self.cancel_button = self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.bhide, is_temp=True, state="hidden"
        )

    def replace(self, *args) -> None:

        bbox = self.canvas.bbox(self.tag)

        dx = self.canvas.master.winfo_width() // 2 - (bbox[2] + bbox[0]) // 2
        dy = self.canvas.master.winfo_height() // 2 - (bbox[3] + bbox[1]) // 2

        self.canvas.move(self.tag, dx, dy)

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
