from Perso.personne import Personne
from Perso.soldat import Soldat
from Territoire.village import Village
from parameter import prenom_aleatoire


class Noble(Personne):

    """
    Un noble est une personne qui contôle des roturiers (sous forme d'une liste de roturiers)
    il est également soumis à un impôt s'il est vassal d'un seigneur (10%).
    Chaque noble aura un nombre de PA intitialisé à 10 et qui sera modifié au fur et à mesure des action du jeu
    en cours de partie
    Il sera réinitialisé à chaque fin de tour
    """
    def __init__(self, pnom: str, pres: int, parg: int):
        Personne.__init__(self, pnom, pres, parg)
        self._taux_impot = 0.10
        self._pa = 10

        # Dictionnaire des villages que le noble dirige avec la structure suivante : identifiant_village : int -> Village
        # Servira à accéder à la liste de Roturiers que le noble possède
        self._dico_villages: dict[int, Village] = {}

        # Liste des soldats sous les ordres du noble
        self._liste_soldats: list[Soldat] = []

    @property
    def pa(self) -> int:
        return self._pa

    def retirer_pa(self, qt: int):
        self._pa -= qt

    @property
    def dico_villages(self):
        return self._dico_villages

    @dico_villages.setter
    def dico_villages(self, dico_villages: dict[int, Village]):
        self._dico_villages = dico_villages

    @property
    def liste_soldats(self):
        return self._liste_soldats

    @liste_soldats.setter
    def liste_soldats(self, liste_soldats: list[Soldat]):
        self._liste_soldats = liste_soldats

    @property
    def bonheur_general(self):
        """
        Retourne la moyenne du bonheur dans tous les villages dirigés par le noble
        """
        bonheur = 0
        nb_village = 0
        for village in self._dico_villages.values() :
            bonheur += village.bonheur_general
            nb_village += 1
        return round(bonheur/nb_village,2)

    @property
    def population(self):
        pop = 0
        for village in self._dico_villages.values():
            pop += village.population

        return pop

    @property
    def effectif_armee(self) -> int:
        return len(self._liste_soldats)

    def payer_impot(self):
        """
        Méthode d'impôt en fonction du pourcentage d'impot attribué noble
        Retourne un tuple de la quantité d'argent et de ressources prises au noble
        et enlève cette quantité de l'argent ET des ressources de ce noble
        Une partie de son bonheur lui sera enlevé à l'issu de cette action
        """
        imp_arg = self._argent * self._taux_impot
        imp_ress = self._ressources * self._taux_impot

        self._argent -= imp_arg
        self._ressources -= imp_ress

        return imp_arg, imp_ress

    def prend_impot_village(self, pid_village: int) -> tuple[int, int]:
        """
        Ajoute aux ressources du noble les impot perçu pour chaque roturier sous ses ordres dans le village mis en paramètre
        """
        impot_total_arg = 0
        impot_total_res = 0

        for roturier in self._dico_villages[pid_village].liste_roturier :
            impot_percu = roturier.payer_impot() # recupération du tuple (roturier.argent, roturier.ressources)
            impot_total_arg += impot_percu[0]
            impot_total_res += impot_percu[1]

        self._argent += impot_total_arg
        self._ressources += impot_total_res

        return impot_total_arg, impot_total_res

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
        return True
        if(pnoble.argent * 0.25 < pargent and pnoble.ressources * 0.25 < press) or (len(pnoble.liste_soldats) < len(self.liste_soldats)) :
            return True
        else :
            return False


    def ajouter_village(self, pid: int, nom: str):
        """
        Crée un village et l'ajoute à la liste des villages dirigés par le seigneur (dictionnaire)
        """
        self._dico_villages[pid] = Village(pid, nom)

    def ajout_soldat(self, peffectif: int):
        """
        Méthode qui ajouter peffectif soldats dans sa liste de soldats

        :param peffectif:
        """
        for _ in range(peffectif):
            self._liste_soldats += [Soldat(prenom_aleatoire())]

    def nourrir_soldats(self) -> int:
        """
        Retourne zéro si le seigneur a assez de ressources pour nourrir ses soldats.
        Retourne le nombre de ressources manquantes sinon (ce sera le nombre de soldats qui seront morts de faim)
        """
        deces = 0
        nb_soldats = len(self._liste_soldats) # effectif armé

        if self._ressources < nb_soldats:
            deces = nb_soldats - self._ressources
            self._liste_soldats = self._liste_soldats[:self._ressources]

        return deces
