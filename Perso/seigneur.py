from Perso.vassal import Vassal
from Perso.noble import Noble


class Seigneur(Noble):
    """
    Le seigneur est un noble qui a sous ses ordres d'autres nobles qu'il soumet à l'impôt
    """

    def __init__(self, pnom: str, pres: int, parg: int, index: int):
        Noble.__init__(self, pnom, pres, parg, index)

        # Liste des vassaux du seigneur (nobles sous les ordres du seigneur)
        self._liste_nobles: list[Vassal] = []

        # PYREVERSE
        #self._liste_nobles = Vassal()

    @property
    def liste_nobles(self):
        return self._liste_nobles

    @liste_nobles.setter
    def liste_nobles(self, liste_nobles: list[Vassal]):
        self._liste_nobles = liste_nobles

    @property
    def effectif_armee(self) -> int:
        armee = len(self._liste_soldats) + len(self._liste_nobles)
        for vassal in self._liste_nobles:
            armee += len(vassal.liste_soldats)
        return armee

    def prend_impot_noble(self, indice_noble : int):
        """
        Ajoute aux ressources du seigneur les impot perçu pour le noble se trouvant à l'indice indice_noble de sa liste de nobles sous ses ordres
        """
        impot =  self._liste_nobles[indice_noble].payer_impot()
        self._argent += impot[0]
        self._ressources += impot[1]

    def imposer(self, l_villages : list[int], l_noble : list[int] = None):
        """
        Methode qui permet d'imposer un village et/ou un noble suivant les choix qu'aura fait le joueur/bot

        :param l_villages : liste d'id des villages choisis
        :param l_noble : liste d'id des nobles choisis
        """
        for inoble in l_noble :
            self.prend_impot_noble(inoble)

        Noble.imposer(self, l_villages)