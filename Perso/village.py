from Perso.noble import Noble
from Perso.seigneur import ListNoble, Seigneur
from Perso.noble import ListRoturier
from Perso.paysan import Paysan
from Perso.roturier import Roturier
from parameter import prenom_aleatoire

from typing import Literal

class Village :
    """
    Un village est représenté par son id (qui servira pour l'associer à son emplacement sur la map)
    par sa population (une liste de roturiers, de nobles et de soldats) ainsi que par son dirigeant (un seigneur)
    """
    def __init__(self, pid : int, nom : str, nom_proprio: str) :
        self._nom = nom
        self._identifiant = pid
        self._nom_proprio = nom_proprio
        self._liste_roturier = ListRoturier()

    
    def ajouter_villageois(self,pvillageois : Literal["paysan", "artisan"], effectif : int) :
        """
        
        """
        for v in range(effectif) :
            prenom = prenom_aleatoire()
            if pvillageois == "artisan" :
                self._liste_roturier


