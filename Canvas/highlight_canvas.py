
from tkinter import Canvas

from parameter import *
from Canvas.Radiobutton import RadiobuttonsSupervisor


class HighlightCanvas(Canvas):
    def __init__(self, master=None, cnf=None, **kw):
        # C'est PyCharm qui me dit de mettre ça au lieu de cnf={} directement dans les arguments donc...
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        self.tag_highlight = {
            MAP_TAG: self.highlight_square,
            CLICKABLE_TAG: self.highlight_clickable,
            TOGGLEABLE_TAG: self.highlight_toggleable,
            HIGHLIGHT_BUTTON_TAG: self.highlight_button,
            NOTHING_TAG: dummy
        }

        self.tag_unhighlight = {
            MAP_TAG: self.unhighlight_square,
            CLICKABLE_TAG: self.unhighlight_clickable,
            TOGGLEABLE_TAG: dummy,
            HIGHLIGHT_BUTTON_TAG: self.unhighlight_button,
            NOTHING_TAG: dummy
        }

        # Cette variable repertoriera tous les id de texts et leur rectangle associé.
        # ça permet de savoir, quand on veut highlight un rectangle après avoir cliqué sur un texte,
        # sur quel rectangle est le texte
        self.text_id_in_rectangle_id = {

        }

        # Comme le dictionnaire qui sert à récupérer le rectangle depuis le texte et inversement. Celui-ci servira
        # à récupérer l'id du rectangle du fond à partir du rectangle par dessus (pour l'highlight du bouton)
        self.get_rect_border_id_from_inner_id = {

        }

        self.radiobuttons = RadiobuttonsSupervisor(self)
        self.add_radiobutton = self.radiobuttons.add

    def highlight_square(self, toward_coor: tuple = None):
        """
        J'aimerai que le carré se raptessisse, jusqu'à être de moitié de la taille initiale, mais progressivement
        :return:
        """
        coords = tuple(self.coords("highlight"))
        if not coords:
            return

        x0, y0, x1, y1 = coords
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)

        if not toward_coor:
            # Facteur de rapetissage
            k = 0.7
            center_x = int(x0 + x1) >> 1
            center_y = int(y0 + y1) >> 1

            new_x0 = int(center_x - (center_x - x0) * k)
            new_y0 = int(center_y - (center_y - y0) * k)

            # Sans le + 1 c'est disproportionné c'est bizarre
            new_x1 = int(center_x + (x1 - center_x) * k) + 1
            new_y1 = int(center_y + (y1 - center_y) * k) + 1
            toward_coor = (new_x0, new_y0, new_x1, new_y1)

        self.coords(
            "highlight",
            abs(toward_coor[0] - x0) // 2 + 1 + x0,
            abs(toward_coor[1] - y0) // 2 + 1 + y0,
            -(abs(toward_coor[2] - x1) // 2 + 1) + x1,
            -(abs(toward_coor[3] - y1) // 2 + 1) + y1
        )

        """self.coords(
            "active",
            (toward_coor[0] + x0) // 2 + 1,
            (toward_coor[1] + y0) // 2 + 1,
            (toward_coor[2] + x1) // 2 + 1,
            (toward_coor[3] + y1) // 2 + 1
        )"""

        if coords != toward_coor:
            self.after(10, self.highlight_square, toward_coor)

    def unhighlight_square(self):
        """
        On récupère les coordonnées du carré au dessus, et grâce à ça on sait où placer le carré sélectionné
        :return:
        """
        # Si un carré est tout en haut est cliqué, alors prendre le carré d'en dessous
        id_carre_clicked = self.find_withtag("highlight")[0]

        if id_carre_clicked <= CARRE_PAR_LIGNE:
            # Carré du dessous
            x0, y0, x1, y1 = self.coords(id_carre_clicked + CARRE_PAR_LIGNE)
            self.coords("highlight", x0, y0 - SPS, x1, y0)

        else:
            # Coordonnées du carré au dessus, et on rajoute juste 50 aux ordonnées pour le placer en dessous
            x0, y0, x1, y1 = self.coords(id_carre_clicked - CARRE_PAR_LIGNE)
            self.coords("highlight", x0, y1, x1, y1 + SPS)

    def highlight_clickable(self): self.itemconfigure("highlight", fill=fill_brighter[self.gettags("highlight")[COLOR_TAG_INDEX]])
    def unhighlight_clickable(self): self.itemconfigure("highlight", fill=self.gettags("highlight")[COLOR_TAG_INDEX])
    def highlight_toggleable(self): self.radiobuttons.toggle_switch_option(self.gettags("highlight")[GROUP_TAG_INDEX], self.find_withtag("highlight")[0])

    def highlight_button(self):
        """
        Méthode qui va être trigger lors de l'highlight du bouton
        """
        self.itemconfig(self.get_rect_border_id_from_inner_id[self.find_withtag("highlight")[0]], outline="#CCCCCC")     # Bord éclairé
        self.itemconfig("highlight", outline="grey")       # Bord interne clair
        self.itemconfigure("highlight", fill=self.gettags("highlight")[COLOR_TAG_INDEX])

    def unhighlight_button(self):
        """
        Méthode qui va être trigger lors de l'unhighlight du bouton
        """
        self.itemconfig(self.get_rect_border_id_from_inner_id[self.find_withtag("highlight")[0]], outline="darkgrey")  # Bord plus sombre
        self.itemconfig("highlight", outline="black")      # Bord interne foncé
        self.itemconfig("highlight", fill=fill_brighter[self.gettags("highlight")[COLOR_TAG_INDEX]])      # Bord interne foncé
