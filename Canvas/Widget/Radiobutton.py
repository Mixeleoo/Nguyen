
from abc import ABC, abstractmethod

from parameter import *
from Canvas.highlight_canvas import HighlightCanvas


class SelectorsABC(ABC):
    def __init__(self, canvas: HighlightCanvas, group_tag: str):

        self.canvas = canvas
        self.group_tag = group_tag

        # L'option actuellement selectionnée
        self.currently_selected = None

        # Nombre d'options
        self.nb_options = 0

    def add_option(self, option_id: int) -> None:
        """
        Méthode qui ajoute une option au radiobutton.

        :param option_id: id de l'élément à ajouter au sélecteur.
        """
        tags = list(self.canvas.gettags(option_id))
        tags[GROUP_TAG_INDEX] = self.group_tag
        self.canvas.itemconfigure(option_id, tags=tags)
        self.nb_options += 1

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
        """
        pass

    @abstractmethod
    def get_selected_option(self, *args) -> int | list[int, ...] | None:
        """
        Méthode qui retournera le(s) option(s) récupérée(s) sous forme d'id ou liste d'id.
        """
        pass

    @abstractmethod
    def griser(self, *args) -> None:
        """
        Méthode qui "grisera" les choix sélectionnés (= cachera les choix sélectionnés).
        """
        pass

    @abstractmethod
    def degriser(self, *args) -> None:
        """
        Méthode qui "degrisera" les choix sélectionnés (= highlightera les choix sélectionnés).
        """
        pass


class Radiobutton(SelectorsABC):
    def __init__(self, canvas: HighlightCanvas, group_tag: str):
        super().__init__(canvas, group_tag)

    def reset(self):
        self.griser()
        self.currently_selected = None

    def griser(self):
        if self.currently_selected:
            self.canvas.itemconfigure(
                self.currently_selected,
                fill=self.canvas.gettags(self.currently_selected)[COLOR_TAG_INDEX]
            )

    def degriser(self):
        if self.currently_selected:
            self.canvas.itemconfigure(
                self.currently_selected,
                fill=fill_brighter[self.canvas.gettags(self.currently_selected)[COLOR_TAG_INDEX]]
            )

    def toggle_switch_option(self, option_id: int):

        # S'il y a quelque chose à unhighlight
        if self.currently_selected:
            self.griser()

        # On highlight l'option qui est cliquée
        self.canvas.highlight_clickable()

        # On met à jour la dernière option cliquée
        self.currently_selected = option_id

    def get_selected_option(self) -> int | None: return self.currently_selected


class Checkbutton(SelectorsABC):
    def __init__(self, canvas: HighlightCanvas, group_tag: str):
        super().__init__(canvas, group_tag)

        self.currently_selected = []

    def reset(self) -> None:

        # On remet leur couleur par défaut
        self.griser()

        # On remet à vide la liste des éléments sélectionnés
        self.currently_selected = []

    def griser(self):
        for option_id in self.currently_selected:
            self.canvas.itemconfigure(
                option_id,
                fill=self.canvas.gettags(option_id)[COLOR_TAG_INDEX]
            )

    def degriser(self):
        for option_id in self.currently_selected:
            self.canvas.itemconfigure(
                option_id,
                fill=fill_brighter[self.canvas.gettags(option_id)[COLOR_TAG_INDEX]]
            )

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

    def get_selected_option(self, *args) -> list[int, ...] | list: return self.currently_selected


class SelectorSupervisor:

    """
    Cette classe servira à gérer les différents radiobutton sur le canvas
    """
    def __init__(self, canvas: HighlightCanvas):

        self.current_radio_group_id = 0
        self.current_check_group_id = 0

        self.canvas = canvas
        self.selectors: dict[str, Radiobutton | Checkbutton] = {

        }

    def add_radiobutton(self, *items_id: int) -> Radiobutton:
        """
        Cette méthode sert à encadrer l'ajout de nouveaux radiobuttons.
        Elle ajoutera le nouveau radiobutton à sa liste.
        Pour chacun des éléments de ce radiobutton, elle ajoutera le tag pour les regrouper.
        """
        group_tag = f"radiobutton_group{self.current_radio_group_id}"

        self.current_radio_group_id += 1
        self.selectors[group_tag] = Radiobutton(self.canvas, group_tag)

        for item_id in items_id:
            tags = list(self.canvas.gettags(item_id))
            tags[GROUP_TAG_INDEX] = group_tag
            self.canvas.itemconfigure(item_id, tags=tags)

        return self.selectors[group_tag]

    def add_checkbutton(self, *items_id: int) -> Radiobutton:
        """
        Cette méthode sert à encadrer l'ajout de nouveaux selectors.
        Elle ajoutera le nouveau selector à sa liste.
        Pour chacun des éléments de ce selector, elle ajoutera le tag pour les regrouper.
        """
        group_tag = f"checkbutton_group{self.current_check_group_id}"

        self.current_check_group_id += 1
        self.selectors[group_tag] = Checkbutton(self.canvas, group_tag)

        for item_id in items_id:
            self.selectors[group_tag].add_option(item_id)

        return self.selectors[group_tag]

    def toggle_switch_option(self, group_tag: str, option_id: int):
        self.selectors[group_tag].toggle_switch_option(option_id)
