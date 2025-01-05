
import random

from .personne import Personne
from Territoire.terre import Terre
from parameter import capacite_prod_terre

prenoms_roturiers = [
    "Alaric", "Béranger", "Adélaïde", "Eudes", "Clotilde", "Léonard", "Ysabeau", "Godefroy", "Agnès", "Hugues",
    "Géraldine", "Baudoin", "Armand", "Isabeau", "Aimé", "Perrin", "Tanguy", "Clothilde", "Florent", "Sygarde",
    "Gildas", "Théodora", "Renaud", "Béatrice", "Geoffroy", "Hildegarde", "Roland", "Mathilde", "Thierry",
    "Gertrude", "Bernard", "Edwige", "Louis", "Aubrée", "Gérald", "Renée", "Frédéric", "Alix", "Frédérique",
    "Foulques", "Hélène", "Henri", "Aude", "Mathieu", "Judith", "Galeran", "Constance", "Géraud", "Solange",
    "Renaude", "Esteban", "Eustache", "Brunehaut", "Déodat", "Lancelot", "Lison", "Eléonore", "Sénéchal",
    "Aldegarde", "Béatrice", "Térence", "Iseult", "Roger", "Pépin", "Blanche", "Godefroy", "Tiberius", "Hildebrand",
    "Eadric", "Sigismond", "Gaétane", "Éléonore", "Thibault", "Isolde", "Géron", "Luce", "Guy", "Sibylle",
    "Bertrand", "Mathurin", "Lothaire", "Théodore", "Hermenegilde", "Aldric", "Adeline", "Justine", "Yvain",
    "Guibert", "Pétronille", "Floriane", "Valérie", "Ulric", "Adhémar", "Bérengère", "Gauthier", "Adalbert",
    "Lambert", "Gervais", "Clovis", "Eugénie", "Héribert", "Philomène", "Mathias", "Frédégonde", "Hildegarde",
    "Édouard", "Pétronille", "Arsène", "Carlotta", "Geoffroy", "Aldebert", "Aymon", "Béna", "Géraldine", "Alvéran",
    "Théophane", "Maud", "Roland", "Odilon", "Arnaud", "Adèle", "Maïeul", "Cécile", "Thierry", "Milburge",
    "Madeleine", "Hildegarde", "Olivier", "Rémacle", "Hélier", "Hélène", "Eberhard", "Côme", "Eustache", "Éva",
    "Grégoire", "Aimée", "Fulbert", "Agnès", "Baudouin", "Désiré", "Arnould", "Sybille", "Agathe", "Enguerrand",
    "Yvette", "Roderick", "Ivo", "Guillaume", "Otton", "Léon", "Claire", "Dido", "Ernestine", "Clément", "Irène",
    "Gauthier", "Béatrix", "Anselme", "Godefroy", "Quentin", "Madeleine", "Liévin", "Olric", "Odon", "Géraud",
    "Venance", "Alix", "Eloise", "Engelbert", "Gauthier", "Raoul", "Théobald", "Perrine", "Ethelred", "Gisèle",
    "Mathilde", "Thierry", "François", "Orabel", "Sigismond", "Léonidas", "Godfrey", "Alice", "Audebert", "Romain",
    "Berthe", "André", "Maurin", "Agnès", "Godefroy", "Norbert", "Millicent", "Eulalie", "Bertrade", "Hermenegilde",
    "Louis", "Gilbert", "Beatrix", "Gildas"
]

class Roturier(Personne):
    """
    Un roturier est une personne qui a en plus une capacité de prodcution qui lui est propre (minimum de 2)
    il a également un taux d'impôt prédéfinit (25%)
    Une terre lui est également associée pour qu'il puisse y récupérer ses récoltes
    """

    _prenoms_perso = prenoms_roturiers.copy()

    @classmethod
    def default(cls):
        cls._prenoms_perso = prenoms_roturiers.copy()

    def __init__(self,terre : Terre, pnom: str = None, parg: int = None, cdp: int = None):
        if parg is None: parg = random.randint(1, 5)
        if cdp is None: cdp = random.randint(18, 22)

        Personne.__init__(self, 0 , parg, pnom)

        if pnom is None:
            self._nom = random.choice(Roturier._prenoms_perso)

        self.terre = terre
        self.cdp = int(cdp * capacite_prod_terre[terre.type])
        self._taux_impot = 0.25

    def produit(self, facteur : int) -> int:
        """
        Produit ajoute aux ressources la capacité de production (CDP) annuelle (chaque tour du jeu)
        la quantité ajoutée aux ressources recoltées par le roturier est calculé aléatoirement entre la moitié de sa capacité
        et sa capacité complète
        """
        production = random.randint(self.cdp // 2, self.cdp)
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
        lancer_commerce = random.randint(0,100)
        if self.ressources <= lancer_commerce :
            echange = int(self.ressources * 0.50) # si commerce alors vente de 50% des ressources
            self.gestion_ressources(-echange)
            self.gestion_argent(echange)
            self.gerer_bonheur(1)

    def gerer_bonheur(self,pt : int):
        """
        Méthode qui permet aux roturiers de gagner des points de bonheur
        """
        if self.bonheur + pt > 10 :
            self.bonheur = 10
        elif self.bonheur + pt < 0 :
            self.bonheur = 0
        else :
            self.bonheur += pt

