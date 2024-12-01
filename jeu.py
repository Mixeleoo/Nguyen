
from typing import Literal

from Canvas.hud_canvas import HUDCanvas
from Perso.noble import Noble

"""
TOUT TES IMPORT DES DIFFERENTES CLASSES DE PERSO
"""

class Jeu:
    def __init__(self, canvas: HUDCanvas):
        self.canvas = canvas
        """
        TOUTES TES INSTANCIATIONS : LE JOUEUR (Noble), LES BOTS (Noble), ...
        """
        self.joueur = Noble("M.test",0,0)
        pass

    def immigrer(self,  village_id: int, type_v: Literal["paysan", "artisan"], effectif: int):
        """
        Méthode qui va immigrer en fonction de canvas

        :param effectif : nombre de villageois désirés par le joueur
        :param type_v: type de villageois (PS : Literal["paysan", "artisan"] veut dire soit "paysan", soit "artisan" rien d'autre)
        :param village_id : l'id du village dans lequel les futurs villageois habiteront
        """
        self.joueur._dico_villages[village_id].ajouter_villageois(type_v, effectif)


        print("choix nombre :", effectif)
        print("type_villageois :", type_v)
        print("choix village :", village_id)

    def construire_village(self, village_id: int):
        """
        Méthode qui va ajouter un village dans la liste de villages du joueur

        :param village_id : l'id du village (id du carré sur la map que le joueur aura selectionné
        """
        self.joueur.creer_village(village_id)
        print("ID emplacement :",village_id)

    def construire_eglise(self, village_id: int):
        """
        Méthode pour construire une Église dans un village choisit

        :param village_id : id du village dans lequel le joueur veut construir une église
        """
        pass
