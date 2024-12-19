
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

        self.actions = {
            BUILD_CITY: self.choose_plain_to_build,
            BUILD_CHURCH: self.choose_village_to_build,
            PAYSAN_OR_ARTISAN_TAG: self.hudmobile_choose_type_villager.show,
            TAXES_TAG: self.hudmobile_choose_taxes.show,
            VASSALIZE_TAG: self.hudmobile_choose_noble_vassaliser.show,
            WAR_TAG: self.hudcentered_choose_noble_war.show
        }

        self.basic_mode_tag_foc[PLAINE_TAG] = dummy
        self.basic_mode_tag_foc[VILLAGE_TAG] = self.hudmobile_village_info.show
        self.basic_mode_tag_foc[BUILD_CITY] = lambda e: self.before_action(BUILD_CITY, e)
        self.basic_mode_tag_foc[BUILD_CHURCH] = lambda e: self.before_action(BUILD_CHURCH, e)
        self.basic_mode_tag_foc[INFO_EVENT_TAG] = dummy
        self.basic_mode_tag_foc[PAYSAN_OR_ARTISAN_TAG] = lambda e: self.before_action(PAYSAN_OR_ARTISAN_TAG, e)
        self.basic_mode_tag_foc[TAXES_TAG] = lambda e: self.before_action(TAXES_TAG, e)
        self.basic_mode_tag_foc[VASSALIZE_TAG] = lambda e: self.before_action(VASSALIZE_TAG, e)
        self.basic_mode_tag_foc[WAR_TAG] = lambda e: self.before_action(WAR_TAG, e)
        self.basic_mode_tag_foc[NOTHING_TAG] = dummy

        self.build_city_mode_tag_foc[PLAINE_TAG] = self.build_city_on_plain
        self.build_city_mode_tag_foc[VILLAGE_TAG] = lambda e: print("Y'a déjà un village ici ?")
        self.build_city_mode_tag_foc[NOTHING_TAG] = dummy

        self.build_church_mode_tag_foc[PLAINE_TAG] = dummy
        self.build_church_mode_tag_foc[VILLAGE_TAG] = self.build_church_on_village
        self.build_church_mode_tag_foc[NOTHING_TAG] = dummy

    def before_action(self, tag: str, event: tk.Event):
        if self.jeu.action_possible(ACTIONS_NAME_COST[tag]):
            self.hudmobile_taspasassezdePAgros.show(100, 100)

        else:
            self.actions[tag](event)