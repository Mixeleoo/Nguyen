from Perso.personne import Personne

class Soldat(Personne) :

    def __init__(self, pnom : str):
        Personne.__init__(self,pnom,0,0)