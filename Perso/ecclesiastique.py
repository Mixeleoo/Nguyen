
import random

from .personne import Personne


class Ecceclesiastique(Personne):
    _noms_pretres = [
    "Père Augustin", "Père Bernard", "Père Thomas", "Père François", "Père Dominique", "Père Anselme",
        "Père Bonaventure", "Père Grégoire", "Père Pierre", "Père Benoît", "Père Grégoire", "Père Jean",
        "Père Athanase", "Père Jérôme", "Père Ignace", "Père Cyprien", "Père Hilaire", "Père Ambroise", "Père Léon",
        "Père Isidore", "Père Martine", "Père Nicolas", "Père Jean", "Père François", "Père Pierre", "Père Vincent",
        "Père Louis", "Père Clément", "Père Polycarpe", "Père Ephrem", "Père Fulgence", "Père Augustin",
        "Père Grégoire", "Père Firmin", "Père Remi", "Père Évode", "Père Richard", "Père Wenceslas", "Père Thomas",
        "Père Boniface", "Père Lambert", "Père Gérard", "Père Hyacinthe", "Père Albin", "Père Martin",
        "Père Gaudentius", "Père Jean", "Père Théodore", "Père Basil", "Père Sévérin"
    ]
    """
    Un eccleasiatique est une figure religieuse qui sera amené dans un village dès le construction d'une église, c'est lui qui en aura
    la direction.
    Il possède un don choisit aléatoirement parmis : 1-Amelioration de l'humeur, 2-Augmentation éspérance de vie, 3-Augementation Production,...)
    """
    def __init__(self, pnom: str = None):
        Personne.__init__(self, 0, 0, pnom)
        self.don = random.randint(1, 3)

        if pnom is None:
            self._nom = random.choice(Ecceclesiastique._noms_pretres)
