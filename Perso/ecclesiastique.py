from Perso.personne import Personne


class Ecceclesiastique(Personne):
    def __init__(self, pnom: str, pres: int, parg: int):
        Personne.__init__(self, pnom, pres, parg)
