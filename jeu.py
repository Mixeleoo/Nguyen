
from typing import Literal

from Canvas.hud_canvas import HUDCanvas
from Perso.noble import Noble
from parameter import prenoms_perso, prenom_aleatoire

"""
TOUT TES IMPORT DES DIFFERENTES CLASSES DE PERSO
"""

class Jeu:
    def __init__(self, canvas: HUDCanvas):
        self.canvas = canvas
        """
        TOUTES TES INSTANCIATIONS : LE JOUEUR (Noble), LES BOTS (Noble), ...
        """
        self._joueurs: list[Noble] = []

        """
        Variable qui indique l'indice du joueur en train de jouer,
        est incrémentée lorsque le joueur clique sur "fin de tour" ou quand le bot fini son tour
        """
        self._id_joueur_actuel = 0

    @property
    def joueur_actuel(self) -> Noble:
        return self._joueurs[self._id_joueur_actuel]

    def creer_noble(self, village_id: int):
        """
        Méthode qui créera un nouveau noble et lui attribuera l'id de son village

        :param village_id: id du village crée
        """
        nouveau_noble = Noble(prenom_aleatoire(), 0, 0)
        nouveau_noble.ajouter_village(village_id)
        self._joueurs.append(nouveau_noble)

    def immigrer(self,  village_id: int, type_v: Literal["paysan", "artisan", "soldat"], effectif: int):
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
