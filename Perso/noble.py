from Perso.personne import Personne
from Perso.soldat import Soldat
from Territoire.village import Village
from parameter import nom_aleatoire_village, prenom_aleatoire


class Noble(Personne):

    """
    Un noble est une personne qui contôle des roturiers (sous forme d'une liste de roturiers)
    il est également soumis à un impôt s'il est vassal d'un seigneur (10%).
    """
    def __init__(self, pnom: str, pres: int, parg: int):
        Personne.__init__(self, pnom, pres, parg)
        self._taux_impot = 0.10

        # Dictionnaire des villages que le noble dirige avec la structure suivante : identifiant_village : int -> Village
        # Servira a accéder à la liste de Roturiers que le noble possède
        self._dico_villages: dict[int, Village] = {}

        # Liste des soldats sous les ordres du noble
        self._liste_soldats: list[Soldat] = []


    @property
    def dico_villages(self):
        return self._dico_villages

    def prend_impot_village(self, pid_village: int) -> tuple[int, int]:
        """
        Ajoute aux ressources du noble les impot perçu pour chaque roturier sous ses ordres dans le village mis en paramètre
        """
        impot_total_arg = 0
        impot_total_res = 0

        for roturier in self._dico_villages[pid_village].liste_roturier :
            impot_percu = roturier.payer_impot() # recupération du tuple (roturier.argent, roturier.ressources)
            impot_total_arg += impot_percu[0]
            impot_total_res += impot_percu[1]

        self._argent += impot_total_arg
        self._ressources += impot_total_res

        return impot_total_arg, impot_total_res

    def ajouter_village(self, pid: int):
        """
        Crée un village et l'ajoute à la liste des villages dirigés par le seigneur (dictionnaire)
        """
        nom = nom_aleatoire_village()
        self._dico_villages[pid] = Village(pid, nom)

    def ajout_soldat(self, peffectif: int):
        """
        Méthode qui ajouter peffectif soldats dans sa liste de soldats

        :param peffectif:
        """
        for _ in range(peffectif):
            self._liste_soldats += [Soldat(prenom_aleatoire())]

    def nourrir_soldats(self) -> int:
        """
        Retourne 0 si le seigneur a assez de ressources pour nourrir ses soldats
        Retourne le nombre de ressources manquantes sinon (ce sera le nombre de soldats qui seront morts de faim)
        """
        deces = 0
        nb_soldats = len(self._liste_soldats) # effectif armé

        if self._ressources < nb_soldats:
            deces = nb_soldats - self._ressources
            self._liste_soldats = self._liste_soldats[:self._ressources]

        return deces
