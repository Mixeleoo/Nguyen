from random import choice

from Perso.ecclesiastique import Ecceclesiastique
from Perso.paysan import Paysan
from Perso.roturier import Roturier
from Territoire.eglise import Eglise
from parameter import nom_aleatoire_pretres, nom_aleatoire_eglise

from typing import Literal

class Village :
    """
    Un village est représenté par son id (qui servira pour l'associer à son emplacement sur la map)
    par sa population de roturiers (une liste de roturiers) et des églises qui la composent (liste d'églises)
    """
    def __init__(self, pid : int, nom : str) :
        self._nom = nom
        self._identifiant = pid

        # Les roturiers que possède le noble
        self._liste_roturier : list[Roturier] = [Roturier() for _ in range(5)] + [Paysan() for _ in range(5)]

        # Liste des églises dans le village
        self._liste_eglises : list[Eglise] = []

    @property
    def nom(self):
        return self._nom

    @property
    def id(self):
        return self._identifiant

    @property
    def liste_roturier(self):
        return self._liste_roturier

    @property
    def population(self):
        return len(self._liste_roturier)

    @property
    def ressources(self):
        res = 0
        for r in self._liste_roturier:
            res += r.ressources

        return res

    @property
    def bonheur_general(self):
        """
        Retourne la moyenne du bonheur dans le village
        """
        bonheur = 0
        effectif = 0
        for villageois in self.liste_roturier:
            bonheur += villageois.bonheur
            effectif += 1
        return round(bonheur / effectif, 2)

    def ajouter_villageois(self, type_v: Literal["paysan", "artisan", "soldat"], effectif : int) :
        """
        Cette fonction prend en paramètre le type de villageois qui sera ajouté et leur nombre.
        Elle servira lorsque le joueur choisira l'action 'Immigration'
        """
        # Réduire la taille maximale à 80 habitants.
        effectif = 80 - self.population if 80 - self.population < effectif else effectif

        for v in range(effectif):
            if type_v == "artisan":
                self._liste_roturier += [Roturier()]
            elif type_v == "paysan":
                self._liste_roturier += [Paysan()]

        print(f"Roturiers du village : {self._nom} | {self._identifiant} : \n{self._liste_roturier}")

    def creer_eglise(self):
        """
        ajoute à la liste d'églises du village une nouvelle église
        """
        pretre = Ecceclesiastique(nom_aleatoire_pretres())
        self._liste_eglises += [Eglise(pretre, nom_aleatoire_eglise())]

    def appliquer_don(self):
        """
        Methode qui permet de faire profiter un villageois au hasard du don dont le prêtre de l'eglise du village est doté
        S'il y a plusieurs églises dans le village alors autant de villageois seront tirés au hasard pour profiter chacun
        d'un don (on prendra soin de ne pas tirer plusieurs fois le même villageois)
        """

        nb_eglises = len(self._liste_eglises)
        nb_villageois = len(self._liste_roturier)
        new_liste_eglise = self._liste_eglises.copy()
        new_liste_roturier = self._liste_roturier.copy()

        if nb_eglises > nb_villageois :
            for villageois in new_liste_roturier :
                eglise = choice(new_liste_eglise)
                new_liste_eglise.remove(eglise)
                don = eglise.pretre.don
                if don == 1 :
                    villageois.bonheur += 1  # valeur à determiner
                elif don == 2 :
                    villageois.esperance_vie += 1  # valeur à determiner
                elif don == 3 :
                    villageois.cdp += 1  # valeur à determiner

        else :
            for eglise in new_liste_eglise :
                villageois = choice(new_liste_roturier)
                new_liste_roturier.remove(villageois)
                don = eglise.pretre.don
                if don == 1 :
                    villageois.bonheur += 1  # valeur à determiner
                elif don == 2 :
                    villageois.esperance_vie += 1  # valeur à determiner
                elif don == 3 :
                    villageois.cdp += 1  # valeur à determiner