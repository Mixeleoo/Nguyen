
import tkinter as tk

from Canvas.base_canvas import BaseCanvas
from parameter import *

class HUDCanvas(BaseCanvas):
    def __init__(self, master=None, cnf=None, **kw):
        # C'est PyCharm qui me dit de mettre ça au lieu de cnf={} directement dans les arguments donc...
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        # Initialisation du mode de jeu
        self.game_mode = "basic"

        # L'id des canvas.after qui sont lancés quand on reste clické sur les boutons de QuantitySelector
        self.after_quantity_selector_id = None

        from Canvas.HUDs.HUDWindow import HUDWindowMoreInfoSupervisor

        self.to_show_if_cancel = []

        import Canvas.HUDs.HUDStandard as HUDStandard

        self.hud_actions = HUDStandard.Actions(self)
        self.hud_history = HUDStandard.History(self)
        self.add_history_text = self.hud_history.add_text

        self.hud_build_city = HUDStandard.BuildCity(self)
        self.hud_build_church = HUDStandard.BuildChurch(self)
        self.hud_event = HUDStandard.Event(self)
        self.hud_top_side = HUDStandard.TopSide(self)
        self.update_hudtop = self.hud_top_side.update

        self.hud_end_turn = HUDStandard.EndTurn(self)

        import Canvas.HUDs.HUDMobile as HUDMobile

        self.hudmobile_village_info = HUDMobile.VillageInfo(self)
        self.hudmobile_yavillagegros = HUDMobile.YaUnVillageGros(self)
        self.hudmobile_ilfautfaireunchoixgros = HUDMobile.IlFautFaireUnChoixGros(self)

        import Canvas.HUDs.HUDCentered as HUDCentered

        self.hudmobile_choose_type_villager = HUDCentered.ChooseTypeVillager(self)
        self.hudmobile_choose_taxes = HUDCentered.ChooseTaxes(self)
        self.hudmobile_choose_village = HUDCentered.ChooseVillage(self)
        self.hudmobile_choose_noble_vassaliser = HUDCentered.ChooseNobleVassaliser(self)
        self.hudmobile_choose_arg_res = HUDCentered.ChooseArgRes(self)
        self.hudcentered_choose_noble_war = HUDCentered.ChooseNobleWar(self)

        self.hudwindow_more_info_supervisor = HUDWindowMoreInfoSupervisor(self)

    def create_HUDs(self, geometry_width: int, geometry_height: int):

        # HUDs permanants
        self.hud_actions.create(geometry_width, geometry_height)
        self.hud_history.create(geometry_width, geometry_height)
        self.hud_build_city.create(geometry_width, geometry_height)
        self.hud_build_church.create(geometry_width, geometry_height)
        self.hud_event.create(geometry_width, geometry_height)
        self.hud_end_turn.create(geometry_width, geometry_height)

        # HUDs mobile
        self.hudmobile_village_info.create()
        self.hudmobile_yavillagegros.create()
        self.hudemobile_ilfautfaireunchoixgros.create()

        # HUD centrés
        self.hudmobile_choose_type_villager.create()
        self.hudmobile_choose_village.create()
        self.hudmobile_choose_noble_vassaliser.create()
        self.hudmobile_choose_taxes.create()
        self.hudmobile_choose_arg_res.create()
        self.hudcentered_choose_noble_war.create()

        for i in range(NB_NOBLE_AU_DEPART):
            self.hudwindow_more_info_supervisor.add()

        self.init_nobles()

        self.hud_top_side.create(geometry_width, geometry_height)

    def hide_all_permanant_huds(self):
        # On simule un clic sur le bouton qui cache les pages d'actions
        if self.hud_actions.state == "normal":
            self.hud_actions.bhide()
            self.to_show_if_cancel += [self.hud_actions.bshow]

        # On simule un clic sur le bouton qui cache l'historique
        if self.hud_history.state == "normal":
            self.hud_history.bhide()
            self.to_show_if_cancel += [self.hud_history.bshow]

        self.hud_end_turn.hide_animation()
        self.to_show_if_cancel += [self.hud_end_turn.show_animation]

    def show_hidden_permanant_huds(self):
        # Réafficher les HUDs cachés lorsque le joueur a cliqué sur l'action pour construire un village
        for f in self.to_show_if_cancel:
            f()

        self.to_show_if_cancel = []

    def init_nobles(self):
        # Ajouter un village au joueur
        square_id = self.engine_build_city()

        nom = nom_aleatoire_village()
        self.hudmobile_choose_village.choose_village.add_option(nom, square_id)
        self.hudmobile_choose_taxes.add_village(nom, square_id)

        self.jeu.creer_noble(square_id, prenom_aleatoire(), nom)

        # Ajout des villages aléatoirement
        for noble in range(NB_NOBLE_AU_DEPART):
            square_id = self.engine_build_city()
            prenom = prenom_aleatoire()

            # + 1 Pour ne pas compter le premier noble (qui est le joueur)
            self.hudmobile_choose_noble_vassaliser.add_noble(prenom, noble + 1)
            self.hudcentered_choose_noble_war.add_noble(prenom, noble + 1)
            self.jeu.creer_noble(square_id, prenom, nom_aleatoire_village())

    def choose_plain_to_build(self, event: tk.Event):
        """
        Uniquement s'il y a la possibilité, on cache les HUDs, et on affiche le texte disant : Où voulez-vous construire
        votre village ? Passage en mode citybuilding mgl
        """
        # On eclaircit la zone
        self.hide_all_permanant_huds()

        # On affiche le rectangle de construction
        self.hud_build_city.show_animation()

        self.game_mode = "build_city"

    def build_city_on_plain(self, event: tk.Event):
        """
        Cette fonction crée un village si le joueur clique sur une plaine qui n'a pas de villages aux alentours.
        Elle affiche également les HUDs qui étaient précédemment affichés avant de construire le village.
        """
        # Modifier la case en village
        square_id = self.find_withtag("active")[0]
        village_around_id = self.villages_around(square_id)

        if village_around_id:
            self.hudmobile_yavillagegros.show(village_around_id)

        else:
            # Même comportement que si on annulait la construction, sauf que là, on construit
            self.hud_build_city.cancel()

            tags = list(self.gettags(square_id))

            # Comme il y a un nouveau village, il faut update les HUDs qui permet de choisir le village
            nom = nom_aleatoire_village()
            self.hudmobile_choose_village.add_village(nom, square_id)
            self.hudmobile_choose_taxes.add_village(nom, square_id)

            # On lance la méthode qui influera sur le jeu
            self.jeu.construire_village(village_id=square_id, nom=nom)

            # On change son tag de trigger de fonction
            self.engine_build_city(square_id, tags)

            # On affiche dans l'historique son action
            self.hud_history.add_text("Le joueur a crée un village !")

    def choose_village_to_build(self, event: tk.Event):
        """
        Uniquement s'il y a la possibilité, on cache les HUDs, et on affiche le texte disant : Où voulez-vous construire
        votre eglise ? Passage en mode churchbuilding mgl
        """
        self.hide_all_permanant_huds()

        # On affiche le rectangle de construction
        self.hud_build_church.show_animation()

        self.game_mode = "build_church"

    def build_church_on_village(self, e=None):

        # Même comportement que si on annulait sa construction, mais on la construit vraiment
        self.hud_build_church.cancel()

        self.jeu.construire_eglise(self.find_withtag("active")[0])

    def vassaliser(self, don_argent: int, don_ressources: int):

        noble_selected_index = self.hudmobile_choose_noble_vassaliser.noble_index_selected
        noble_selected = self.jeu.get_const_joueur(noble_selected_index)

        if self.jeu.joueur_actuel.soumettre(
                noble_selected, don_argent, don_ressources
        ):
            self.jeu.vassalisation_confirmee(
                noble_selected,
                don_argent,
                don_ressources
            )

            self.add_history_text("Vous avez vassalisé " + noble_selected.nom)

            # Ajouter le nouveau choix de noble à imposer
            self.hudmobile_choose_taxes.add_noble(noble_selected.nom, noble_selected_index)

            # Retirer le choix de noble à vassaliser et guerre
            self.hudmobile_choose_noble_vassaliser.remove_noble(noble_selected_index)
            self.hudcentered_choose_noble_war.remove_noble(noble_selected_index)

            # Mettre à jour l'HUD d'en haut
            self.update_hudtop()

    def war(self, noble_index: int):

        noble = self.jeu.get_const_joueur(noble_index)
        if self.jeu.guerre(noble):
            self.add_history_text(f"Tu as battu {noble.nom}.")

            self.hudcentered_choose_noble_war.remove_noble(noble_index)
            self.hudmobile_choose_noble_vassaliser.remove_noble(noble_index)
            self.update_hudtop()

        else:
            self.add_history_text(f"{noble.nom} vous a battu.")

    def imposer(self, l_villages: list[int], l_nobles: list[int]):
        self.jeu.imposer(l_villages, l_nobles)
        self.update_hudtop()

    def immigrer(self, village_id: int):

        effectif = self.hudmobile_choose_type_villager.last_choice_made[0]
        type_v = self.hudmobile_choose_type_villager.last_choice_made[1]

        # lancer l'immigration du jeu
        self.jeu.immigrer(
            effectif=effectif,
            type_v=type_v,
            village_id=village_id
        )

        self.add_history_text(f"Vous avez immigré {effectif} {type_v} dans le village {village_id} !")
        self.update_hudtop()
