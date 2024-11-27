from Perso.noble import Noble
from Perso.village import Village
from parameter import nom_aleatoire


class Seigneur(Noble):
    """
    Le seigneur est un noble qui a sous ses ordres d'autres nobles qu'il soumet à l'impôt
    """

    def __init__(self, pnom: str, pres: int, parg: int):
        Noble.__init__(self, pnom, pres, parg)

        # Liste des vassaux du seigneur (nobles sous les ordres du seigneur)
        self._liste_nobles: list[Noble] = []
        # Dictionnaire des villages avec la structure suivante : identifiant_village : int -> Village
        self._dico_villages: dict[int: Village] = {}
        self._liste_soldats: list[Soldat] = []

    def prend_impot(self):
        """
        Ajoute aux ressources du seigneur les impot perçu pour chaque noble sous ses ordres
        """
        Noble.prend_impot(self)  # recupération de l'impôt de ses roturiers

        for noble in self._liste_nobles:
            self._ressources += noble.payer_impot()

    def creer_village(self, pid: int):
        """
        Crée un village et l'ajoute à la liste des villages dirigés par le seigneur (dictionnaire)
        """
        nom = nom_aleatoire()
        self._dico_villages[pid] = Village(pid, nom, self._nom)

    def nourrir_soldats(self):
        """
        Retourne 0 si le seigneur a assez de ressources pour nourrir ses soldats
        Retourne le nombre de ressources manquantes sinon (ce sera le nombre de soldats qui seront morts de faim)
        """
        deces = 0
        nb_soldats = len(self._liste_soldats)  # effectif armée

        if self._ressources < nb_soldats:
            deces = nb_soldats - self._ressources
            self._liste_soldats = self._liste_soldats[:self._ressources]

        return deces


class ListNoble(list):
    """
     Liste qui ne peut contenir que des Nobles
     """

    def __new__(cls, *args, **kwargs):
        for elt in args:
            if not isinstance(elt, Noble):
                raise TypeError(f"ListNoble n'accepte que des Nobles")

        list.__new__(*args, **kwargs)

    def __iadd__(self, other):
        if not isinstance(other, Noble):
            raise TypeError(f"ListNoble n'accepte que des Nobles")

        self.append(other)

    def __radd__(self, other):
        if not isinstance(other, Noble):
            raise TypeError(f"ListNoble n'accepte que des Nobles")

        self.append(other)

    def append(self, __object):
        if not isinstance(__object, Noble):
            raise TypeError(f"ListNoble n'accepte que des Nobles")

        else:
            list.append(self, __object)