from Perso.roturier import Roturier
from personne import Personne


class Noble(Personne):

    """
    Un noble est une personne qui contôle des roturiers (sous forme d'une liste de roturiers)
    il est également soumis à un impôt s'il est vassal d'un seigneur (10%)
    """
    def __init__(self, pnom: str, pres: int, parg: int):
        Personne.__init__(self, pnom, pres, parg)
        self._taux_impot = 0.10

        # Les roturiers que possède le noble
        self.liste_roturiers = ListRoturier()

    def prend_impot(self):
        """
        Ajoute aux ressources du noble les impot perçu pour chaque roturiers sous ses ordres
        """
        for roturier in self.liste_roturiers:
            impot_percu = roturier.payer_impot() # recupération du tuple (roturier.argent, roturier.ressources)
            self._argent += impot_percu[0]
            self._ressources += impot_percu[1]

            # Dictionnaire des villages que le noble dirige avec la structure suivante : identifiant_village : int -> Village
            self._dico_villages: dict[int: Village] = {}
            self._liste_soldats: list[Soldat] = []

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