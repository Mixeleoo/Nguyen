
from typing import Literal, Any

from Perso.noble import Noble
from Perso.seigneur import Seigneur
from Perso.vassal import Vassal
from Territoire.village import Village
from parameter import *

# TODO Léo: Établir une quantité de ressources récoltées pour chaque type de terre autour du village. 10 Roturiers max par terre.
# TODO Léo: Les Nobles étant dans notre liste peuvent aussi jouer avec moins d'actions.
# TODO Léo: Si les nobles se vassalisent entre eux, ils sont à supprimer des nobles à vaincre.
# TODO Léo: Dans la fenêtre plus d'info, permettre d'afficher tous les villageois sous forme de scrollbar (automatiser la scrollbar du coup flemme de la refaire), et si on clique sur un villageois afficher ses détails dans la même fenêtre + un bouton pour revenir en arrière.

class Jeu:
    def __init__(self):

        self._const_joueurs: list[Vassal | Noble | Seigneur] = []
        self._joueurs: list[Vassal | Noble | Seigneur] = []

        """
        Variable qui indique l'indice du joueur en train de jouer,
        est incrémentée lorsque le joueur clique sur "fin de tour" ou quand le bot fini son tour
        """
        self._index_joueur_actuel = 0

    @property
    def joueur_actuel(self) -> Noble | Seigneur | Vassal:
        return self._joueurs[self._index_joueur_actuel]

    def fin_de_tour(self):
        self._index_joueur_actuel = (self._index_joueur_actuel + 1) % (NB_NOBLE_AU_DEPART + 1)

    @property
    def nb_joueurs(self) -> int:
        return len([j for j in self._joueurs if isinstance(j, Noble)])

    def get_joueur(self, index: int) -> Noble:
        return self._joueurs[index]

    def get_joueur_index(self, n: Noble | Seigneur) -> int:
        return self._joueurs.index(n)

    def get_const_joueur(self, index: int) -> Noble:
        return self._const_joueurs[index]

    @property
    def index_joueur_actuel(self):
        return self._index_joueur_actuel

    def get_village(self, village_id: int) -> Village | None:
        """
        Cette méthode servira à récupérer le village en fonction de l'id. Si ce n'est pas le village de l'utilisateur alors
        il retourne None
        """
        if village_id in self.joueur_actuel.dico_villages:
            return self.joueur_actuel.dico_villages[village_id]

        else:
            return None

    # Evenements en début de partie
    def evenement(self) -> tuple[str, tuple[str, ...], Any]:
        """
        Cette méthode permet de gérer les évenment en début de partie à l'aide d'un système de tirage de dés à 100 faces
        """
        choix_ev = 100 #randint(1,100)

        if 1 <= choix_ev <= 5:
            # épidémie : tous les villageois qui ont une espérance de vie inférieure à esp meurent
            esp = randint(50,100)
            nb_morts = 0
            for village in list(self.joueur_actuel.dico_villages.values()) :
                for villageois in village.liste_roturier :
                    if villageois.esperance_vie < esp :
                        nb_morts += 1
                        village.liste_roturier.remove(villageois)

            return "Épidémie", (f"Morts : {nb_morts}",), None

        elif 6 <= choix_ev <= 10:
            # incendies : un village aléatoire parmi la liste de villages du joueur/bot disparaît
            id_village_supp = choice(list(self.joueur_actuel.dico_villages.keys()))
            village_supp = self.joueur_actuel.dico_villages.pop(id_village_supp)
            return "Incendie", (f"Village disparu : {village_supp.nom}",), village_supp

        elif 11 <= choix_ev <= 20:
            # pillage : l'argent et les ressources d'un village son volés
            id_village_pie = choice(list(self.joueur_actuel.dico_villages.keys()))
            qt_arg = 0
            qt_res = 0

            for villageois in self.joueur_actuel.dico_villages[id_village_pie].liste_roturier:
                qt_arg += villageois.argent
                qt_res += villageois.ressources

                villageois.reset_resssources()
                villageois.reset_argent()

            return "Pillage", (
                f"Village pillé : {self.joueur_actuel.dico_villages[id_village_pie].nom}",
                f"Quantité de ressources volées : {qt_res}",
                f"Quantité d'argent volé : {qt_arg}"
            ), self.joueur_actuel.dico_villages[id_village_pie]


        elif 21 <= choix_ev <= 40:
            # famine : les ressources des terres sont divisées par 2
            return "Famine", ("Les ressources des terres sont divisées par 2",), None

        elif 41 <= choix_ev <= 64:
            return "Rien", (), None

        elif 65 <= choix_ev <= 84:
            # récolte abondante : ressources des terres doublées
            return "Récolte abondante", ("Les ressources des terres sont doublées",), None

        elif 85 <= choix_ev <= 94:
            # immigration : des roturiers augmentent la population d'un village
            id_village_peuple = choice(list(self.joueur_actuel.dico_villages.keys()))
            nb_immigres = randint(1,3)
            type_imigres = choice(["artisan","paysan"])
            self.joueur_actuel.dico_villages[id_village_peuple].ajouter_villageois(type_imigres, nb_immigres)
            return "Immigration", (f"Effectif : {nb_immigres}", f"Type : {type_imigres}"), None

        elif 95 <= choix_ev <= 100:
            # vassalisation : un noble se propose comme vassal
            noble = choice(self._joueurs)
            return "Vassalisation", (f"Se propose comme vassal : {noble.nom}",), noble

    # Actions

    def creer_noble(self, village_id: int, prenom: str, nom_village: str):
        """
        Méthode qui créera un nouveau noble et lui attribuera l'id de son village

        :param village_id: id du village crée
        :param prenom: prenom du noble
        :param nom_village: nom du village
        """
        nouveau_noble = Noble(prenom, 100, 10)
        v = nouveau_noble.ajouter_village(village_id, nom_village)
        self._joueurs.append(nouveau_noble)
        self._const_joueurs.append(nouveau_noble)

        return v

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

        self.joueur_actuel.dico_villages[village_id].ajouter_villageois(type_v, effectif)

        if type_v == "paysan":
            self.joueur_actuel.retirer_pa(effectif)

        elif type_v == "artisan":
            self.joueur_actuel.retirer_pa(effectif*2)

    def construire_village(self, village_id: int, nom: str):
        """
        Méthode qui va ajouter un village dans la liste de villages du joueur

        :param village_id : l'id du village (id du carré sur la map que le joueur aura selectionné
        """
        self.joueur_actuel.ajouter_village(village_id, nom)
        print("ID emplacement :",village_id)

        self.joueur_actuel.retirer_pa(8)
        self.joueur_actuel.gestion_argent(-300)
        self.joueur_actuel.gestion_ressources(-150)

    def construire_eglise(self, village_id: int):
        """
        Méthode pour construire une Église dans un village choisi

        :param village_id : id du village dans lequel le joueur veut construir une église
        """
        self.joueur_actuel.dico_villages[village_id].creer_eglise()

        self.joueur_actuel.retirer_pa(6)
        self.joueur_actuel.gestion_argent(-100)
        self.joueur_actuel.gestion_ressources(-50)

    def recruter_soldat(self, effectif: int):
        """
        Méthode qui ajoute à la liste de soldats du joueur/bot le nombre de soldats désiré

        :param effectif: NOMBRE DE SOLDATS DESIRE
        """
        self.joueur_actuel.ajout_soldat(effectif)

        self.joueur_actuel.retirer_pa(effectif * 2)

    def vassalisation_confirmee(self, pnoble : Noble | Seigneur, parg : int, pres : int) -> list[Noble]:
        """
        Méthode qui permet de vassaliser le noble/seigneur mis en paramètre s'il a accepté de se soumettre
        Si le joueur/bot n'est pas encore un Seigneur( n'a encore vassalisé aucun noble), alors il en devient un
        Puis dans sa liste de noble est ajouté le nouveau vassal

        :param pnoble: Joueur vassalisé.
        :param parg: Quantité d'argent que le joueur/bot souhaite offrir à son futur vassal qui lui sont donc retiré
        :param pres: Quantité de ressources que le joueur/bot souhaite offir à son futur vassal qui lui sont donc retiré
        """

        self.joueur_actuel.gestion_ressources(-pres)
        self.joueur_actuel.gestion_argent(-parg)
        self.joueur_actuel.retirer_pa(4)

        nobles_vassalises = [pnoble]

        if not(isinstance(self.joueur_actuel, Seigneur)):
            new_seigneur = Seigneur(self.joueur_actuel.nom, self.joueur_actuel.ressources, self.joueur_actuel.argent)
            new_seigneur.dico_villages = self.joueur_actuel.dico_villages
            new_seigneur.liste_soldats = self.joueur_actuel.liste_soldats

            index = self.get_joueur_index(self.joueur_actuel)
            self._joueurs[index] = new_seigneur
            self._const_joueurs[index] = new_seigneur

        # Si le noble vassalisé est un seigneur, le noble vassaliseur gagne ses vassaux.
        if isinstance(pnoble, Seigneur):
            self.joueur_actuel.liste_nobles = pnoble.liste_nobles
            nobles_vassalises += pnoble.liste_nobles

        # Transformation du Noble en vassal
        new_vassal = Vassal(pnoble.nom, pnoble.ressources, pnoble.argent)
        new_vassal.dico_villages = pnoble.dico_villages
        new_vassal.liste_soldats = pnoble.liste_soldats

        index = self.get_joueur_index(pnoble)
        self._joueurs[index] = new_vassal
        self._const_joueurs[index] = new_vassal

        self.joueur_actuel.liste_nobles += [new_vassal]

        return nobles_vassalises

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

        self.joueur_actuel.retirer_pa(5)

    def guerre(self, pnoble : Noble | Seigneur):
        """
        Méthode qui permettra de gérer la guerre si le joueur/bot la déclare OU si un noble refuse de se soumettre
        On remplira la liste des membre de l'armée du joueur/bot et celle du noble/seigneur auquel il déclare la guerre
        en ajoutant respectivement leurs soldats, leur vassaux s'ils en ont et les soldats de leur vassaux

        On décidera du vainqueur en fonction de la taille de son armée : retourne True si l'armée du joueur/bot est plus grande et False sinon
        Si leurs armées sont de même taille, le vainqueur sera choisi au pile ou face :
        Si c'est 1, le joueur/bot a gagné
        Si c'est 0, il a perdu

        En cas de victoire du joueur/bot, on ajoute les villages du noble vaincu au dico de village du joueur/bot et perd 50% de l'effectif
        de l'armée ennemie parmis ses soldat et le noble vaincu est suprimé de la liste des joueurs

        :param pnoble : Noble auquel la guerre est déclarée
        """
        self.joueur_actuel.retirer_pa(8)
        self.joueur_actuel.gestion_ressources(-100)

        # initialisation des deux armées
        effectif_armee_joueur = self.joueur_actuel.effectif_armee
        effectif_armee_ennemie = pnoble.effectif_armee

        # choix vainqueur
        if effectif_armee_joueur > effectif_armee_ennemie or effectif_armee_joueur == effectif_armee_ennemie and randint(0,1) == 1:
            # Conquête des villages du noble vaincu
            self.joueur_actuel._dico_villages = self.joueur_actuel.dico_villages | pnoble.dico_villages
            self._joueurs.remove(pnoble)

            pertes_soldats = len(self.joueur_actuel.liste_soldats) - (0.5 * effectif_armee_ennemie) #quantité de soldat restant au joueur après la bataille
            self.joueur_actuel.liste_soldats = self.joueur_actuel.liste_soldats[:pertes_soldats] #supression des soldats perdus
            return True

        else:
            return False

    def tour_noble(self) -> tuple[str, ...]:
        """
        Méthode qui lancera UNE action du noble actuellement en train de jouer.
        S'il fait la guerre contre le joueur (l'utilisateur) et que le joueur perd, plus besoin de finir les tours des nobles.

        :return: un tuple comportant (
            "Titre action effectuée",
            "Message à écrire dans l'historique",
            Noble vassalisé ou Noble déclérant la guerre au joueur sinon None.
        )
        """

        action_liste = ["Immigration","Soldat","Eglise","Village","Impôt","Guerre","Vassalisation"]

        if self.joueur_actuel.pa == 0:
            self.fin_de_tour()

        else:
            # TODO Éloïse.

            if isinstance(self.joueur_actuel,Vassal) :
                action_liste.remove("Vassalisation")
                action_liste.remove("Guerre")

            action = choice(action_liste)

            if action == "Immigration":
                if self.joueur_actuel.pa >= 10 :
                    type_villageois = choice(["artisan","paysan"])
                pass


            elif action == "Soldat" and self.joueur_actuel.pa >= 2:
                #Choix aléatoire du nombre de soldats recrutés en fonction du nombre de PA du bot
                nb_soldats = randint(1,self.joueur_actuel.pa//2)
                self.recruter_soldat(nb_soldats)

                return "Soldat", f"{self.joueur_actuel.nom} a recruté {nb_soldats} soldats"

            elif action == "Eglise" and self.joueur_actuel.pa >= 6 and self.joueur_actuel.ressources >= 50 and self.joueur_actuel.argent >= 100:
                #Construction d'une église dans un village choisi aléatoirement parmis ceux du bot
                village = choice(list(self.joueur_actuel.dico_villages.keys()))
                self.construire_eglise(village)


                return "Eglise", f"{self.joueur_actuel.nom} a construit une église"

            elif action == "Village":
                # TODO : gérer choix emplacement village
                pass
            elif action == "Impôt":
                pass
            elif action == "Guerre":
                pass
            elif action == "Vassalisation":
                pass




            self.joueur_actuel.retirer_pa(1)
            pass
