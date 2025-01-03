
import random

from Perso.ecclesiastique import Ecceclesiastique


class Eglise :
    _noms_eglises = [
        "Église Saint-Pierre", "Église Notre-Dame", "Église Sainte-Marie", "Église Saint-Jean-Baptiste",
        "Église Saint-Paul", "Église Saint-Louis", "Église Saint-Augustin", "Église Saint-Antoine",
        "Église Sainte-Catherine", "Église Saint-Joseph", "Église Saint-François", "Église Saint-André",
        "Église Sainte-Thérèse", "Église Saint-Honoré", "Église Saint-Sulpice", "Église Sainte-Claire",
        "Église Saint-Denis", "Église Saint-Alexandre", "Église Sainte-Anne", "Église Saint-Michel",
        "Église Saint-Roch", "Église Sainte-Rita", "Église Saint-Étienne", "Église Sainte-Élisabeth",
        "Église Saint-Jean-de-Latran", "Église Saint-Martin", "Église Sainte-Bernadette", "Église Saint-Benoît",
        "Église Saint-Marc", "Église Sainte-Madeleine", "Église Saint-Basile", "Église Saint-Hubert",
        "Église Saint-Pierre-et-Saint-Paul", "Église Sainte-Véronique", "Église Saint-Augustin-de-Canterbury",
        "Église Saint-Jean-de-Dieu", "Église Saint-Cyr",  "Église Sainte-Victoire", "Église Saint-Hélier",
        "Église Saint-Léon", "Église Sainte-Famille", "Église Saint-Georges", "Église Saint-Jacques",
        "Église Sainte-Rose", "Église Saint-Nicolas", "Église Sainte-Marthe", "Église Saint-Jean-Eudes",
        "Église Saint-Étienne-de-Montluc", "Église Saint-Dominique", "Église Saint-Louis-de-Gonzague",
        "Église Saint-Alban"
    ]

    """
    Une eglise est composée d'un prêtre qui lui est associé
    """
    def __init__(self, ppretre : Ecceclesiastique, pnom : str = None):
        self.pretre = ppretre

        if pnom is None:
            self.nom = random.choice(self._noms_eglises)
            Eglise._noms_eglises.remove(self.nom)

        else:
            self.nom = pnom
