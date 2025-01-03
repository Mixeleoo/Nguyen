
from random import randint

from .personne import Personne
from Territoire.terre import Terre
from parameter import prenom_aleatoire, capacite_prod_terre



class Roturier(Personne):
    """
    Un roturier est une personne qui a en plus une capacité de prodcution qui lui est propre (minimum de 2)
    il a également un taux d'impôt prédéfinit (25%)
    Une terre lui est également associée pour qu'il puisse y récupérer ses récoltes
    """
    def __init__(self,terre : Terre, pnom: str = None, parg: int = None, cdp: int = None):
        if pnom is None: pnom = prenom_aleatoire()
        if parg is None: parg = randint(1, 5)
        if cdp is None: cdp = randint(18, 22)


        Personne.__init__(self, pnom, 0 , parg)
        self.terre = terre
        self.cdp = int(cdp * capacite_prod_terre[terre.type])
        self._taux_impot = 0.25

    def produit(self, facteur : int) -> int:
        """
        Produit ajoute aux ressources la capacité de production (CDP) annuelle (chaque tour du jeu)
        la quantité ajoutée aux ressources recoltées par le roturier est calculé aléatoirement entre la moitié de sa capacité
        et sa capacité complète
        """
        production = randint(self.cdp // 2, self.cdp)
        self.gestion_ressources(production//facteur)
        return production

    def payer_impot(self):
        """
        Méthode d'impôt en fonction du pourcentage d'impot attribué roturier
        Retourne un tuple de la quantité d'argent et de ressources prises au roturier
        et enlève cette quantité de l'argent ET des ressources de ce roturier
        Le roturier imposé perdra une partie de son bonheur au cours de cette action (1 point de bonheur)
        """

        imp_arg = int(self._argent * self._taux_impot)
        imp_ress = int(self._ressources * self._taux_impot)

        self._argent -= imp_arg
        self._ressources -= imp_ress

        if self.bonheur - 1 < 0 :
            self.bonheur = 0
        else :
            self.bonheur -= 1

        return imp_arg, imp_ress

    def commercer(self):
        """
        Méthode qui permet à un roturier de commercer en fonction de sa quantité de ressources
        L'échange ne se fera pas avec d'autre roturier, mais avec un commerçant imaginaire que nous simulerons
        Si le roturier possède moins de ressources que le nombre qui sera tiré au hasard pour décider de s'il commerce, alors il peut vendre
        des ressources contre de l'argent, sinon rien ne se passe
        """
        lancer_commerce = randint(0,100)
        if self.ressources <= lancer_commerce :
            echange = int(self.ressources * 0.50) # si commerce alors vente de 50% des ressources
            self.gestion_ressources(-echange)
            self.gestion_argent(echange)
