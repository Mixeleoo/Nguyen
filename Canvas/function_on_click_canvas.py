
import tkinter as tk

from parameter import *
from Canvas.animation_canvas import AnimationCanvas


class FunctionOnClickCanvas(AnimationCanvas):
    """
    Class squelette qui servira à d'autres class à en hériter des fonctions et à en spécifier les actions
    en fonction du mode de jeu
    PS : Le "Click" ici est considéré comme un click confirmé, donc au relâchement après aucuns mouvements.
    """
    def __init__(self, master=None, cnf=None, **kw):
        # C'est PyCharm qui me dit de mettre ça au lieu de cnf={} directement dans les arguments donc...
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        self.game_mode = "basic"

        self.basic_mode_tag_foc[PLAINE_TAG] = lambda e: None
        self.basic_mode_tag_foc[VILLAGE_TAG] = self.hudmobile_village_info.show
        self.basic_mode_tag_foc[MORE_INFO_TAG] = lambda *args: self.hudwindow_more_info_supervisor.get_active_window().show()
        self.basic_mode_tag_foc[CHANGE_PAGE_PLUS] = self.hud_actions.on_change_page
        self.basic_mode_tag_foc[CHANGE_PAGE_MINUS] = self.hud_actions.on_change_page
        self.basic_mode_tag_foc[HIDE_PAGE] = self.hud_actions.hide_page
        self.basic_mode_tag_foc[SHOW_PAGE] = self.hud_actions.show_page
        self.basic_mode_tag_foc[HIDE_HISTORY] = self.hud_history.hide_history
        self.basic_mode_tag_foc[SHOW_HISTORY] = self.hud_history.show_history
        self.basic_mode_tag_foc[BUILD_CITY] = self.build_city
        self.basic_mode_tag_foc[BUILD_CHURCH] = self.build_church
        self.basic_mode_tag_foc[CHOOSE_VILLAGE_TO_IMMIGRATE_TAG] = self.hud_paysan_or_artisan.immigrate
        self.basic_mode_tag_foc[CANCEL_IMMIGRATION_TAG] = self.hud_paysan_or_artisan.cancel_immigration
        self.basic_mode_tag_foc[IMMIGRATE_TAG] = self.hud_choose_village.immigrate
        self.basic_mode_tag_foc[CANCEL_CHOOSE_VILLAGE_TO_IMMIGRATE_TAG] = self.hud_choose_village.hide
        self.basic_mode_tag_foc[PLUS_IMMIGRANTS_TAG] = self.hud_paysan_or_artisan.plus_immigrants
        self.basic_mode_tag_foc[MINUS_IMMIGRANTS_TAG] = self.hud_paysan_or_artisan.minus_immigrants
        self.basic_mode_tag_foc[CLOSE_MORE_INFO_WINDOW] = lambda *args: self.hudwindow_more_info_supervisor.get_active_window().hide()
        self.basic_mode_tag_foc[PIN_MORE_INFO_WINDOW] = lambda *args: self.hudwindow_more_info_supervisor.get_active_window().pin()
        self.basic_mode_tag_foc[OK_EVENT_TAG] = self.hud_event.hide
        self.basic_mode_tag_foc[INFO_EVENT_TAG] = lambda e: None
        self.basic_mode_tag_foc[PAYSAN_OR_ARTISAN_TAG] = self.hud_paysan_or_artisan.show
        self.basic_mode_tag_foc[NOTHING_TAG] = lambda e: None


        self.build_city_mode_tag_foc[PLAINE_TAG] = self.build_city_on_plain
        self.build_city_mode_tag_foc[SHOW_PAGE] = lambda e: None
        self.build_city_mode_tag_foc[CHANGE_PAGE_MINUS] = lambda e: None
        self.build_city_mode_tag_foc[CHANGE_PAGE_PLUS] = lambda e: None
        self.build_city_mode_tag_foc[CANCEL_BUILD_CITY_TAG] = self.cancel_build_city

        self.build_church_mode_tag_foc[PLAINE_TAG] = lambda e: None
        self.build_church_mode_tag_foc[VILLAGE_TAG] = self.build_church_on_village
        self.build_church_mode_tag_foc[CANCEL_BUILD_CHURCH] = self.cancel_build_church

        self.to_show_if_cancel = []

    def build_city(self, event: tk.Event):
        """
        Uniquement s'il y a la possibilité, on cache les HUD, et on affiche le texte disant : Où voulez-vous construire
        votre village ? Passage en mode citybuilding mgl
        """
        # On simule un clic sur le bouton qui cache les ppages d'actions
        if self.find_withtag(HIDE_PAGE):
            self.hud_actions.hide_page()
            self.to_show_if_cancel += [self.hud_actions.show_page]

        # On simule un clic sur le bouton qui cache l'historique
        if self.find_withtag(HIDE_HISTORY):
            self.hud_history.hide_history()
            self.to_show_if_cancel += [self.hud_history.show_history]

        # On affiche le rectangle de construction
        self.hud_build_city.show_animation()

        self.game_mode = "build_city"

    def cancel_build_city(self, e=None):
        # Réafficher les HUD cachés lorsque le joueur a cliqué sur l'action pour construire un village
        for f in self.to_show_if_cancel:
            f()

        self.to_show_if_cancel = []

        self.hud_build_city.hide_animation()
        self.game_mode = "basic"

    def build_city_on_plain(self, event: tk.Event):
        """
        Cette fonction créé un village si le joueur clique sur une plaine qui n'a pas de villages aux alentours
        Elle affiche également les HUD qui étaient précédemment affichés avant de construire le village
        """
        # Modifier la case en village
        square_id = self.find_withtag("active")[0]
        village_around_id = self.villages_around(square_id)

        if village_around_id:
            self.hudmobile_yavillagegros.show(village_around_id)

        else:
            # Même comportement que si on annulait la construction, sauf que là, on construit
            self.cancel_build_city()

            tags = list(self.gettags(square_id))

            # Comme il y a un nouveau village, il faut update l'HUD qui permet de choisir le village
            new_option_id = self.hud_choose_village.add_village_update_HUD("village 2")
            self.radiobuttons.add_option(tags[GROUP_TAG_INDEX], new_option_id)

            # On change son tag de trigger de fonction
            tags[TRIGGER_TAG_INDEX] = VILLAGE_TAG
            self.itemconfigure(square_id, fill="orange", tags=tags)

    def build_church(self, event: tk.Event):
        """
        Uniquement s'il y a la possibilité, on cache les HUD, et on affiche le texte disant : Où voulez-vous construire
        votre eglise ? Passage en mode churchbuilding mgl
        """
        # On simule un clic sur le bouton qui cache les ppages d'actions
        if self.find_withtag(HIDE_PAGE):
            self.hud_actions.hide_page()
            self.to_show_if_cancel += [self.hud_actions.show_page]

        # On simule un clic sur le bouton qui cache l'historique
        if self.find_withtag(HIDE_HISTORY):
            self.hud_history.hide_history()
            self.to_show_if_cancel += [self.hud_history.show_history]

        # On affiche le rectangle de construction
        self.hud_build_church.show_animation()

        self.game_mode = "build_church"

    def cancel_build_church(self, e=None):
        # Réafficher les HUD cachés lorsque le joueur a cliqué sur l'action pour construire un village
        for f in self.to_show_if_cancel:
            f()

        self.to_show_if_cancel = []

        self.hud_build_church.hide_animation()
        self.game_mode = "basic"

    def build_church_on_village(self, e=None):

        # Même comportement que si on annulait sa construction, mais on la construit vraiment
        self.cancel_build_church()

        print("TU AS CONSTRUIT UNE EGLISE GG")
