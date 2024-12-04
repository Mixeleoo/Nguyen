
from typing import Literal
import tkinter as tk
from abc import ABC, abstractmethod

from parameter import *
from Canvas.base_canvas import BaseCanvas

class ButtonABC(ABC):
    def __init__(self, canvas: BaseCanvas, hud_tag: str, group_tag: str, trigger_name: str,
                 func_triggered: callable = dummy,
                 for_which_game_mode: tuple[str, ...] = ("basic", "build_city", "build_church")):

        # Attribus dépendant des arguments
        self.canvas = canvas
        self.group_tag = group_tag
        self.hud_tag = hud_tag
        self.trigger_name = trigger_name

        # Attribus fixes dès la création du bouton
        self.id = 0

        self.attach_trigger_to_button(func_triggered, for_which_game_mode)

    @abstractmethod
    def draw(self, *args) -> int:
        """
        Méthode qui dessine le bouton

        :return: id du rectangle du milieu
        """
        pass

    def attach_trigger_to_button(self, func: callable, for_which_game_mode: tuple[str, ...] = ("basic", "build_city", "build_church")):
        # S'il y a une fonction à attacher au tag
        if func:
            # Pour chaque mode de jeu existant
            for game_mode in ("basic", "build_city", "build_church"):

                # Si la fonction est censée être trigger durant ce mode de jeu
                if game_mode in for_which_game_mode:

                    # Si le nom du trigger apparaît dores et déjà dans le dictionnaire, c'est pas bon
                    if self.trigger_name in game_mode:
                        raise TypeError(f"{self.trigger_name} a déjà une fonction attribuée dans le mode de jeu {game_mode}.")

                    else:
                        self.canvas.tag_foc[game_mode][self.trigger_name] = func

                # Sinon ça veut dire qu'il faut attacher lambda e=None: None à ce tag pour le mode de jeu
                else:
                    self.canvas.tag_foc[game_mode][self.trigger_name] = dummy

    def move(self, dx: float, dy: float) -> None:
        """
        Méthode qui bouge le bouton
        """
        self.canvas.move(self.group_tag, dx, dy)


class Button(ButtonABC):
    def __init__(self, canvas: BaseCanvas, hud_tag: str, group_tag: str, trigger_name: str,
                 func_triggered: callable = dummy,
                 for_which_game_mode: tuple[str, ...] = ("basic", "build_city", "build_church")):

        super().__init__(canvas, hud_tag, group_tag, trigger_name, func_triggered, for_which_game_mode)

    def draw(
            self: ButtonABC, x0: int | float, y0: int | float, x1: int | float, y1: int | float,
            text: str=None, text_font=None,
            state: Literal["normal", "hidden", "disabled"] = "normal", is_temp: bool = False, fill=FILL_ACTION_BOX
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
            tags=set_tags(color_tag="#CCCCCC", hud_tag=self.hud_tag, group_tag=self.group_tag) + if_temp,
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
                hud_tag=self.hud_tag,
                group_tag=self.group_tag
            ) + if_temp,
            text_tags=set_tags(hud_tag=self.hud_tag, group_tag=self.group_tag) + (TEXT_TAG,) + if_temp,
            fill=fill_brighter[fill], state=state
        )

        # On lie les deux rectangles
        self.canvas.get_rect_border_id_from_inner_id[rect_inner] = rect_border
        self.id = rect_inner

        return rect_inner


class ButtonSupervisor:
    def __init__(self, canvas: BaseCanvas):

        self.canvas = canvas

        self.current_group_id = 0

    def add(
            self, hud_tag: str, trigger_name: str,
            func_triggered: callable = dummy,
            for_which_game_mode: tuple[str, ...] = ("basic", "build_city", "build_church")
    ) -> Button:
        """
        Méthode qui servira à ajouter des boutons et à leur attribuer un tag différent pour éviter les ambigüités

        :param hud_tag:
        :param func_triggered:
        :param trigger_name:
        :param for_which_game_mode:
        :return: Button
        """
        b = Button(
            self.canvas,
            hud_tag,
            f"button_group{self.current_group_id}",
            trigger_name,
            func_triggered,
            for_which_game_mode
        )

        self.current_group_id += 1
        return b

    def create_ok_button(
            self, x1_cadre: int | float, y1_cadre: int | float, hud_tag: str, func_triggered: callable = None,
            state: Literal["normal", "hidden", "disabled"] = "normal",
            trigger_name: str = NOTHING_TAG, is_temp: bool = False,
            for_which_game_mode: tuple[str, ...] = ("basic", "build_city", "build_church")
    ) -> Button:
        """
        Méthode qui créera un bouton, avec le comportement, l'emplacement et la couleur d'un OK bouton
        Emplacement
        """
        text_width = get_width_text("OK")

        b = self.add(
            hud_tag=hud_tag,
            trigger_name=trigger_name,
            func_triggered=func_triggered,
            for_which_game_mode=for_which_game_mode
        )
        b.draw(
            x1_cadre - text_width + 5, y1_cadre - 15, x1_cadre + 5, y1_cadre + 5,
            text="OK", fill=FILL_OK, state=state, is_temp=is_temp
        )
        return b

    def create_cancel_button(
            self, x0_cadre: int | float, y1_cadre: int | float, hud_tag: str, func_triggered: callable = None,
            state: Literal["normal", "hidden", "disabled"] = "normal",
            trigger_name: str = NOTHING_TAG, is_temp: bool = False,
            for_which_game_mode: tuple[str, ...] = ("basic", "build_city", "build_church")
    ) -> Button:
        """
        Méthode qui créera un bouton, avec le comportement, l'emplacement et la couleur d'un OK bouton
        Emplacement
        """
        text_width = get_width_text("Annuler")

        b = self.add(
            hud_tag=hud_tag,
            trigger_name=trigger_name,
            func_triggered=func_triggered,
            for_which_game_mode=for_which_game_mode
        )
        b.draw(
            x0_cadre - 5, y1_cadre - 15, x0_cadre + text_width - 5, y1_cadre + 5,
            text="Annuler", fill=FILL_CANCEL, state=state, is_temp=is_temp
        )
        return b
