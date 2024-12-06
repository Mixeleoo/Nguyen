
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
    def joueur_actuel(self) -> Noble|Seigneur:
        return self._joueurs[self._id_joueur_actuel]

    def get_joueur(self, index: int) -> Noble:
        return self._joueurs[index]

    def creer_noble(self, village_id: int, prenom: str):
        """
        Méthode qui créera un nouveau noble et lui attribuera l'id de son village

        :param village_id: id du village crée
        :param prenom: prenom du noble
        """
        nouveau_noble = Noble(prenom, 0, 0)
        nouveau_noble.ajouter_village(village_id)
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

    def construire_village(self, village_id: int):
        """
        Méthode qui va ajouter un village dans la liste de villages du joueur

        :param village_id : l'id du village (id du carré sur la map que le joueur aura selectionné
        """
        self.joueur_actuel.ajouter_village(village_id)
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

    def vassalisation_confirmee(self, pnoble : Noble, parg : int, pres : int):
        """
        Méthode qui permet de vassaliser le noble mis en paramètre s'il a accepté de se soumettre
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
