
from typing import Literal

from Perso.noble import Noble
from Perso.seigneur import Seigneur
from parameter import *


class Jeu:
    def __init__(self):
        self._joueurs: list[Noble] = []

        """
        Variable qui indique l'indice du joueur en train de jouer,
        est incrémentée lorsque le joueur clique sur "fin de tour" ou quand le bot fini son tour
        """
        self._id_joueur_actuel = 0

    @property
    def joueur_actuel(self) -> Noble | Seigneur:
        return self._joueurs[self._id_joueur_actuel]

    def get_joueur(self, index: int) -> Noble:
        return self._joueurs[index]

    # Evenements en début de partie

    def evenement(self):
        """
        Cette méthode permet de gérer les évenment en début de partie à l'aide d'un système de tirage de dés à 100 faces
        """
        choix_ev = randint(1,100)

        if 1 <= choix_ev <= 5 :
            # épidémie : tous les villageois qui ont un espérance de vie inférieure à esp meurent
            esp = randint(50,100)
            nb_morts = 0
            for village in list(self.joueur_actuel.dico_villages.values()) :
                for villageois in village.liste_roturier :
                    if villageois.esperance_vie < esp :
                        nb_morts += 1
                        village.liste_roturier.remove(villageois)
            return "épidémie", nb_morts

        elif 6 <= choix_ev <= 10 :
            # incendies : un village aléatoire parmis la liste de villages du joueur/bot disparaît
            if len(self.joueur_actuel.dico_villages.values()) > 1 :
                id_village_supp = choice(self.joueur_actuel.dico_villages.keys())
                return "incendie", id_village_supp

        elif 11 <= choix_ev <= 20 :
            # pillage : l'argent et les ressources d'un village son volés
            id_village_pie = choice(list(self.joueur_actuel.dico_villages.keys()))
            for villageois in self.joueur_actuel.dico_villages[id_village_pie].liste_roturier :
                villageois._ressources = 0
                villageois._argent = 0
            return "pillage", self.joueur_actuel.dico_villages[id_village_pie].nom

        elif 21 <= choix_ev <= 40 :
            # famine : les ressources des plaines sont divisées par 2
            pass





    # Actions

    def creer_noble(self, village_id: int, prenom: str, nom_village: str):
        """
        Méthode qui créera un nouveau noble et lui attribuera l'id de son village

        :param village_id: id du village crée
        :param prenom: prenom du noble
        :param nom_village: nom du village
        """
        nouveau_noble = Noble(prenom, 10, 10)
        nouveau_noble.ajouter_village(village_id, nom_village)
        self._joueurs.append(nouveau_noble)

    def immigrer(self, village_id: int, type_v: Literal["paysan", "artisan", "soldat"], effectif: int):
        """
        Méthode qui va ajouter au village (village_id) le nombre (effectif) de villageois (type_v)

        :param effectif : nombre de villageois désirés par le joueur
        :param type_v: type de villageois (PS : Literal["paysan", "artisan"] veut dire soit "paysan", soit "artisan" rien d'autre)
        :param village_id : l'id du village dans lequel les futurs villageois habiteront
        """

        print("choix nombre :", effectif)
        print("type_villageois :", type_v)
        print("choix village :", village_id)

        self.joueur_actuel.dico_villages[village_id].ajouter_villageois(type_v, effectif)

    def construire_village(self, village_id: int, nom: str):
        """
        Méthode qui va ajouter un village dans la liste de villages du joueur

        :param village_id : l'id du village (id du carré sur la map que le joueur aura selectionné
        """
        self.joueur_actuel.ajouter_village(village_id, nom)
        print("ID emplacement :",village_id)

    def construire_eglise(self, village_id: int):
        """
        Méthode pour construire une Église dans un village choisi

        :param village_id : id du village dans lequel le joueur veut construir une église
        """
        self.joueur_actuel.dico_villages[village_id].creer_eglise()

    def recruter_soldat(self, effectif: int):
        """
        Méthode qui ajoute à la liste de soldats du joueur/bot le nombre de soldats désiré

        :param effectif: NOMBRE DE SOLDATS DESIRE
        """
        self.joueur_actuel.ajout_soldat(effectif)

    def vassalisation_confirmee(self, pnoble : Noble | Seigneur, parg : int, pres : int):
        """
        Méthode qui permet de vassaliser le noble/seigneur mis en paramètre s'il a accepté de se soumettre
        Si le joueur/bot n'est pas encore un Seigneur( n'a encore vassalisé aucun noble), alors il en devient un
        Puis dans sa liste de noble est ajouté le nouveau vassal

        :param pnoble: Noble que le joueur/bot souhaite vassaliser
        :param parg: Quantité d'argent que le joueur/bot souhaite offrir à son futur vassal qui lui sont donc retiré
        :param pres: Quantité de ressources que le joueur/bot souhaite offir à son futur vassal qui lui sont donc retiré
        """

        self.joueur_actuel.gestion_ressources(-pres)
        self.joueur_actuel.gestion_argent(-parg)

        if not(isinstance(self.joueur_actuel, Seigneur)) :
            new_seigneur = Seigneur(self.joueur_actuel.nom,self.joueur_actuel.ressources,self.joueur_actuel.argent)
            new_seigneur._dico_villages = self.joueur_actuel.dico_villages
            new_seigneur._liste_soldats = self.joueur_actuel.liste_soldats
            self._joueurs[self._id_joueur_actuel] = new_seigneur

        self.joueur_actuel.liste_nobles += [pnoble]

    def imposer(self, l_villages : list[int], l_noble : list[int]):
        """
        Methode qui permet d'imposer un village et/ou un noble suivant les choix qu'aura fait le joueur/bot

        :param l_villages : liste d'id des villages choisis
        :param l_noble : liste d'id des nobles choisis
        """
        for inoble in l_noble :
            self.joueur_actuel.prend_impot_noble(inoble)
        for ivillage in l_villages :
            self.joueur_actuel.prend_impot_village(ivillage)

    def guerre(self, pnoble : Noble | Seigneur):
        """
        Méthode qui permettra de gérer la guerre si le joueur/bot la déclare OU si un noble refuse de se soumettre
        On remplira la liste des membre de l'armée du joueur/bot et celle du noble/seigneur auquel il déclare la guerre
        en ajoutant respectivement leurs soldats, leur vassaux s'ils en ont et les soldats de leur vassaux

        On décidera du vainqueur en fonction de la taille de son armée : retourne True si l'armée du joueur/bot est plus grande et False sinon
        Si leurs armées sont de même taille, le vainqueur sera choisi au pile ou face :
        Si c'est 1, le joueur/bot a gagné
        Si c'est 0, il a perdu

        En cas de victoire du joueur/bot, on ajoute les villages du noble vaincu au dico de village du joueur/bot
        et le noble vaincu est suprimé de la liste des joueurs

        :param pnoble : Noble auquel la guerre est déclarée
        """
        # initialisation des deux armées
        armee_joueur = self.joueur_actuel.liste_soldats + [self._id_joueur_actuel]
        armee_ennemie = pnoble.liste_soldats + [pnoble]

        # points_joueur = 0
        # points_ennemie = 0

        # remplissage de l'armée du joueur/bot
        if isinstance(self.joueur_actuel, Seigneur):
            armee_joueur += self.joueur_actuel.liste_nobles
            for noble in self.joueur_actuel.liste_nobles :
                armee_joueur += noble.liste_soldats

        # remplissage de l'armée ennemie
        if isinstance(pnoble,Seigneur) :
            armee_ennemie += pnoble.liste_nobles
            for noble in pnoble.liste_nobles :
                armee_ennemie += noble.liste_soldats

        # choix vainqueur

        victoire = len(armee_joueur) > len(armee_ennemie) or (len(armee_ennemie) == len(armee_joueur) and randint(0,1) == 1)

        # Conquête des villages du noble vaincu
        if victoire :
            self.joueur_actuel._dico_villages = self.joueur_actuel.dico_villages | pnoble.dico_villages
            self._joueurs.remove(pnoble)

        return victoire

