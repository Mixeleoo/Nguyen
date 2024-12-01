from Perso.personne import Personne
from Perso.soldat import Soldat
from Territoire.village import Village
from parameter import nom_aleatoire_village


class Noble(Personne):

    """
    Un noble est une personne qui contôle des roturiers (sous forme d'une liste de roturiers)
    il est également soumis à un impôt s'il est vassal d'un seigneur (10%)
    """
    def __init__(self, pnom: str, pres: int, parg: int):
        Personne.__init__(self, pnom, pres, parg)
        self._taux_impot = 0.10

        # Dictionnaire des villages que le noble dirige avec la structure suivante : identifiant_village : int -> Village
        # Servira a accéder à la liste de Roturiers que le noble possède
        self._dico_villages: dict[int, Village] = {}

        # Liste des soldats sous les ordres du noble
        self._liste_soldats: list[Soldat] = []


    def prend_impot_village(self,pid_village : int):
        """
        Ajoute aux ressources du noble les impot perçu pour chaque roturiers sous ses ordres dans le village mis en paramètre
        """
        for roturier in self._dico_villages[pid_village]._liste_roturier :
            impot_percu = roturier.payer_impot() # recupération du tuple (roturier.argent, roturier.ressources)
            self._argent += impot_percu[0]
            self._ressources += impot_percu[1]

    def creer_village(self, pid: int):
        """
        Crée un village et l'ajoute à la liste des villages dirigés par le seigneur (dictionnaire)
        """
        nom = nom_aleatoire_village()
        self._dico_villages[pid] = Village(pid, nom)

    def nourrir_soldats(self):
        """
        Retourne 0 si le seigneur a assez de ressources pour nourrir ses soldats
        Retourne le nombre de ressources manquantes sinon (ce sera le nombre de soldats qui seront morts de faim)
        """
        deces = 0
        nb_soldats = len(self._liste_soldats) # effectif armée

        if self._ressources < nb_soldats:
            deces = nb_soldats - self._ressources
            self._liste_soldats = self._liste_soldats[:self._ressources]

        return deces
