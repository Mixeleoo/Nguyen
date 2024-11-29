from random import randint

from Perso.paysan import Paysan
from Perso.roturier import Roturier
from parameter import prenom_aleatoire

from random import randint

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

        # Les roturiers que possède le noble
        self._liste_roturier = ListRoturier()


    
    def ajouter_villageois(self,pvillageois : Literal["paysan", "artisan"], effectif : int) :
        """
        Cette fonction prend en paramètre le type de villageois qui sera ajouté et leur nombre
        Elle servira lorsque le joueur choisira l'action 'Immigration'
        """
        for v in range(effectif) :
            prenom = prenom_aleatoire()
            argent = randint(1,5)
            capacite_prod = randint(18,22)
            if pvillageois == "artisan" :
                self._liste_roturier += [Roturier(prenom,argent,capacite_prod)]
            elif pvillageois == "paysan" :
                self._liste_roturier += [Paysan(prenom, capacite_prod)]



class ListRoturier(list):
    """
    Liste qui ne peut contenir que des Roturiers
    """
    def __new__(cls, *args, **kwargs):
        for elt in args:
            if not isinstance(elt, Roturier):
                raise TypeError(f"ListRoturier n'accepte que des Roturiers")

        list.__new__(*args, **kwargs)

    def __iadd__(self, other):
        if not isinstance(other, Roturier):
            raise TypeError(f"ListRoturier n'accepte que des Roturiers")

        self.append(other)

    def __radd__(self, other):
        if not isinstance(other, Roturier):
            raise TypeError(f"ListRoturier n'accepte que des Roturiers")

        self.append(other)

    def append(self, __object):
        if not isinstance(__object, Roturier):
            raise TypeError(f"ListRoturier n'accepte que des Roturiers")

        else:
            list.append(self, __object)