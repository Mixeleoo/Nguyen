
from tkinter import Canvas


class HighlightCanvas(Canvas):
    def __init__(self, master=None, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        # Dictionnaires définissant les comportements de mise en surbrillance
        self.tag_highlight = {
            "MAP_TAG": self.highlight_square,
            "CLICKABLE_TAG": self.highlight_clickable,
            "TOGGLEABLE_TAG": self.highlight_togleable,
            "NOTHING_TAG": lambda: None
        }

        self.tag_unhighlight = {
            "MAP_TAG": self.unhighlight_square,
            "CLICKABLE_TAG": self.unhighlight_clickable,
            "TOGGLEABLE_TAG": lambda: None,
            "NOTHING_TAG": lambda: None
        }

        # Cette variable repertoriera tous les id de texts et leur rectangle associé.
        # ça permet de savoir, quand on veut highlight un rectangle après avoir cliqué sur un texte,
        # sur quel rectangle est le texte
        self.text_id_in_rectangle_id = {

        }

    def highlight_square(self, toward_coor: tuple = None):
        """
        Met en surbrillance un carré.
        :param toward_coor: Coordonnées vers lesquelles le carré se redimensionne.
        """
        pass

    def unhighlight_square(self):
        """
        Annule la surbrillance d'un carré.
        """
        pass

    def highlight_clickable(self):
        """
        Met en surbrillance un élément "cliquable".
        """
        pass

    def unhighlight_clickable(self):
        """
        Annule la surbrillance d'un élément "cliquable".
        """
        pass

    def highlight_togleable(self):
        """
        Met en surbrillance un élément "toggleable".
        """
        pass
