
from abc import ABC, abstractmethod
from typing import Literal

from parameter import *
from Canvas.highlight_canvas import HighlightCanvas


class SelectorsABC(ABC):
    def __init__(self, canvas: HighlightCanvas, group_tag: str):
        self.canvas = canvas
        self.group_tag = group_tag

        # L'option actuellement selectionnée
        self.currently_selected = None

    def add_option(self, option_id: int) -> None:
        """
        Méthode qui ajoute une option au radiobutton (comme ça, c'est dynamique).

        :param option_id: id de l'élément à ajouter au sélecteur.
        """
        tags = list(self.canvas.gettags(option_id))
        tags[GROUP_TAG_INDEX] = self.group_tag
        self.canvas.itemconfigure(option_id, tags=tags)

    @abstractmethod
    def reset(self) -> None:
        """
        Méthode qui restaure le sélecteur à son état par défaut :
            - Aucuns choix sélectionnés.
            - Tous les choix grisés.
        """
        pass

    @abstractmethod
    def toggle_switch_option(self, option_id: int) -> None:
        """
        Méthode qui sera trigger lors du clic sur un choix du sélecteur concerné.

        :param option_id: id de l'élément à toggle
        :return:
        """
        pass

    @abstractmethod
    def get_selected_option(self, *args) -> int | list[int, ...] | None:
        """
        Méthode qui retournera le(s) option(s) récupérée(s) sous forme d'id ou liste d'id.
        """
        pass


class Radiobutton(SelectorsABC):
    def __init__(self, canvas: HighlightCanvas, group_tag: str):
        super().__init__(canvas, group_tag)

    def reset(self):

        if self.currently_selected:
            self.canvas.itemconfigure(
                self.currently_selected,
                fill=self.canvas.gettags(self.currently_selected)[COLOR_TAG_INDEX]
            )

            self.currently_selected = None

    def toggle_switch_option(self, option_id: int):

        # S'il y a quelque chose à unhighlight
        if self.currently_selected:
            self.canvas.itemconfigure(
                self.currently_selected,
                fill=self.canvas.gettags(self.currently_selected)[COLOR_TAG_INDEX]
            )

        # On highlight l'option qui est cliquée
        self.canvas.highlight_clickable()

        # On met à jour la dernière option cliquée
        self.currently_selected = option_id

    def get_selected_option(self) -> int | None:
        """
        :return: L'id du rectangle dernièrement sélectionné
        """
        return self.currently_selected


class Checkbutton(SelectorsABC):
    def __init__(self, canvas: HighlightCanvas, group_tag: str):
        super().__init__(canvas, group_tag)

        self.currently_selected = []

    def reset(self) -> None:

        # On remet leur couleur par défaut
        for option_id in self.currently_selected:
            self.canvas.itemconfigure(
                option_id,
                fill=self.canvas.gettags(option_id)[COLOR_TAG_INDEX]
            )

            # On remet à vide la liste des éléments sélectionnés
            self.currently_selected = []

    def toggle_switch_option(self, option_id: int):

        # Si l'option clickée était déjà clickée, alors on la unhighlight
        if option_id in self.currently_selected:

            # On unhighlight l'option clickée
            self.canvas.unhighlight_clickable()

            # On la supprime de la liste des options clickées
            self.currently_selected.remove(option_id)

        # Sinon ça veut dire que c'est une option non clickée, alors on l'highlight
        else:
            # On highlight l'option qui est cliquée
            self.canvas.highlight_clickable()

            # On met à jour la dernière option cliquée
            self.currently_selected.append(option_id)

    def get_selected_option(self, *args) -> list[int, ...] | list:
        return self.currently_selected


class RadiobuttonsSupervisor:

    """
    Cette classe servira à gérer les différents radiobutton sur le canvas
    """
    def __init__(self, canvas: HighlightCanvas):
        self.current_group_id = 0
        self.canvas = canvas
        self.radiobuttons: dict[str: Radiobutton | Checkbutton] = {

        }

    def add(self, *radiobutton_items_id: int, type_b: Literal["check", "radio"]) -> Radiobutton:
        """
        Cette méthode sert à encadrer l'ajout de nouveaux radiobuttons.
        Elle ajoutera le nouveau radiobutton à sa liste.
        Pour chacun des éléments de ce radiobutton, elle ajoutera le tag pour les regrouper.
        """
        group_tag = f"radiobutton_group{self.current_group_id}"

        self.current_group_id += 1
        self.radiobuttons[group_tag] = Radiobutton(self.canvas, group_tag)

        for item_id in radiobutton_items_id:
            tags = list(self.canvas.gettags(item_id))
            tags[GROUP_TAG_INDEX] = group_tag
            self.canvas.itemconfigure(item_id, tags=tags)

        return self.radiobuttons[group_tag]

    def toggle_switch_option(self, group_tag: str, option_id: int):
        self.radiobuttons[group_tag].toggle_switch_option(option_id)
