
from .vassal import Vassal


class Noble(Vassal):

    """
    Un noble est une personne qui contôle des roturiers (sous forme d'une liste de roturiers)
    il est également soumis à un impôt s'il est vassal d'un seigneur (10%).
    Chaque noble aura un nombre de PA intitialisé à 10 et qui sera modifié au fur et à mesure des action du jeu
    en cours de partie
    Il sera réinitialisé à chaque fin de tour
    """
    def __init__(self, pnom: str, pres: int, parg: int, index: int, couleur: str = None):
        Vassal.__init__(self, pnom, pres, parg, index, couleur)

    def soumettre(self, pnoble: 'Noble', pargent : int, press : int):
        """
        Méthode qui permet de déterminer si un noble accepte de se soumettre ou non
        Ce choix se fera en fonction de la taille de l'armée et de la quantité de ressources et d'argent que l'on offre au nobles à soumettre
        Si la quantité de ressources et d'argent proposés sont strictement supérieur à 25% de ce que le noble à déjà OU
        que la taille de son armée est inférieur à celle du noble qui soumet : la fonction return True
        Sinon : False

        :param pnoble: Noble souhaitant soumettre un autre noble
        :param pargent: Quantité d'argent offerte au noble
        :param press: Quantité de ressources offertes au noble
        :return : True si le noble accepte de devenir vassal, False sinon
        """
        self.retirer_pa(4)

        return (pnoble.argent * 0.25 < pargent and pnoble.ressources * 0.25 < press) or (len(pnoble.liste_soldats) < len(self.liste_soldats))
