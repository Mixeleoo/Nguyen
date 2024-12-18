
import tkinter as tk

from Canvas.base_canvas import BaseCanvas
from Perso.noble import Noble
from Territoire.village import Village
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

        from Canvas.HUDs.HUDWindow import HUDWindowSupervisor

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
        self.hudmobile_taspasassezdePAgros = HUDMobile.TasPasAssezDePAGros(self)
        self.hudmobile_start_menu = HUDMobile.StartMenu(self)
        self.hudmobile_end_menu = HUDMobile.EndMenu(self)
        self.hudmobile_more_info_event = HUDMobile.MoreInfoEvent(self)

        import Canvas.HUDs.HUDCentered as HUDCentered

        self.hudmobile_choose_type_villager = HUDCentered.ChooseTypeVillager(self)
        self.hudmobile_choose_taxes = HUDCentered.ChooseTaxes(self)
        self.hudmobile_choose_village = HUDCentered.ChooseVillage(self)
        self.hudmobile_choose_noble_vassaliser = HUDCentered.ChooseNobleVassaliser(self)
        self.hudmobile_choose_arg_res = HUDCentered.ChooseArgRes(self)
        self.hudcentered_choose_noble_war = HUDCentered.ChooseNobleWar(self)
        self.hudcentered_accept_vassal = HUDCentered.AcceptVassal(self)
        self.hudcentered_results_war = HUDCentered.ResultsWar(self)

        self.hudwindow_supervisor = HUDWindowSupervisor(self)

    def create_HUDs(self, geometry_width: int, geometry_height: int):

        # HUDs permanants
        self.hud_actions.create(geometry_width, geometry_height)
        self.hud_history.create(geometry_width, geometry_height)
        self.hud_build_city.create(geometry_width, geometry_height)
        self.hud_build_church.create(geometry_width, geometry_height)
        self.hud_event.create(geometry_width, geometry_height)
        self.hud_end_turn.create(geometry_width, geometry_height)
        self.hudmobile_end_menu.create(geometry_width, geometry_height)

        # HUDs mobile
        self.hudmobile_village_info.create()
        self.hudmobile_yavillagegros.create()
        self.hudmobile_ilfautfaireunchoixgros.create()
        self.hudmobile_taspasassezdePAgros.create()
        self.hudmobile_more_info_event.create(geometry_width, geometry_height)

        # HUD centrés
        self.hudmobile_choose_type_villager.create()
        self.hudmobile_choose_village.create()
        self.hudmobile_choose_noble_vassaliser.create()
        self.hudmobile_choose_taxes.create()
        self.hudmobile_choose_arg_res.create()
        self.hudcentered_choose_noble_war.create()
        self.hudcentered_accept_vassal.create()
        self.hudcentered_results_war.create()

        self.init_nobles()

        self.hud_top_side.create(geometry_width, geometry_height)
        self.hudmobile_start_menu.create(geometry_width, geometry_height)

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

        village = self.jeu.creer_noble(square_id, prenom_aleatoire(), nom)

        # Ajouter la fenêtre du village
        self.hudwindow_supervisor.add_more_info(village)

        # Ajout des villages aléatoirement
        for noble in range(NB_NOBLE_AU_DEPART):

            square_id = self.engine_build_city()
            prenom = prenom_aleatoire()
            nom_village = nom_aleatoire_village()

            # + 1 Pour ne pas compter le premier noble (qui est le joueur)
            self.hudmobile_choose_noble_vassaliser.add_noble(prenom, noble + 1)
            self.hudcentered_choose_noble_war.add_noble(prenom, noble + 1)
            village = self.jeu.creer_noble(square_id, prenom, nom_village)

            # Ajouter la fenêtre du village
            self.hudwindow_supervisor.add_more_info(village)

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

            # On retire les points d'actions du joueur et on met à jour l'HUD des caractéristiques
            self.jeu.joueur_actuel.retirer_pa(8)
            self.update_hudtop()

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

        # On retire les points d'actions du joueur et on met à jour l'HUD des caractéristiques
        self.jeu.joueur_actuel.retirer_pa(6)
        self.update_hudtop()

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

            if self.jeu.nb_joueurs == 1:
                self.hudmobile_end_menu.win()

            else:
                self.add_history_text("Vous avez vassalisé " + noble_selected.nom)

                # Ajouter le nouveau choix de noble à imposer
                self.hudmobile_choose_taxes.add_noble(noble_selected.nom, noble_selected_index)

                # Retirer le choix de noble à vassaliser et guerre
                self.hudmobile_choose_noble_vassaliser.remove_noble(noble_selected_index)
                self.hudcentered_choose_noble_war.remove_noble(noble_selected_index)

                # On retire les points d'actions du joueur et on met à jour l'HUD des caractéristiques
                self.jeu.joueur_actuel.retirer_pa(4)
                self.update_hudtop()

        else:
            # TODO Léo: Vassalisation refusée -> guerre
            pass

    def war(self, noble_index: int):

        noble = self.jeu.get_const_joueur(noble_index)
        # Si le joueur remporte la guerre.
        if self.jeu.guerre(noble):

            # S'il est le dernier alors, il a gagné.
            if self.jeu.nb_joueurs == 1:
                self.hudmobile_end_menu.win()

            else:
                self.add_history_text(f"Tu as battu {noble.nom}.")

                self.hudcentered_choose_noble_war.remove_noble(noble_index)
                self.hudmobile_choose_noble_vassaliser.remove_noble(noble_index)

                # On retire les points d'actions du joueur et on met à jour l'HUD des caractéristiques
                self.jeu.joueur_actuel.retirer_pa(8)
                self.update_hudtop()

        else:
            self.hudmobile_end_menu.lose()

    def imposer(self, l_villages: list[int], l_nobles: list[int]):
        self.jeu.imposer(l_villages, l_nobles)

        # On retire les points d'actions du joueur et on met à jour l'HUD des caractéristiques
        self.jeu.joueur_actuel.retirer_pa(5)
        self.update_hudtop()

    def save_villager_choice(self, type_v: int, quantity: int):
        """
        Méthode lancée lors du clic gauche sur le bouton OK du choix du type de villageois.
        """

        # Si le choix fait est soldat, alors pas besoin de choisir dans quel village l'immigrer.
        if self.itemcget(
                self.text_id_in_rectangle_id[type_v], "text"
        ).split(" ")[0].lower() == "soldat":

            # On lance la méthode du jeu.
            self.jeu.recruter_soldat(quantity)

            # On ajoute le texte descriptif à l'historique.
            self.add_history_text(f"Vous avez recruté {quantity} soldat(s) !")

            # On met à jour l'HUD des caractéristiques.
            self.update_hudtop()

        # Sinon c'est un artisan ou un paysan, il faut donc les immigrer dans un village.
        else:
            self.hudmobile_choose_type_villager.last_choice_made = [
                quantity,
                self.itemcget(
                    self.text_id_in_rectangle_id[type_v], "text"
                ).split(" ")[0].lower()
            ]

            # On affiche le choix du village
            self.hudmobile_choose_village.show()

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

        # On retire les points d'actions du joueur et on met à jour l'HUD des caractéristiques
        if type_v == "artisan": self.jeu.joueur_actuel.retirer_pa(effectif * 2)
        else: self.jeu.joueur_actuel.retirer_pa(effectif)
        self.update_hudtop()

    def event(self):
        res = self.jeu.evenement()

        events = {
            "Incendie": self.event_incendie,
            "Vassalisation": self.event_vassalisation
        }

        events.get(res[0], self.event_autre)(*res)

    def event_incendie(self, type_ev: str, texts: list[str, ...], v: Village):
        if not len(self.jeu.joueur_actuel.dico_villages):
            self.hudmobile_end_menu.lose()

        else:
            # TODO Léo: Retirer le village de la carte.
            self.hudmobile_choose_taxes.remove_village(v.id)
            pass

        self.hudmobile_more_info_event.refresh_text(v.nom)

    def event_vassalisation(self, type_ev: str, texts: tuple[str], n: Noble):
        self.hudcentered_accept_vassal.show(n)
        self.hudmobile_more_info_event.refresh_text(texts)

    def event_accept_vassal(self, n: Noble):

        noble_index = self.jeu.get_joueur_index(n)
        self.jeu.vassalisation_confirmee(n, 0, 0)

        if self.jeu.nb_joueurs == 1:
            self.hudmobile_end_menu.win()

        else:
            self.add_history_text("Vous avez vassalisé " + n.nom)

            # Ajouter le nouveau choix de noble à imposer
            self.hudmobile_choose_taxes.add_noble(n.nom, noble_index)

            # Retirer le choix de noble à vassaliser et guerre
            self.hudmobile_choose_noble_vassaliser.remove_noble(noble_index)
            self.hudcentered_choose_noble_war.remove_noble(noble_index)

            # On met à jour l'HUD des caractéristiques
            self.update_hudtop()

    def event_autre(self, type_ev: str, texts: tuple[str], *args):

        self.hudmobile_more_info_event.refresh_text(texts)
        self.update_hudtop()

        self.hud_event.set_text(type_ev)
        self.hud_event.show_animation()

    def end_turn_trigger(self):
        self.jeu.fin_de_tour()
        rev = self.jeu.joueur_actuel.reaction_revolte()
        if rev:
            # VICTOIRE
            if rev[0] == "V":
                self.hudcentered_results_war.show(rev[1])

            # DEFAITE
            else:
                self.hudmobile_end_menu.lose()

        # Tour des nobles.

        while self.jeu.index_joueur_actuel != 0:
            self.jeu.tour_noble()
            # TODO Léo: Gérer le cas de l'affichage des guerres déclenchées par les bots et si on s'est fait vaincre.
            # TODO Léo: Gérer le cas des vassalisations, supprimer le noble des choix.

        self.event()
