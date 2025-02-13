from random import randint


class Personne:
    """
    Une personne est définie par son nom, son age (ici les personnages commencent leur vie à 20 ans), les ressources et l'argent qu'elle possède,
    son espérence de vie (entre 30 et 100 ans), son indice de bonheur (entre 0 et 10, initialisé à 5)
    """

    def __init__(self, pres: int, parg: int, pnom: str = None):
        self._statut = type(self)
        if pnom is not None:
            self._nom = pnom

        self._ressources = pres
        self._argent = parg
        self._age = 20
        self.esperance_vie = randint(30,100)
        self.bonheur = 5

    def __str__(self):
        return self._nom

    @property
    def nom(self):
        return self._nom

    @property
    def age(self):
        return self._age

    @property
    def ressources(self):
        return self._ressources

    def reset_resssources(self):
        self._ressources = 0

    @property
    def argent(self):
        return self._argent

    def reset_argent(self):
        self._argent = 0

    def gestion_ressources(self, value: int) -> bool:
        """
        Permet de gérer l'achat, la vente ou la récolte de ressource d'une Peronne
        """
        self._ressources += value
        # La personne ne peut pas avoir de quantité de ressource negative ou vendre des ressources qu'elle ne possède pas
        if self._ressources < 0 :
            return False
        else :
            return True

    def gestion_argent(self, value: int) -> bool:
        """
       Permet de gérer le gain ou la dépense d'argent d'une Personne
        """
        self._argent += value
        # si la personne dépense plus d'argent qu'elle n'en a,la fonction retourne une erreur
        if self._argent < 0:
            return False
        else:
            return True

    def vieillir(self):
        """
        Méthode qui permet de viellir une personne de 1 an (à chaque tour)
        """
        self._age += 1
