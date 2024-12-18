from Perso.vassal import Vassal
from Perso.noble import Noble


class Seigneur(Noble):
    """
    Le seigneur est un noble qui a sous ses ordres d'autres nobles qu'il soumet à l'impôt
    """

    def __init__(self, pnom: str, pres: int, parg: int):
        Noble.__init__(self, pnom, pres, parg)

        # Liste des vassaux du seigneur (nobles sous les ordres du seigneur)
        self._liste_nobles: list[Vassal] = []

    @property
    def liste_nobles(self):
        return self._liste_nobles

    @liste_nobles.setter
    def liste_nobles(self, liste_nobles: list[Vassal]):
        self._liste_nobles = liste_nobles

    @property
    def effectif_armee(self) -> int:
        return len(self._liste_soldats) + len(self._liste_nobles)

    def prend_impot_noble(self, indice_noble : int):
        """
        Ajoute aux ressources du seigneur les impot perçu pour le noble se trouvant à l'indice indice_noble de sa liste de nobles sous ses ordres
        """
        impot =  self._liste_nobles[indice_noble].payer_impot()
        self._argent += impot[0]
        self._ressources += impot[1]