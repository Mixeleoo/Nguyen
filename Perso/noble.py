from Perso.roturier import Roturier
from personne import Personne


class Noble(Personne):

    """
    Un noble est une personne qui contôle des roturiers (sous forme d'une liste de roturiers)
    il est également soumis à un impôt s'il est vassal d'un seigneur (10%)
    """
    def __init__(self, pnom: str, pres: int, parg: int):
        Personne.__init__(self, pnom, pres, parg)
        self._pourcentage_impot = 10

        # Les roturiers que possède le noble
        self.liste_roturiers = ListRoturier()

    def prend_impot(self):
        """
        Ajoute aux ressources un pourcentage fixe en fonction de l'impôt auquel sont soumis les roturiers sous ses ordres
        """
        for roturier in self.liste_roturiers:
            self._ressources += roturier.payer_impot()



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


