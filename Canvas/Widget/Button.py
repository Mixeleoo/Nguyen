
from typing import Literal
import tkinter as tk
from abc import ABC, abstractmethod

from parameter import *
from Canvas.base_canvas import BaseCanvas

class ButtonABC(ABC):
    _instance_counter = 0

    def __init__(self, canvas: BaseCanvas, hud_tag: str, trigger_name: str,
                 func_triggered: callable = dummy,
                 for_which_game_mode: tuple[str] = ("basic", "build_city", "build_church")):

        # Attribus dépendant des arguments
        self.canvas = canvas
        self.hud_tag = hud_tag
        self.trigger_name = trigger_name

        # Attribus fixes dès la création du bouton
        self.id = 0

        # Tag pour différencier entre chaque bouton
        self._index = ButtonABC._instance_counter
        ButtonABC._instance_counter += 1
        self.group_tag = "button" + str(self._index)

        self.attach_trigger_to_button(func_triggered, for_which_game_mode)

    @abstractmethod
    def draw(self, *args) -> int:
        """
        Méthode qui dessine le bouton

        :return: id du rectangle du milieu
        """
        pass

    def attach_trigger_to_button(self, func: callable, for_which_game_mode: tuple[str] = ("basic", "build_city", "build_church")):
        # S'il y a une fonction à attacher au tag
        if func:
            self.canvas.new_trigger(self.trigger_name, func, for_which_game_mode)

    def move(self, dx: float, dy: float) -> None:
        """
        Méthode qui bouge le bouton
        """
        self.canvas.move(self.group_tag, dx, dy)

    @abstractmethod
    def desactivate(self):
        """
        Méthode qui rendra le bouton inutilisable avec un effet visuel le grisant pour indiquer son hors-service.
        """
        pass

    @abstractmethod
    def reactivate(self):
        """
        Méthode qui rendra le bouton réutilisable.
        """
        pass


class Button(ButtonABC):
    def __init__(self, canvas: BaseCanvas, hud_tag: str, trigger_name: str = NOTHING_TAG,
                 func_triggered: callable = dummy,
                 for_which_game_mode: tuple[str] = ("basic", "build_city", "build_church")):

        super().__init__(canvas, hud_tag, trigger_name, func_triggered, for_which_game_mode)

    def draw(
            self: ButtonABC, x0: int | float, y0: int | float, x1: int | float, y1: int | float,
            text: str=None, text_font=None,
            state: Literal["normal", "hidden", "disabled"] = "normal", is_temp: bool = False, fill=FILL_ACTION_BOX,
            justify: Literal["left", "center", "right"] = "left"
    ) -> int:
        """
        Méthode qui créerera un texte sur un rectangle, qui agira comme un bouton :
        - Il est clickable (highlight)
        - Trigger une fonction lorsque clické dessus (trigger_name)
        - Peut être temporaire (is_temp)
        """
        if text_font is None:
            text_font = tk.font.nametofont("TkDefaultFont")

        if_temp = (TEMP_TAG,) if is_temp else tuple()

        rect_border = self.canvas.create_rectangle(
            x0, y0, x1, y1,
            outline="#CCCCCC",
            width=1,
            tags=set_tags(color_tag="#CCCCCC", hud_tag=self.hud_tag) + if_temp,
            state=state
        )

        rect_inner = self.canvas.create_text_in_rectangle(
            x0 + 1, y0 + 1, x1 - 1, y1 - 1,
            outline="grey",
            text=text,
            text_font=text_font,
            rectangle_tags=set_tags(
                HIGHLIGHT_BUTTON_TAG,
                self.trigger_name,
                color_tag=fill,
                hud_tag=self.hud_tag
            ) + if_temp,
            text_tags=set_tags(hud_tag=self.hud_tag) + (TEXT_TAG,) + if_temp,
            fill=fill_brighter[fill], state=state, justify=justify
        )

        # On lie les deux rectangles
        self.canvas.get_rect_border_id_from_inner_id[rect_inner] = rect_border
        self.id = rect_inner

        return rect_inner

    def desactivate(self):
        tags = list(self.canvas.gettags(self.id))
        tags[TRIGGER_TAG_INDEX] = NOTHING_TAG

        self.canvas.itemconfigure(self.id, tags=tags)
        self.canvas.itemconfigure(self.id, fill=tags[COLOR_TAG_INDEX])

    def reactivate(self):
        tags = list(self.canvas.gettags(self.id))
        tags[TRIGGER_TAG_INDEX] = self.trigger_name

        self.canvas.itemconfigure(self.id, tags=tags)
        self.canvas.itemconfigure(self.id, fill=fill_brighter[tags[COLOR_TAG_INDEX]])
