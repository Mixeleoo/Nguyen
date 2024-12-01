
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

    def immigrer(self, effectif: int, type_v: Literal["paysan", "artisan"], village_id: int):
        """
        Méthode qui va immigrer en fonction de canvas

        :param effectif : nombre du type de villageois désiré
        :param type_v: type de villageois (PS : Literal["paysan", "artisan"] veut dire soit "paysan", soit "artisan" rien d'autre)
        :param village_id : l'id du village concerné
        """
        print("choix nombre :", effectif)
        print("type_villageois :", type_v)
        print("choix village :", village_id)

    def construire_village(self, village_id: int):
        """
        Méthode qui va ajouter un village au joueur

        :param village_id : l'id du village
        """
        pass

    def construire_eglise(self):
        """
        Méthode pour construire une Église dans un village
        """
        pass
