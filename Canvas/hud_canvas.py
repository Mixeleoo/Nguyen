
import tkinter as tk

from Canvas.base_canvas import BaseCanvas
from Perso import Noble
from jeu import ActionBotInfo
from parameter import *

class HUDCanvas(BaseCanvas):
    def __init__(self, master=None, cnf=None, **kw):
        # C'est PyCharm qui me dit de mettre ça au lieu de cnf={} directement dans les arguments donc...
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        # Initialisation du mode de jeu
        self.game_mode = "basic"

        self.nb_nobles = 0

        # L'id des canvas.after qui sont lancés quand on reste clické sur les boutons de QuantitySelector
        self.after_quantity_selector_id = None

        from eventmanager import EventManager

        self.eventmanager = EventManager(self.jeu, self)

        from Canvas.HUDs.HUDStandard.HUDWindow import HUDWindowSupervisor

        self.to_show_if_cancel = []

        import Canvas.HUDs.HUDStandard.HUDStatic as HUDStatic

        self.hud_actions = HUDStatic.Actions(self)
        self.hud_history = HUDStatic.History(self)
        self.add_history_text = self.hud_history.add_text

        self.hud_build_city = HUDStatic.BuildCity(self)
        self.hud_build_church = HUDStatic.BuildChurch(self)
        self.hud_event = HUDStatic.Event(self)
        self.hud_top_side = HUDStatic.TopSide(self)
        self.update_hudtop = self.hud_top_side.update

        self.hud_end_turn = HUDStatic.EndTurn(self)

        import Canvas.HUDs.HUDStandard as HUDStandard

        self.hudmobile_cestpastonvillage = HUDStandard.CestPasTonVillage(self)
        self.hudmobile_ally_village_info = HUDStandard.AllyVillageInfo(self)
        self.hudmobile_enemy_village_info = HUDStandard.EnemyVillageInfo(self)
        self.hudmobile_yavillage = HUDStandard.YaUnVillage(self)
        self.hudmobile_ilfautfaireunchoix = HUDStandard.IlFautFaireUnChoix(self)
        self.hudmobile_taspasassezdePA = HUDStandard.TasPasAssezDe(self, "e PA")
        self.hudmobile_taspasassezdargent = HUDStandard.TasPasAssezDe(self, "'argent")
        self.hudmobile_taspasassezderessources = HUDStandard.TasPasAssezDe(self, "e ressources")
        self.hudmobile_start_menu = HUDStandard.StartMenu(self)
        self.hudmobile_end_menu = HUDStandard.EndMenu(self)
        self.lose = self.hudmobile_end_menu.lose
        self.win = self.hudmobile_end_menu.win

        self.hudmobile_more_info_event = HUDStandard.MoreInfoEvent(self)

        import Canvas.HUDs.HUDStandard.HUDCentered as HUDCentered

        self.hudinfo_city_full = HUDCentered.CityFull(self)
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
        self.hudinfo_city_full.create()
        self.hudmobile_cestpastonvillage.create()
        self.hudmobile_ally_village_info.create()
        self.hudmobile_enemy_village_info.create()
        self.hudmobile_yavillage.create()
        self.hudmobile_ilfautfaireunchoix.create()
        self.hudmobile_taspasassezdePA.create()
        self.hudmobile_taspasassezdargent.create()
        self.hudmobile_taspasassezderessources.create()
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

    def land_around(self, square_id: int) -> tuple[str, ...]:
        l = ()

        for i in [
            square_id - CARRE_PAR_LIGNE - 1,
            square_id - CARRE_PAR_LIGNE,
            square_id - CARRE_PAR_LIGNE + 1,
            square_id - 1,
            square_id + 1,
            square_id + CARRE_PAR_LIGNE - 1,
            square_id + CARRE_PAR_LIGNE,
            square_id + CARRE_PAR_LIGNE + 1
        ]:
            e = self.square_id_to_tag.get(i, None)
            if e is not None:
                l += (e,)

        return l

    def init_nobles(self):

        # Ajouter un village au joueur
        square_id = self.engine_build_city()

        color = self.hudmobile_start_menu.get_color_choice()
        if color is not None:
            noble = self.jeu.creer_noble(square_id, self.land_around(square_id), color)
            self.itemconfigure(square_id, fill=self.hudmobile_start_menu.get_color_choice())

        else:
            noble = self.jeu.creer_noble(square_id, self.land_around(square_id))
            self.itemconfigure(square_id, fill=noble.couleur)

        village = noble.dico_villages[square_id]

        self.hudmobile_choose_village.choose_village.add_option(village.nom, square_id)
        self.hudmobile_choose_taxes.add_village(village.nom, square_id)

        # Ajouter la fenêtre du village
        self.hudwindow_supervisor.add_more_info(village)

        self.nb_nobles = self.hudmobile_start_menu.get_difficulty_choice()

        # Ajout des villages aléatoirement
        for noble_i in range(self.nb_nobles):

            square_id = self.engine_build_city()

            noble = self.jeu.creer_noble(square_id, self.land_around(square_id))

            # + 1 Pour ne pas compter le premier noble (qui est le joueur)
            self.hudmobile_choose_noble_vassaliser.add_noble(noble.nom, noble_i + 1)
            self.hudcentered_choose_noble_war.add_noble(noble.nom, noble_i + 1)

            self.itemconfigure(square_id, fill=noble.couleur)

        self.update_hudtop()

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
            self.hudmobile_yavillage.show(village_around_id)

        else:
            # Même comportement que si on annulait la construction, sauf que là, on construit
            self.hud_build_city.cancel()

            tags = list(self.gettags(square_id))

            # On lance la méthode qui influera sur le jeu
            village = self.jeu.joueur_actuel.construire_village(village_id=square_id, l_terre=self.land_around(square_id))

            # Comme il y a un nouveau village, il faut update les HUDs qui permet de choisir le village
            self.hudmobile_choose_village.add_village(village.nom, square_id)
            self.hudmobile_choose_taxes.add_village(village.nom, square_id)

            # Ajouter la fenêtre du village
            self.hudwindow_supervisor.add_more_info(village)

            # On change son tag de trigger de fonction
            self.engine_build_city(square_id, tags)
            self.itemconfigure(square_id, fill=self.jeu.joueur_actuel.couleur)

            # On affiche dans l'historique son action
            self.hud_history.add_text("Vous avez créé un village !")

            # On met à jour l'HUD des caractéristiques
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

    def build_church_on_village(self, event: tk.Event):

        village_id = self.find_withtag("active")[0]
        village = self.jeu.joueur_actuel.get_village(village_id)

        if village is not None:
            # Même comportement que si on annulait sa construction, mais on la construit vraiment
            self.hud_build_church.cancel()

            self.jeu.joueur_actuel.construire_eglise(self.find_withtag("active")[0])

            # On met à jour l'HUD des caractéristiques
            self.update_hudtop()

        else:
            self.hudmobile_cestpastonvillage.show(event.x, event.y)

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
                self.win("Vous avez vaincu ou vassalisé tous les nobles\nVous avez gagné.")

            else:
                self.add_history_text("Vous avez vassalisé " + noble_selected.nom)

                # Ajouter le nouveau choix de noble à imposer
                self.hudmobile_choose_taxes.add_noble(noble_selected.nom, noble_selected_index)

                # Retirer le choix de noble à vassaliser et guerre
                self.hudmobile_choose_noble_vassaliser.remove_noble(noble_selected_index)
                self.hudcentered_choose_noble_war.remove_noble(noble_selected_index)

                # Pour chaque village du noble vassalisé, le joueur doit avoir accès aux détails.
                for village in noble_selected.dico_villages.values():
                    self.hudwindow_supervisor.add_more_info(village)

                # On met à jour l'HUD des caractéristiques
                self.update_hudtop()

        else:
            # Vassalisation refusée = guerre déclarée
            # ChatGPT m'a écrit cette phrase ci-dessous.
            self.add_history_text(f"Le noble chevalier, {noble_selected.nom}, a décliné vostre offre avec mépris, et vous adresse une missive cinglante déclarant la guerre !")
            self.war(noble_selected_index, "V")

    def war(self, noble_index: int, cause: Literal["V", "G"]):
        """
        Méthode qui gère la guerre entre le joueur actuel et noble_index
        """

        noble = self.jeu.get_const_joueur(noble_index)

        # Si le joueur remporte la guerre.
        if self.jeu.guerre(noble, cause):

            # S'il est le dernier alors, il a gagné.
            if self.jeu.nb_joueurs == 1:
                self.win("Vous avez vaincu ou vassalisé tous les nobles\nVous avez gagné.")

            else:
                self.add_history_text(f"Vous avez battu {noble.nom}.")

                # Retirer le noble des choix.
                self.hudcentered_choose_noble_war.remove_noble(noble_index)
                self.hudmobile_choose_noble_vassaliser.remove_noble(noble_index)

                for village in noble.dico_villages.values():
                    self.hudmobile_choose_taxes.add_village(village.nom,village.id)
                    self.hudmobile_choose_village.add_village(village.nom,village.id)

                    # Les villages vaincus prennent la couleur du joueur
                    self.itemconfigure(village.id, fill=self.jeu.joueur_actuel.couleur)

                # On met à jour l'HUD des caractéristiques
                self.update_hudtop()

        # Si le joueur perd la guerre
        else:
            if cause == "V":
                self.lose(f"Votre demande de vassalisation n'a pas plu {noble.nom} et en est venu aux mains.\nVotre armée n'était pas de taille. Vous avez perdu")

            else:
                self.lose("Votre tentative est vaine, votre armée n'était pas de taille.\nVous avez perdu")

    def imposer(self, l_villages: list[int], l_nobles: list[int]):
        """
        Méthode appelée lors du clic gauche sur le bouton OK du choix de qui taxer.
        """

        self.jeu.imposer(l_villages, l_nobles)

        phrase = f"vous avez imposé"
        if len(l_villages) > 0 and len(l_nobles) > 0:
            phrase += f" {len(l_villages)} village(s) et {len(l_nobles)} noble(s)"
        elif len(l_villages) > 0:
            phrase += f" {len(l_villages)} village(s)"
        elif len(l_nobles) > 0:
            phrase += f" {len(l_nobles)} noble(s)"
        self.add_history_text(phrase)

        # On met à jour l'HUD des caractéristiques
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
            self.jeu.joueur_actuel.ajout_soldat(quantity)

            # On ajoute le texte descriptif à l'historique.
            self.add_history_text(f"Vous avez recruté {quantity} soldat(s) !")

            # On met à jour l'HUD des caractéristiques.
            self.update_hudtop()

        # Sinon c'est un artisan ou un paysan, il faut donc les immigrer dans un village.
        else:
            # On sauvegarde les choix du type de villageois.
            self.hudmobile_choose_type_villager.last_choice_made = [
                quantity,
                self.itemcget(
                    self.text_id_in_rectangle_id[type_v], "text"
                ).split(" ")[0].lower()
            ]

            # On affiche le choix du village
            self.hudmobile_choose_village.show()

    def immigrer(self, village_id: int):
        """
        Méthode lancée lors du clic gauche sur le bouton OK du choix du village pour l'immigration.
        """

        # Récupération des choix précédemment faits.
        effectif = self.hudmobile_choose_type_villager.last_choice_made[0]
        type_v = self.hudmobile_choose_type_villager.last_choice_made[1]

        # lancer l'immigration du jeu
        v = self.jeu.joueur_actuel.immigrer(
            effectif=effectif,
            type_v=type_v,
            village_id=village_id
        )

        if v is not None:
            self.hudinfo_city_full.show()
            return

        # Ajout du texte descriptif de l'action dans l'historique.
        self.add_history_text(f"Vous avez immigré {effectif} {type_v}{'s' if effectif > 1 else ''} dans le village {self.jeu.joueur_actuel.dico_villages[village_id].nom} !")

        # On met à jour l'HUD des caractéristiques
        self.update_hudtop()

    def end_turn_trigger(self):
        """
        Méthode appelée quand on clique sur fin de tour
        """

        self.jeu.fin_de_tour()

        for rev in self.jeu.joueur_actuel.reaction_revolte():
            if rev.issue is not None:
                # VICTOIRE
                if rev.issue == "Victoire":
                    self.add_history_text(f"Une révolte a eu lieu dans {rev.village.nom}, mais vos soldat ont tenu bon. Les pertes s'élèvent à ", rev.pertes + " villageois.")

                # DEFAITE
                else:
                    self.lose("Vos villageois ont perdu votre confiance et vous fait comprendre leur souffrance.\nVous avez perdu.")

        # Tour des nobles, le temps que ce n'est pas le tour du joueur.
        while self.jeu.index_joueur_actuel != 0:
            actionbotinfo: ActionBotInfo = self.jeu.tour_bots()

            # Si le bot a fait la guerre.
            if actionbotinfo.type == "Guerre":

                # Si le joueur est vaincu, il a perdu.
                if actionbotinfo.noble_vaincu == self.jeu.get_joueur(0):
                    self.lose(f"{self.jeu.joueur_actuel.nom} vous a pris pour cible et vous a vaincu.\nVous avez perdu.")

                # Si ce n'est pas le joueur qui est vaincu:
                else:
                    self.add_history_text(actionbotinfo.descriptif)
                    self.hudcentered_choose_noble_war.remove_noble(actionbotinfo.noble_vaincu.id)
                    self.hudmobile_choose_noble_vassaliser.remove_noble(actionbotinfo.noble_vaincu.id)

            # Si le bot choisit de vassaliser
            elif actionbotinfo.type == "Vassaliser":

                # Si le joueur est choisi
                if actionbotinfo.noble_vassalise == self.jeu.get_joueur(0):
                    """On permet vraiment au joueur d'accepter de se faire vassaliser ? ça serait marrant"""
                    pass

                # Si ce n'est pas un noble qui est visé
                else:

                    # Un noble vassalisé ne peut plus être vassalisé.
                    self.hudmobile_choose_noble_vassaliser.remove_noble(actionbotinfo.noble_vaincu.id)

            elif actionbotinfo.type == "Village":

                square_id = self.engine_build_city()

                tags = list(self.gettags(square_id))

                # On lance la méthode qui influera sur le jeu
                village = self.jeu.joueur_actuel.construire_village(
                    village_id=square_id, l_terre=self.land_around(square_id)
                )

                # Ajouter la fenêtre du village
                self.hudwindow_supervisor.add_more_info(village)

                # On change son tag de trigger de fonction
                self.engine_build_city(square_id, tags)
                self.itemconfigure(square_id, fill=self.jeu.joueur_actuel.couleur)

                # On affiche dans l'historique son action
                self.hud_history.add_text(f"{self.jeu.joueur_actuel.nom} a créé un village !")

                # On met à jour l'HUD des caractéristiques
                self.update_hudtop()

            # Ajout du texte
            self.add_history_text(actionbotinfo.descriptif)

        #self.jeu.joueur_actuel.reset_pa()
        joueur_vivant = self.eventmanager.handle_event()

        if joueur_vivant:
            for p in self.jeu.fin_annee():
                self.add_history_text(p)

            self.add_history_text(f"Année n°{self.jeu.tour}")
            self.update_hudtop()

    def event_accept_vassal(self, n: Noble):

        noble_index = self.jeu.get_joueur_index(n)
        self.jeu.vassalisation_confirmee(n, 0, 0)

        if self.jeu.nb_joueurs == 1:
            self.hudmobile_end_menu.win("Vous avez accepté la proposition de vassalisation du dernier Noble, sage de votre part.\nVous avez gagné.")

        else:
            self.add_history_text("Vous avez vassalisé " + n.nom)

            # Ajouter le nouveau choix de noble à imposer
            self.hudmobile_choose_taxes.add_noble(n.nom, noble_index)

            # Retirer le choix de noble à vassaliser et guerre
            self.hudmobile_choose_noble_vassaliser.remove_noble(noble_index)
            self.hudcentered_choose_noble_war.remove_noble(noble_index)

            # On met à jour l'HUD des caractéristiques
            self.update_hudtop()

    def start(self, e):
        self.init_nobles()
        self.hudmobile_start_menu.hide()

        # Début du tutoriel
        # TODO Léo : tutoriel

    def restart(self, e):
        self.hudmobile_choose_taxes.choose_villages.default()
        self.hudmobile_choose_taxes.choose_nobles.default()
        self.hudmobile_choose_noble_vassaliser.choose_noble.default()
        self.hudmobile_choose_village.choose_village.default()
        self.hudcentered_choose_noble_war.choose_noble.default()

        self.delete("all")
        self.create_HUDs(self.winfo_width(), self.winfo_height())
        self.jeu.restart()
