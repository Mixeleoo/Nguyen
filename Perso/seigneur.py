from Perso.noble import Noble


class Seigneur(Noble):
    """
    Le seigneur est un noble qui a sous ses ordres d'autres nobles qu'il soumet à l'impôt
    """
    def __init__(self, pnom: str, pres: int, parg: int):
        Noble.__init__(self, pnom, pres, parg)

        # Liste des vassaux du seigneur (nobles sous les ordres du seigneur)
        self.liste_nobles = ListNoble()

    def prend_impot(self):
        for noble in self.liste_nobles:
            self._ressources += noble.payer_impot()


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