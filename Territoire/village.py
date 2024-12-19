
from random import choice
from typing import Literal
from dataclasses import dataclass


from Perso.ecclesiastique import Ecceclesiastique
from Perso.paysan import Paysan
from Perso.roturier import Roturier
from Territoire.eglise import Eglise
from Perso.soldat import Soldat
from parameter import *


# TODO Éloïse: Établir une quantité de ressources récoltées pour chaque type de terre autour du village. 10 Roturiers max par terre.



class Village :
    """
    Un village est représenté par son id (qui servira pour l'associer à son emplacement sur la map), par une liste des terres qui l'entourent
    par sa population de roturiers (une liste de roturiers) et des églises qui la composent (liste d'églises)
    """
    def __init__(self, pid : int, nom : str, l_terres : list[Terre]) :
        self._nom = nom
        self._identifiant = pid

        # Les roturiers que possède le noble
        self._liste_roturier : list[Roturier] = [Roturier() for _ in range(5)] + [Paysan() for _ in range(5)]

        # Liste des églises dans le village
        self._liste_eglises : list[Eglise] = []

        # Liste du type des 8 terres entourant le village
        self._liste_terres : list[Terre] = l_terres

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

    def recuperer_recoltes(self):
        """
        Méthode qui permet de gérer la récupération des ressources sur les terres autour du village par chacun des villageois
        En fonction de la capcacité de la terre sur laquelle il travail + sa capactité de production
        """
        for villageois in self.liste_roturier :
            villageois.gestion_ressources(capacite_prod_terre[villageois.terre.type] + villageois.produit())

    def ajouter_villageois(self, type_v: Literal["paysan", "artisan"], effectif : int) -> int :
        """
        Cette fonction prend en paramètre le type de villageois qui sera ajouté et leur nombre.
        Elle servira lorsque le joueur choisira l'action 'Immigration'

        :param type_v : type de villageois souhaité
        :param effectif : nombre de villageaois souhaité

        :return: nombre de place disponible dans le village si effectif souhaité trop grand
        """
        # Limite la taille maximale à 80 habitants.
        if self.population + effectif > 80  :
            return 80 - self.population

        for v in range(effectif):
            terre = choice(self._liste_terres)
            while terre.nb_roturiers >= 10:
                terre = choice(self._liste_terres)

            if type_v == "artisan":
                self._liste_roturier += [Roturier(terre)]

            elif type_v == "paysan":
                self._liste_roturier += [Paysan(terre)]

            terre.nb_roturiers += 1



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

    def revolte(self, l_soldat : list[Soldat]) :
        """
        Méthode qui gère un cas de révolte dans une village
        Si une révolte se produit.
        Le joueur/bot gagne s'il a plus de la moitié de ses effectifs de roturiers comme effectif de soldats
            Si le joueur gagne, renvoyer "V" puis le nombre de roturiers perdus (25% de ses roturiers) sous forme de chaîne de caractère.
            Sinon renvoyer "D".
        Sinon renvoyer un tuple vide.
        """

        if self.bonheur_general > 1 :
            return ()

        if len(l_soldat) > len(self.liste_roturier)//2 :
            perte_revolutionnaires = int(len(self.liste_roturier) * 0.25)
            self.liste_roturier = self.liste_roturier[:len(self.liste_roturier)-perte_revolutionnaires]
            return "V", str(perte_revolutionnaires)

        elif len(l_soldat) <= len(self.liste_roturier)//2 :
            return ("D",)