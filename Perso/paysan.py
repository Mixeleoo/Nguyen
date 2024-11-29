from roturier import Roturier


class Paysan(Roturier):

    """
    Un paysan est un roturier qui débute sans argent et qui est soumit à un impôt plus élévé qu'un simple roturier (50%)
    """
    def __init__(self, pnom: str, cdp: int):
        Roturier.__init__(self, pnom, 0, cdp)
        self._taux_impot = 0.50
