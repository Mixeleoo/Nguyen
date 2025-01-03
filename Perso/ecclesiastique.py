
from .personne import Personne
from random import randint


class Ecceclesiastique(Personne):
    """
    Un eccleasiatique est une figure religieuse qui sera amené dans un village dès le construction d'une église, c'est lui qui en aura
    la direction.
    Il possède un don choisit aléatoirement parmis : 1-Amelioration de l'humeur, 2-Augmentation éspérance de vie, 3-Augementation Production,...)
    """
    def __init__(self, pnom: str):
        Personne.__init__(self, pnom, 0, 0)
        self.don = randint(1, 3)