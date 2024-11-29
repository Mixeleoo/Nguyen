from Perso.ecclesiastique import Ecceclesiastique

class Eglise :
    """
    Une eglise est composée d'un prêtre qui lui est associé
    """
    def __init__(self, ppretre : Ecceclesiastique, pnom : str):
        self._pretre = ppretre
        self._nom = pnom