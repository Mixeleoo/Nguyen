
from typing import Literal
from dataclasses import dataclass
from random import randint, choice
from math import ceil

from Perso.noble import Noble
from Perso.seigneur import Seigneur
from Perso.vassal import Vassal
from parameter import ACTIONS_NAME_COST, PAYSAN_OR_ARTISAN_TAG, BUILD_CHURCH, BUILD_CITY, TAXES_TAG, \
    WAR_TAG, VASSALIZE_TAG
from Territoire.village import Village

@dataclass
class EventInfo:
    type: Literal["Épidémie", "Incendie", "Pillage", "Famine", "Rien", "Récolte abondante", "Immigration", "Vassalisation"]
    descriptif: tuple[str, ...] = ()  # Le fait qu'il soit en tuple m'aide pour savoir la taille qu'aura la fenêtre des infos.
    noble_vassalise: Noble = None
    village_incendie: Village = None


@dataclass
class ActionBotInfo:
    type: Literal["Immigration", "Soldat", "Eglise", "Village", "Impôt", "Guerre", "Vassalisation", ""]
    descriptif: str
    noble_vassalise: Noble = None
    noble_vaincu: Noble = None


class Jeu:
    def __init__(self):

        self._const_joueurs: list[Vassal | Noble | Seigneur] = []

        # PYREVERSE
        #self._const_joueurs = Vassal()
        #self._const_joueurs = Noble()
        #self._const_joueurs = Seigneur()

        self._joueurs: list[Vassal | Noble | Seigneur] = []

        # PYREVERSE
        #self._liste_terres = Vassal()
        #self._liste_terres = Noble()
        #self._liste_terres = Seigneur()

        self._tour = 1

        """
        Variable qui indique l'indice du joueur en train de jouer,
        est incrémentée lorsque le joueur clique sur "fin de tour" ou quand le bot fini son tour
        """
        self._index_joueur_actuel = 0

    @property
    def tour(self):
        return self._tour

    @property
    def joueur_actuel(self) -> Noble | Seigneur | Vassal:
        return self._joueurs[self._index_joueur_actuel]

    @property
    def nb_joueurs(self) -> int:
        return len([j for j in self._joueurs if isinstance(j, Noble)])

    def get_joueur(self, index: int) -> Noble:
        return self._joueurs[index]

    def get_joueur_index(self, n: Noble | Seigneur) -> int:
        return self._joueurs.index(n)

    def get_const_joueur(self, index: int) -> Vassal:
        return self._const_joueurs[index]

    @property
    def index_joueur_actuel(self):
        return self._index_joueur_actuel

    def village_de(self, village_id: int) -> Vassal:
        """
        Méthode qui permet de savoir à quel joueur appartient le village placé en paramètre
        """
        for joueur in self._const_joueurs :
            if village_id in joueur.dico_villages.keys() :
                return joueur

    def fin_de_tour(self):
        self._index_joueur_actuel = (self._index_joueur_actuel + 1) % len(self._joueurs)

    # Evenements en début de partie
    def evenement(self) -> EventInfo:
        """
        Cette méthode permet de gérer les évenment en début de partie à l'aide d'un système de tirage de dés à 100 faces
        """
        choix_ev = randint(1,100)

        if 1 <= choix_ev <= 5:
            # épidémie : tous les villageois qui ont une espérance de vie inférieure à esp meurent
            esp = randint(50,100)
            nb_morts = 0
            for village in list(self.joueur_actuel.dico_villages.values()) :
                for villageois in village.liste_roturier :
                    if villageois.esperance_vie < esp :
                        nb_morts += 1
                        village.liste_roturier.remove(villageois)

            return EventInfo("Épidémie", (f"Morts : {nb_morts}",))

        elif 6 <= choix_ev <= 10:
            # incendies : un village aléatoire parmi la liste de villages du joueur/bot disparaît
            id_village_supp = choice(list(self.joueur_actuel.dico_villages.keys()))
            village_supp = self.joueur_actuel.dico_villages.pop(id_village_supp)

            return EventInfo("Incendie", (f"Village disparu : {village_supp.nom}",), village_incendie=village_supp)

        elif 11 <= choix_ev <= 20:
            # pillage : l'argent et les ressources d'un village sont volés
            id_village_pie = choice(list(self.joueur_actuel.dico_villages.keys()))
            qt_arg = 0
            qt_res = 0

            for villageois in self.joueur_actuel.dico_villages[id_village_pie].liste_roturier:
                qt_res += villageois.ressources
                qt_arg += villageois.argent


                villageois.reset_resssources()
                villageois.reset_argent()

            return EventInfo(
                "Pillage",
                (f"Village pillé : {self.joueur_actuel.dico_villages[id_village_pie].nom}",
                f"Quantité de ressources volées : {qt_res}",
                f"Quantité d'argent volé : {qt_arg}"))

        elif 21 <= choix_ev <= 40:
            # famine : les ressources des terres sont divisées par 2
            for village in self.joueur_actuel.dico_villages.values():
                village.facteur_recolte = 0.5
            return EventInfo("Famine", ("Les ressources des terres sont divisées par 2",))

        elif 41 <= choix_ev <= 64:
            return EventInfo("Rien")

        elif 65 <= choix_ev <= 84:
            # récolte abondante : ressources des terres doublées
            for village in self.joueur_actuel.dico_villages.values() :
                village.facteur_recolte = 2
                village.recuperation_bonheur()
            return EventInfo("Récolte abondante", ("Les ressources des terres sont doublées",))

        elif 85 <= choix_ev <= 94:
            # immigration : des roturiers augmentent la population d'un village
            id_village_peuple = choice(list(self.joueur_actuel.dico_villages.keys()))
            nb_immigres = randint(1,3)
            type_imigres = choice(["artisan","paysan"])
            self.joueur_actuel.dico_villages[id_village_peuple].ajouter_villageois(type_imigres, nb_immigres)
            return EventInfo("Immigration", (f"Effectif : {nb_immigres}\nType : {type_imigres}",))

        elif 95 <= choix_ev <= 100:
            # vassalisation : un noble se propose comme vassal
            noble = choice([j for j in self._joueurs[1:] if type(j) != Vassal])
            return EventInfo("Vassalisation", (f"Se propose comme vassal : {noble.nom}",), noble_vassalise=noble)

    # Actions
    def creer_noble(self, village_id: int, l_terre: list[Literal["PLAIN", "MOUNTAIN", "LAKE", "FOREST"]], couleur: str = None):
        """
        Méthode qui créera un nouveau noble et lui attribuera l'id de son village

        :param village_id: id du village crée
        :param prenom: prenom du noble
        :param nom_village: nom du village
        :param l_terre: liste des terres du village
        """
        nouveau_noble = Noble(300, 300, index=len(self._joueurs), couleur=couleur)
        nouveau_noble.ajouter_village(village_id, l_terre)
        self._joueurs.append(nouveau_noble)
        self._const_joueurs.append(nouveau_noble)

        return nouveau_noble

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

        nobles_vassalises = [pnoble]

        if not(isinstance(self.joueur_actuel, Seigneur)):
            new_seigneur = Seigneur(self.joueur_actuel.ressources, self.joueur_actuel.argent, self.joueur_actuel.id, pnom=self.joueur_actuel.nom, couleur=self.joueur_actuel.couleur)
            new_seigneur.dico_villages = self.joueur_actuel.dico_villages
            new_seigneur.liste_soldats = self.joueur_actuel.liste_soldats

            index = self.get_joueur_index(self.joueur_actuel)
            self._joueurs[index] = new_seigneur
            self._const_joueurs[index] = new_seigneur

        # Si le noble vassalisé est un Seigneur, le noble qui vassalise gagne ses vassaux
        if isinstance(pnoble, Seigneur):
            self.joueur_actuel.liste_nobles = pnoble.liste_nobles
            nobles_vassalises += pnoble.liste_nobles

        # Transformation du Noble en Vassal
        new_vassal = Vassal(pnoble.ressources, pnoble.argent, pnoble.id, pnom=pnoble.nom, couleur=pnoble.couleur)
        new_vassal.dico_villages = pnoble.dico_villages
        new_vassal.liste_soldats = pnoble.liste_soldats

        index = self.get_joueur_index(pnoble)
        self._joueurs[index] = new_vassal
        self._const_joueurs[index] = new_vassal

        self.joueur_actuel.liste_nobles += [new_vassal]

        return nobles_vassalises

    def guerre(self, pnoble : Noble | Seigneur, cause : Literal["V","G"]):
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
        :param cause : Paramètre qui permet de dire si la guerre est déclanchée suite à une vassalisation(V) ou par choix(G)
        """
        if cause == "G" :
            self.joueur_actuel.retirer_pa(8)
            self.joueur_actuel.gestion_ressources(-100)

        # initialisation des deux armées
        effectif_armee_joueur = self.joueur_actuel.effectif_armee
        effectif_armee_ennemie = pnoble.effectif_armee

        # L'attaquant gagne
        if effectif_armee_joueur > effectif_armee_ennemie or effectif_armee_joueur == effectif_armee_ennemie and randint(0,1) == 1:
            # Conquête des villages du noble vaincu
            self.joueur_actuel._dico_villages = self.joueur_actuel.dico_villages | pnoble.dico_villages
            # conquete des villages des vassaux si le noble vaincu est un seigneur
            if isinstance(pnoble,Seigneur) :
                for noble in pnoble.liste_nobles :
                    self.joueur_actuel._dico_villages = self.joueur_actuel.dico_villages | noble.dico_villages
                    self._joueurs.remove(noble)
            self._joueurs.remove(pnoble)

            # Si le défenseur a une armée, l'attaquant a des pertes.
            if effectif_armee_ennemie:
                perte_soldats = 0.5 * effectif_armee_ennemie  # quantité de soldat en moins dans l'armée total du joueur/bot après la bataille (soldats des vassaux compris)

                self.joueur_actuel.liste_soldats = self.joueur_actuel.liste_soldats[:len(self.joueur_actuel.liste_soldats) - ceil((perte_soldats*len(self.joueur_actuel.liste_soldats))/effectif_armee_joueur)] #supression des soldats perdus
                if isinstance(self.joueur_actuel, Seigneur) :
                    for chevalier in self.joueur_actuel.liste_nobles:
                       chevalier.liste_soldats = chevalier.liste_soldats[:len(chevalier.liste_soldats) - ceil((perte_soldats * len(chevalier.liste_soldats)) / effectif_armee_joueur)]  # supression des soldats perdus

            return True

        # Le défenseur gagne
        else:
            # Conquête des villages du noble vaincu
            pnoble._dico_villages = pnoble.dico_villages | self.joueur_actuel.dico_villages
            # conquete des villages des vassaux si le noble vaincu est un seigneur
            if isinstance(self.joueur_actuel, Seigneur):
                for noble in self.joueur_actuel.liste_nobles:
                    pnoble._dico_villages = pnoble.dico_villages | noble.dico_villages
                    self._joueurs.remove(noble)
            self._joueurs.remove(self.joueur_actuel)

            # Si l'attaquant a une armée, le défenseur a des pertes.
            if effectif_armee_joueur:
                perte_soldats = 0.5 * effectif_armee_joueur  # quantité de soldat en moins dans l'armée total du noble en paramètre après la bataille (soldats des vassaux compris)

                pnoble.liste_soldats = pnoble.liste_soldats[:len(pnoble.liste_soldats) - ceil((perte_soldats * len(pnoble.liste_soldats)) / effectif_armee_ennemie)]  # supression des soldats perdus

                if isinstance(pnoble, Seigneur):
                    for chevalier in pnoble.liste_nobles:
                        chevalier.liste_soldats = chevalier.liste_soldats[:len(chevalier.liste_soldats) - ceil((perte_soldats * len(chevalier.liste_soldats)) / effectif_armee_ennemie)]  # supression des soldats perdus

            return False

    def imposer(self, l_villages: list[int], l_nobles: list[int] = None) -> None:
        if l_nobles is None:
            self.joueur_actuel.imposer(l_villages)

        else:
            l = []
            for noble_i in l_nobles:
                l.append(self.get_const_joueur(noble_i))

            self.joueur_actuel.imposer(l_villages, l)

    def tour_bots(self) -> ActionBotInfo:
        """
        Méthode qui lancera UNE action du noble actuellement en train de jouer.
        S'il fait la guerre contre le joueur (l'utilisateur) et que le joueur perd, plus besoin de finir les tours des nobles.

        :return: un tuple comportant (
            "Titre action effectuée",
            "Message à écrire dans l'historique",
            Noble vassalisé ou Noble déclérant la guerre au joueur sinon None.
        )
        """

        action_liste = [PAYSAN_OR_ARTISAN_TAG, "Soldat", BUILD_CHURCH, BUILD_CITY, TAXES_TAG, WAR_TAG, VASSALIZE_TAG]

        if self.joueur_actuel.pa == 0:
            #self.joueur_actuel.reset_pa()
            self.fin_de_tour()
            return ActionBotInfo("", "")

        else:
            # il faut vérifier que le bot peut bien faire les actions avant de les lancer et donc qu'il a assez de PA
            # Pour ça on peut utiliser le dictionnaire ACTIONS_TAG_COST de parameter.py, et vérifier avec ça et
            # la fameuse boucle qui récupérera un choix au pif le temps que l'action choisie est payable.

            if isinstance(self.joueur_actuel, Vassal):
                action_liste.remove(VASSALIZE_TAG)
                action_liste.remove(WAR_TAG)

            action = choice([a for a in action_liste if self.joueur_actuel.action_possible(ACTIONS_NAME_COST[a])])

            if action == PAYSAN_OR_ARTISAN_TAG:
                # choix aléatoire du type de villageois voulu en fonction du nombre de PA restants au bot
                village = choice(list(self.joueur_actuel.dico_villages.keys()))
                nb_villageois = 0
                if self.joueur_actuel.pa >= 2 :
                    type_villageois: Literal["paysan", "artisan"] = choice(["artisan","paysan"])

                    if type_villageois == "paysan":
                        nb_villageois = randint(1,self.joueur_actuel.pa)
                    elif type_villageois == "artisan":
                        nb_villageois = randint(1,self.joueur_actuel.pa//2)

                    self.joueur_actuel.immigrer(village, type_villageois, nb_villageois)
                    return ActionBotInfo("Immigration", f"{self.joueur_actuel.nom} a accueilli {nb_villageois} nouveau(x) {type_villageois}.")

                elif self.joueur_actuel.pa == 1:
                    self.joueur_actuel.immigrer(village, "paysan", 1)
                    return ActionBotInfo("Immigration", f"{self.joueur_actuel.nom} a accueilli 1 nouveau paysan.")

            elif action == "Soldat":
                #Choix aléatoire du nombre de soldats recrutés en fonction du nombre de PA du bot
                nb_soldats = randint(1, self.joueur_actuel.pa // 2 if self.joueur_actuel.pa // 2 < self.joueur_actuel.argent // 20 else self.joueur_actuel.argent // 20)
                self.joueur_actuel.ajout_soldat(nb_soldats)

                return ActionBotInfo("Soldat", f"{self.joueur_actuel.nom} a recruté {nb_soldats} soldats.")

            elif action == BUILD_CHURCH:
                #Construction d'une église dans un village choisi aléatoirement parmis ceux du bot
                village = choice(list(self.joueur_actuel.dico_villages.keys()))
                self.joueur_actuel.construire_eglise(village)
                return ActionBotInfo("Eglise", f"{self.joueur_actuel.nom} a construit une église.")

            elif action == BUILD_CITY:
                return ActionBotInfo("Village", f"{self.joueur_actuel.nom} a construit un village.")

            elif action == TAXES_TAG:
                #Choix aléatoire du nombre de village et/ou de nobles à imposer + choix aléatoire des quels
                nobles = []
                nb_nobles = 0
                nb_villages = randint(1,len(list(self.joueur_actuel.dico_villages.keys())))
                villages = list(self.joueur_actuel.dico_villages.keys()).copy()

                if isinstance(self.joueur_actuel, Seigneur) :
                    nb_nobles = randint(1, len(self.joueur_actuel.liste_nobles)-1)
                    nobles = self.joueur_actuel.liste_nobles.copy()

                villages_id = []
                nobles_i = []

                for ivillage in range(nb_villages):
                    choix = choice(villages)
                    villages_id += [choix]
                    villages.remove(choix)

                for inoble in range(nb_nobles) :
                    choix_noble = nobles[randint(0,len(nobles)-1)]
                    nobles_i += [choix_noble]
                    nobles.remove(choix_noble)

                self.joueur_actuel.imposer(villages_id, nobles_i)

                return ActionBotInfo("Impôt", f"{self.joueur_actuel.nom} a récupéré l'impôt.")

            elif action == WAR_TAG:
                 noble_choisi = choice(self._joueurs)

                 victoire = self.guerre(noble_choisi,"G")


                 if victoire:
                    noble_vaincu = noble_choisi
                    noble_victorieux = self.joueur_actuel
                 else :
                    noble_vaincu = self.joueur_actuel
                    noble_victorieux = noble_choisi


                 return ActionBotInfo("Guerre",f"{noble_victorieux.nom} a vaincu {noble_vaincu.nom}." , noble_vaincu)

            elif action == VASSALIZE_TAG:

                noble_choisi = choice(self._joueurs)
                while isinstance(noble_choisi, Vassal) :
                    noble_choisi = choice(self._joueurs)

                argent = randint(1,self.joueur_actuel.argent*0.75)
                ressources = randint(1,self.joueur_actuel.ressources * 0.75)

                if self.joueur_actuel.soumettre(noble_choisi, argent, ressources)  :
                    self.vassalisation_confirmee(noble_choisi, argent, ressources)
                    return ActionBotInfo("Vassalisation", f"{noble_choisi.nom} a accepté d'être le vassal de {self.joueur_actuel.nom}.", noble_choisi)

                else :
                    victoire = self.guerre(noble_choisi, "V")

                    if victoire:
                        noble_vaincu = noble_choisi
                        noble_victorieux = self.joueur_actuel
                    else:
                        noble_vaincu = self.joueur_actuel
                        noble_victorieux = noble_choisi

                    return ActionBotInfo("Guerre", f"{noble_choisi.nom} a refusé d'être le vassal de {self.joueur_actuel.nom}.\nUne guerre a éclaté, {noble_victorieux.nom} en ressort victorieux.", noble_vaincu)

    # Fin de tour
    def fin_annee(self) -> list[str]:
        """
        Méthode qui sera appelée en fin de tour

        :return: liste des phrases à afficher dans l'historique pour chaque action de fin de tour
        """
        self._tour += 1
        phrases = []

        for joueur in self._joueurs :
            phrases += [joueur.morts_villageois()]  # vérifier le nombre de roturiers mourrant de vieillesse
            phrases += [joueur.morts_soldats()] # vérifier le nombre de soldats mourrant de vieillesse
            joueur.reset_pa()

        for joueur in self._joueurs :
            for village in joueur.dico_villages.values() :
                village.recuperer_recoltes() # récupération des récoltes en début de tour
                village.appliquer_don() # appliquer le don associée à(aux) église(s) du village
                village.peupler() # des villageois viennet peupler les villages

                for villageois in village.liste_roturier:
                    villageois.commercer() #commerce en cas de surplus de ressource

                village.recuperation_bonheur() # récupération d'un point de bonheur par tous les villageois

            phrases += [joueur.nourrir_soldats()] # vérifier que tous les soldats peuvent être nourris
            phrases += [joueur.nourrir_peuple()]  # vérifier que tous les villageois peuvent être nourris

        return phrases
