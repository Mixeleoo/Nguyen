
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

        self.basic_mode_tag_foc[PLAINE_TAG] = dummy
        self.basic_mode_tag_foc[VILLAGE_TAG] = self.hudmobile_village_info.show
        self.basic_mode_tag_foc[BUILD_CITY] = self.hud_build_city.choose_plain_to_build
        self.basic_mode_tag_foc[BUILD_CHURCH] = self.hud_build_church.choose_village_to_build
        self.basic_mode_tag_foc[CLOSE_MORE_INFO_WINDOW] = lambda *args: self.hudwindow_more_info_supervisor.get_active_window().hide()
        self.basic_mode_tag_foc[PIN_MORE_INFO_WINDOW] = lambda *args: self.hudwindow_more_info_supervisor.get_active_window().pin()
        self.basic_mode_tag_foc[INFO_EVENT_TAG] = dummy
        self.basic_mode_tag_foc[PAYSAN_OR_ARTISAN_TAG] = self.hud_paysan_or_artisan.show
        self.basic_mode_tag_foc[NOTHING_TAG] = dummy

        self.build_city_mode_tag_foc[PLAINE_TAG] = self.hud_build_city.build_city_on_plain
        self.build_city_mode_tag_foc[VILLAGE_TAG] = lambda e: print("Y'a déjà un village ici ?")

        self.build_church_mode_tag_foc[PLAINE_TAG] = dummy
        self.build_church_mode_tag_foc[VILLAGE_TAG] = self.hud_build_church.build_church_on_village
