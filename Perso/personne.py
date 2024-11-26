from random import randint


class Personne:
    """
    Une personne est définie par son nom, son age (ici les personnages commencent leur vie à 20 ans), les ressources et l'argent qu'elle possède,
    son espérence de vie (entre 30 et 100 ans) et son indice de bonheur (entre 0 et 10, initialisé à 5)
    """

    def __init__(self, pnom: str, pres: int, parg: int):
        self._statut = type(self)
        self._nom = pnom
        self._ressources = pres
        self._argent = parg
        self._age = 20
        self._esperance_vie = randint(30,100)
        self._bonheur = 5
        self._pourcentage_impot = 0

    def __str__(self):
        return self._nom

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

    def payer_impot(self) -> int:
        """
        payer_impot retire un pourcentage des ressources et les renvoie
        """
        impot = int(self._ressources * (self._pourcentage_impot / 100))
        self._ressources -= impot
        return impot
