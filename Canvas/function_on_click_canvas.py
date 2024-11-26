
import tkinter as tk

from Canvas.animation_canvas import AnimationCanvas
from parameter import *


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

        self.basic_mode_tag_foc = {
            PLAINE_TAG: lambda e: None,
            VILLAGE_TAG: self.hudmobile_village_info.show,
            MORE_INFO_TAG: self.hudmobile_more_info.show,
            CHANGE_PAGE_MINUS: self.hud_actions.on_change_page,
            CHANGE_PAGE_PLUS: self.hud_actions.on_change_page,
            HIDE_PAGE: self.hud_actions.hide_animation,
            SHOW_PAGE: self.hud_actions.show_animation,
            HIDE_HISTORY: self.hud_history.hide_animation,
            SHOW_HISTORY: self.hud_history.show_animation,
            BUILD_CITY: self.build_city,
            BUILD_CHURCH: self.build_church,
            IMMIGRATE_TAG: self.hud_paysan_or_artisan.immigrate,
            CANCEL_IMMIGRATION_TAG: self.hud_paysan_or_artisan.cancel_immigration,
            PLUS_IMMIGRANTS_TAG: self.hud_paysan_or_artisan.plus_immigrants,
            MINUS_IMMIGRANTS_TAG: self.hud_paysan_or_artisan.minus_immigrants,
            CLOSE_MORE_INFO_WINDOW: self.hudmobile_more_info.hide,
            PIN_MORE_INFO_WINDOW: self.pin_more_info_window,
            OK_EVENT_TAG: self.hud_event.hide,
            INFO_EVENT_TAG: self.hudmobile_more_info.show,
            PAYSAN_OR_ARTISAN_TAG: self.hud_paysan_or_artisan.show,
            NOTHING_TAG: lambda e: None
        }

        self.build_city_mode_tag_foc = dict(self.basic_mode_tag_foc)
        self.build_city_mode_tag_foc[PLAINE_TAG] = self.build_city_on_plain
        self.build_city_mode_tag_foc[SHOW_PAGE] = lambda e: None
        self.build_city_mode_tag_foc[CHANGE_PAGE_MINUS] = lambda e: None
        self.build_city_mode_tag_foc[CHANGE_PAGE_PLUS] = lambda e: None
        self.build_city_mode_tag_foc[CANCEL_BUILD_CITY_TAG] = self.cancel_build_city

        self.build_church_mode_tag_foc = dict(self.build_city_mode_tag_foc)
        self.build_church_mode_tag_foc[PLAINE_TAG] = lambda e: None
        self.build_church_mode_tag_foc[VILLAGE_TAG] = self.build_church_on_village
        self.build_church_mode_tag_foc[CANCEL_BUILD_CHURCH] = self.cancel_build_church

        self.tag_foc = {
            "basic": self.basic_mode_tag_foc,
            "build_city": self.build_city_mode_tag_foc,
            "build_church": self.build_church_mode_tag_foc
        }

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
            # Même comportement que si on annulait la construction, sauf que là on construit
            self.cancel_build_city()

            tags = list(self.gettags(square_id))

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

    def pin_more_info_window(self, event: tk.Event):
        if TEMP_TAG in self.gettags(CLOSE_MORE_INFO_WINDOW):
            # On empêche de unhighlight l'objet
            self.dtag("highlight", "highlight")

            # La fenêtre ne devient plus temporaire
            self.dtag(MORE_INFO_WINDOW, TEMP_TAG)

        else:
            self.addtag_withtag(TEMP_TAG, MORE_INFO_WINDOW)
