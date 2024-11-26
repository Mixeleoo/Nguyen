from Perso.personne import Personne
from random import randint


class Roturier(Personne):
    """
    Un roturier est une personne qui a en plus une capacité de prodcution qui lui est propre (minimum de 2)
    il a également un pourcentage d'impôt prédéfinit (25%)
    """
    def __init__(self, pnom: str, pres: int, parg: int, cdp: int):
        Personne.__init__(self, pnom, pres, parg)
        self._cdp = cdp
        self._pourcentage_impot = 25

    def produit(self) -> int:
        """
        produit ajoute à ressource la capacité de production (CDP) annuelle (chaque tour du jeu)
        la quantité ajoutée aux ressources recoltées par le roturier est calculé aléatoirement entre la moitié de sa capacité
        et sa capacité complète
        """
        production = randint(self._cdp // 2, self._cdp)
        self._ressources += production
        return production
