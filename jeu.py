
from Canvas.hud_canvas import HUDCanvas
"""
TOUT TES IMPORT DES DIFFERENTES CLASSES DE PERSO
"""

class Jeu:
    def __init__(self):
        """
        TOUTES TES INSTANCIATIONS : LE JOUEUR (Seigneur), LES BOTS (Seigneur), ...
        """
        pass

    def immigrer(self, canvas: HUDCanvas):
        """
        Ta méthode qui va immigrer en fonction de canvas
        Les méthodes qui t'intéressent :
        canvas.hud_paysan_or_artisan.last_choice_made
        canvas.hud_choose_village.last_choice_made
        Si tu as besoin de savoir comment sont organisées les données dans ces attribus ctrl + clic gauche dessus PyCharm t'amènera
        vers le commentaire qui la décrit.
        """
        print(canvas.hud_paysan_or_artisan.last_choice_made)
        print(canvas.hud_choose_village.last_choice_made)
