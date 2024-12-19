
from Perso.roturier import Roturier
from Territoire.village import Terre

class Paysan(Roturier):

    """
    Un paysan est un roturier qui débute sans argent et qui est soumit à un impôt plus élévé qu'un simple roturier (50%)
    """
    def __init__(self, terre : Terre, pnom: str = None, cdp: int = None):
        Roturier.__init__(self,terre, pnom, 0, cdp)
        self._taux_impot = 0.50
