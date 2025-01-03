
import random
from typing import Literal

from Perso.personne import Personne
from Perso.soldat import Soldat
from Territoire import Village, RevolteInfo
from parameter import prenom_aleatoire, ActionCost, ACTIONS_NAME_COST

class Vassal(Personne):
    couleurs: list[str] = ["#125ee0", "#b01288", "#b01241", "#680b7d", "#0b7d7d", "#d98634"]

    """
    Un noble est une personne qui contôle des roturiers (sous forme d'une liste de roturiers)
    il est également soumis à un impôt s'il est vassal d'un seigneur (10%).
    Chaque noble aura un nombre de PA intitialisé à 10 et qui sera modifié au fur et à mesure des action du jeu
    en cours de partie
    Il sera réinitialisé à chaque fin de tour
    """
    def __init__(self, pnom: str, pres: int, parg: int, index: int, couleur: str = None):
        Personne.__init__(self, pnom, pres, parg)
        self._taux_impot = 0.10

        # Cet attribut servira à différencier les couleurs entre vassaux | nobles | seigneurs
        if not couleur:
            _couleur = random.choice(Vassal.couleurs)
            Vassal.couleurs.remove(_couleur)
            self.couleur = _couleur

        else:
            Vassal.couleurs.remove(couleur)
            self.couleur = couleur

        self._pa = 0
        self.reset_pa()

        self._id = index  # ça sera simplement l'index du noble dans la liste des joueurs CRÉE AU DEBUT DU JEU

        # Dictionnaire des villages que le noble dirige avec la structure suivante : identifiant_village : int -> Village
        # Servira à accéder à la liste de Roturiers que le noble possède
        self._dico_villages: dict[int, Village] = {}

        # Liste des soldats sous les ordres du noble
        self._liste_soldats: list[Soldat] = []

        # PYREVERSE
        #self._liste_soldats = Soldat()

    @property
    def id(self) -> int:
        return self._id

    @property
    def pa(self) -> int:
        return self._pa

    def retirer_pa(self, qt: int):
        self._pa -= qt

    def reset_pa(self):
        self._pa = 10

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

    def action_possible_pa(self, actioncost: ActionCost):
        return self.pa >= actioncost.pa

    def action_possible_argent(self, actioncost: ActionCost):
        return self.argent >= actioncost.argent

    def action_possible_ressources(self, actioncost: ActionCost):
        return self.ressources >= actioncost.ressources

    def action_possible(self, actioncost: ActionCost):
        return self.action_possible_pa(actioncost) and\
        self.action_possible_argent(actioncost) and\
        self.action_possible_ressources(actioncost)

    def payer_impot(self):
        """
        Méthode d'impôt en fonction du pourcentage d'impot attribué noble
        Retourne un tuple de la quantité d'argent et de ressources prises au noble
        et enlève cette quantité de l'argent ET des ressources de ce noble
        Une partie de son bonheur lui sera enlevé à l'issu de cette action
        """
        imp_arg = int(self._argent * self._taux_impot)
        imp_ress = int(self._ressources * self._taux_impot)

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

    def ajouter_village(self, pid: int, nom: str, l_terre : list[Literal["PLAIN", "MOUNTAIN", "LAKE", "FOREST"]]):
        """
        Crée un village et l'ajoute à la liste des villages dirigés par le seigneur (dictionnaire)
        """

        v = Village(pid, nom, l_terre)
        self._dico_villages[pid] = v
        return v

    def ajout_soldat(self, peffectif: int):
        """
        Méthode qui ajouter peffectif soldats dans sa liste de soldats

        :param peffectif:
        """
        for _ in range(peffectif):
            self._liste_soldats += [Soldat(prenom_aleatoire())]

            self.gestion_argent(-ACTIONS_NAME_COST["Soldat"].argent)
            self.retirer_pa(2)

    def nourrir_soldats(self) :
        """
        Retourne zéro si le seigneur a assez de ressources pour nourrir ses soldats.
        Retourne le nombre de ressources manquantes sinon (ce sera le nombre de soldats qui seront morts de faim)
        """
        deces = 0
        nb_soldats = len(self._liste_soldats) # effectif armé

        if self._ressources < nb_soldats:
            deces = nb_soldats - self._ressources
            self._liste_soldats = self._liste_soldats[:self._ressources]

        if deces > 0 :
            return f"{deces} soldats sont morts dans les rangs de {self.nom} dû au manque de vivre."
        else :
            return f""

    def nourrir_peuple(self):
        """
        Permet de nourrir tout le peuple d'un noble
        """
        nb_morts = 0
        for village in self.dico_villages.values() :
            nb_morts += village.nourrir_population()

        if nb_morts > 0:
            return f"{nb_morts} roturiers est(sont) mort(s) de faim dans le(s) village(s) de {self.nom}"
        else :
            return f""

    def reaction_revolte(self) -> list[RevolteInfo]:
        """
        Méthode lancée par le jeu après avoir cliqué sur fin de tour.
        Vérifie si des révoltes se produisent dans une ou plusieurs villages du joueur/bot
        """
        l_revoltes = []
        for village in list(self.dico_villages.values()) :
            l_revoltes.append(village.revolte(self.liste_soldats))

        return l_revoltes

    def construire_eglise(self, village_id: int):
        """
        Méthode pour construire une Église dans un village choisi

        :param village_id : id du village dans lequel le joueur veut construir une église
        """
        self.dico_villages[village_id].creer_eglise()

        self.retirer_pa(6)
        self.gestion_argent(-100)
        self.gestion_ressources(-50)

    def construire_village(self, village_id: int, nom: str, l_terre : list[Literal["PLAIN", "MOUNTAIN", "LAKE", "FOREST"]]):
        """
        Méthode qui va ajouter un village dans la liste de villages du joueur

        :param village_id : l'id du village (id du carré sur la map que le joueur aura selectionné
        :param nom: nom du village
        :param l_terre : liste des 8 terres entourant le village
        """

        self.retirer_pa(8)
        self.gestion_argent(-300)
        self.gestion_ressources(-150)

        print("ID emplacement :",village_id)
        return self.ajouter_village(village_id, nom, l_terre)

    def immigrer(self, village_id: int, type_v: Literal["paysan", "artisan"], effectif: int):
        """
        Méthode qui va ajouter au village (village_id) le nombre (effectif) de villageois (type_v)

        :param effectif : nombre de villageois désirés par le joueur
        :param type_v: type de villageois (PS : Literal["paysan", "artisan"] veut dire soit "paysan", soit "artisan" rien d'autre)
        :param village_id : l'id du village dans lequel les futurs villageois habiteront
        """

        print("choix nombre :", effectif)
        print("type_villageois :", type_v)
        print("choix village :", village_id)

        self.dico_villages[village_id].ajouter_villageois(type_v, effectif)

        if type_v == "paysan":
            self.retirer_pa(effectif)

        elif type_v == "artisan":
            self.retirer_pa(effectif*2)

    def imposer(self, l_villages : list[int], l_nobles: list[int] = None):
        """
        Methode qui permet d'imposer un village et/ou un noble suivant les choix qu'aura fait le joueur/bot

        :param l_villages : liste d'id des villages choisis
        :param l_nobles
        """

        for ivillage in l_villages :
            self.prend_impot_village(ivillage)

        self.retirer_pa(5)

    def morts_villageois(self):
        """
        Méthode qui permet de compter le nombre de perte de villageois d'un noble

        :return: Phrase qui sera affichée dans l'historique
        """

        nb_morts = 0
        for village in self.dico_villages.values() :
                village.vieillsement_population()

        if nb_morts > 0 :
            return f"{nb_morts} roturier(s) sont mort de vieillesse cette année dans les villages de {self.nom}"
        else :
            return f""

    def morts_soldats(self):
        """
        Méthode qui permet de compter le nombre de perte de soldats d'un noble suite à leur vieillisement
        Si le soldat a atteint son espérance de vie, il meurt
        """
        nb_morts = 0
        for soldat in self.liste_soldats :
            soldat.vieillir()
            if soldat.age >= soldat.esperance_vie :
                nb_morts += 1
                self._liste_soldats.remove(soldat)
        if nb_morts > 0 :
            return f"{nb_morts} soldats sont morts de vieillessse dans les rangs de {self.nom}"
        else :
            return f""

    def get_village(self, village_id: int) -> Village | None:
        """
        Cette méthode servira à récupérer le village en fonction de l'id. Si ce n'est pas le village de l'utilisateur alors
        il retourne None
        """
        if village_id in self.dico_villages:
            return self.dico_villages[village_id]

        else:
            return None

    def village_allie(self, village_id: int) -> bool:
        """
        Méthode qui renvoit
          - Vrai si le village passé en paramètre est un village allié (si c'est un village du vassal)
          - Faux si ça ne l'est pas
        """
        return village_id in self.dico_villages.keys()
