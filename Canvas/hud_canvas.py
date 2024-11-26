
from Canvas.base_canvas import BaseCanvas
from Canvas.HUD.hud_build_city import HUDBuildCity
from Canvas.HUD.hud_paysan_or_artisan import HUDPaysanOrArtisan
from Canvas.HUD.hud_actions import HUDActions
from Canvas.HUD.hud_history import HUDHistory
from Canvas.HUD.hud_build_church import HUDBuildChurch
from Canvas.HUD.hud_event import HUDEvent
from Canvas.HUD.hudmobile_village_info import HUDMobileVillageInfo
from Canvas.HUD.hudmobile_more_info import HUDMobileMoreInfo
from Canvas.HUD.hudmobile_yaunvillagegros import HUDMobileYaUnVillageGros

class HUDCanvas(BaseCanvas):
    def __init__(self, master=None, cnf=None, **kw):
        # C'est PyCharm qui me dit de mettre ça au lieu de cnf={} directement dans les arguments donc...
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        self.hud_paysan_or_artisan = HUDPaysanOrArtisan(self)
        self.hud_actions = HUDActions(self)
        self.hud_history = HUDHistory(self)
        self.hud_build_city = HUDBuildCity(self)
        self.hud_build_church = HUDBuildChurch(self)
        self.hud_event = HUDEvent(self)
        self.hudmobile_village_info = HUDMobileVillageInfo(self)
        self.hudmobile_more_info = HUDMobileMoreInfo(self)
        self.hudmobile_yavillagegros = HUDMobileYaUnVillageGros(self)

    def create_HUDs(self, geometry_width: int, geometry_height: int):

        # HUD permanants
        self.hud_actions.create(geometry_width, geometry_height)
        self.hud_history.create(geometry_width, geometry_height)
        self.hud_build_city.create(geometry_width, geometry_height)
        self.hud_build_church.create(geometry_width, geometry_height)
        self.hud_event.create(geometry_width, geometry_height)
        self.hud_paysan_or_artisan.create(geometry_width, geometry_height)

        # HUD temporaire
        self.hudmobile_village_info.create()
        self.hudmobile_more_info.create()
        self.hudmobile_yavillagegros.create()


