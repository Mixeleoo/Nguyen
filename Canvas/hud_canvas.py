
from parameter import *
from Canvas.base_canvas import BaseCanvas

class HUDCanvas(BaseCanvas):
    def __init__(self, master=None, cnf=None, **kw):
        # C'est PyCharm qui me dit de mettre ça au lieu de cnf={} directement dans les arguments donc...
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        from Canvas.HUD.hud_build_city import HUDBuildCity
        from Canvas.HUD.hud_paysan_or_artisan import HUDPaysanOrArtisan
        from Canvas.HUD.hud_actions import HUDActions
        from Canvas.HUD.hud_history import HUDHistory
        from Canvas.HUD.hud_build_church import HUDBuildChurch
        from Canvas.HUD.hud_event import HUDEvent
        from Canvas.HUD.hudmobile_village_info import HUDMobileVillageInfo
        from Canvas.HUD.hudmobile_yaunvillagegros import HUDMobileYaUnVillageGros
        from Canvas.HUD.hud_choose_village import HUDChooseVillage

        from Canvas.HUD.hudwindow_more_info import HUDWindowMoreInfoSupervisor

        self.to_show_if_cancel = []

        self.hud_actions = HUDActions(self)
        self.hud_history = HUDHistory(self)
        self.hud_build_city = HUDBuildCity(self)
        self.hud_build_church = HUDBuildChurch(self)
        self.hud_event = HUDEvent(self)
        self.hudmobile_village_info = HUDMobileVillageInfo(self)
        self.hudmobile_yavillagegros = HUDMobileYaUnVillageGros(self)
        self.hud_choose_village = HUDChooseVillage(self)
        self.hud_paysan_or_artisan = HUDPaysanOrArtisan(self)

        self.hudwindow_more_info_supervisor = HUDWindowMoreInfoSupervisor(self)

    def create_HUDs(self, geometry_width: int, geometry_height: int):

        # HUD permanants
        self.hud_actions.create(geometry_width, geometry_height)
        self.hud_history.create(geometry_width, geometry_height)
        self.hud_build_city.create(geometry_width, geometry_height)
        self.hud_build_church.create(geometry_width, geometry_height)
        self.hud_event.create(geometry_width, geometry_height)
        self.hud_paysan_or_artisan.create(geometry_width, geometry_height)
        self.hud_choose_village.create(geometry_width, geometry_height)

        # HUD temporaire
        self.hudmobile_village_info.create()
        self.hudmobile_yavillagegros.create()
        for i in range(NB_NOBLE_AU_DEPART):
            self.hudwindow_more_info_supervisor.add()

    def hide_all_permanant_huds(self):
        # On simule un clic sur le bouton qui cache les pages d'actions
        if self.hud_actions.state == "normal":
            self.hud_actions.bhide()
            self.to_show_if_cancel += [self.hud_actions.bshow]

        # On simule un clic sur le bouton qui cache l'historique
        if self.hud_history.state == "normal":
            self.hud_history.bhide()
            self.to_show_if_cancel += [self.hud_history.bshow]

    def show_hidden_permanant_huds(self):
        # Réafficher les HUD cachés lorsque le joueur a cliqué sur l'action pour construire un village
        for f in self.to_show_if_cancel:
            f()

        self.to_show_if_cancel = []


