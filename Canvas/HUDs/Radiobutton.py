
from parameter import *
from Canvas.highlight_canvas import HighlightCanvas

class Radiobutton:
    def __init__(self, canvas: HighlightCanvas, group_tag: str):

        self.canvas = canvas

        # L'option actuellement selectionnée
        self.currently_selected = None

        self.group_tag = group_tag

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

    def reset(self):
        if self.currently_selected:
            self.canvas.itemconfigure(
                self.currently_selected,
                fill=self.canvas.gettags(self.currently_selected)[COLOR_TAG_INDEX]
            )

            self.currently_selected = None

    def get_selected_option(self) -> int | None:
        """
        :return: L'id du rectangle dernièrement sélectionné
        """
        return self.currently_selected

    def add_option(self, item_id: int) -> None:
        """
        Méthode qui ajoute une option au radiobutton (comme ça c'est dynamique).

        :param item_id: id de l'option (c'est un rectangle) à rajouter au radiobutton
        """
        tags = list(self.canvas.gettags(item_id))
        tags[GROUP_TAG_INDEX] = self.group_tag
        self.canvas.itemconfigure(item_id, tags=tags)


class RadiobuttonsSupervisor:

    """
    Cette classe servira à gérer les différents radiobutton sur le canvas
    """
    def __init__(self, canvas: HighlightCanvas):
        self.current_group_id = 0
        self.canvas = canvas
        self.radiobuttons: dict[str: Radiobutton] = {

        }

    def add(self, *radiobutton_items_id: int) -> Radiobutton:
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

    def add_option(self, group_tag: str, option_id: int):
        """
        Méthode qui ajoute l'option option_id au radiobutton indexé au group_tag.
        Pour cela, il suffit juste d'ajouter un tag qui regroupera l'option avec le reste.
        """
        tags = list(self.canvas.gettags("active"))
        tags[GROUP_TAG_INDEX] = group_tag

        self.canvas.itemconfigure(option_id, tags=tags)
