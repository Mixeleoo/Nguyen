from Perso.personne import Personne

class Soldat(Personne) :

    def __init__(self, pnom : str = None):
        Personne.__init__(self,0 , 0, pnom)