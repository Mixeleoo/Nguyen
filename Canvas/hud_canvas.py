
from parameter import *
from Canvas.base_canvas import BaseCanvas

class HUDCanvas(BaseCanvas):
    def __init__(self, master=None, cnf=None, **kw):
        # C'est PyCharm qui me dit de mettre ça au lieu de cnf={} directement dans les arguments donc...
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        from Canvas.HUDs.HUDStandard.hud_build_city import HUDBuildCity
        from Canvas.HUDs.HUDStandard.hud_actions import HUDActions
        from Canvas.HUDs.HUDStandard.hud_history import HUDHistory
        from Canvas.HUDs.HUDStandard.hud_build_church import HUDBuildChurch
        from Canvas.HUDs.HUDStandard.hud_event import HUDEvent
        from Canvas.HUDs.HUDStandard.hud_top_side import HUDTopSide

        from Canvas.HUDs.HUDMobile.hudmobile_village_info import HUDMobileVillageInfo
        from Canvas.HUDs.HUDMobile.hudmobile_yaunvillagegros import HUDMobileYaUnVillageGros
        from Canvas.HUDs.HUDMobile.hudmobile_choose_type_villager import HUDChooseTypeVillager
        from Canvas.HUDs.HUDMobile.hudmobile_choose_taxes import HUDMobileChooseTaxes
        from Canvas.HUDs.HUDMobile.HUDRadionbuttonInPage.hudmobile_choose_village import HUDChooseVillage
        from Canvas.HUDs.HUDMobile.HUDRadionbuttonInPage.hudmobile_choose_noble import HUDChooseNoble

        from Canvas.HUDs.HUDWindow.hudwindow_more_info import HUDWindowMoreInfoSupervisor

        self.to_show_if_cancel = []

        self.hud_actions = HUDActions(self)
        self.hud_history = HUDHistory(self)
        self.hud_build_city = HUDBuildCity(self)
        self.hud_build_church = HUDBuildChurch(self)
        self.hud_event = HUDEvent(self)
        self.hud_top_side = HUDTopSide(self)

        self.hudmobile_village_info = HUDMobileVillageInfo(self)
        self.hudmobile_yavillagegros = HUDMobileYaUnVillageGros(self)
        self.hudmobile_choose_type_villager = HUDChooseTypeVillager(self)
        self.hudmobile_choose_taxes = HUDMobileChooseTaxes(self)
        self.hudmobile_choose_village = HUDChooseVillage(self)
        self.hudmobile_choose_noble = HUDChooseNoble(self)

        self.hudwindow_more_info_supervisor = HUDWindowMoreInfoSupervisor(self)

    def create_HUDs(self, geometry_width: int, geometry_height: int):

        # HUDs permanants
        self.hud_actions.create(geometry_width, geometry_height)
        self.hud_history.create(geometry_width, geometry_height)
        self.hud_build_city.create(geometry_width, geometry_height)
        self.hud_build_church.create(geometry_width, geometry_height)
        self.hud_event.create(geometry_width, geometry_height)
        self.hud_top_side.create(geometry_width, geometry_height)

        # HUDs mobile
        self.hudmobile_village_info.create()
        self.hudmobile_yavillagegros.create()
        self.hudmobile_choose_type_villager.create()
        self.hudmobile_choose_village.create()
        self.hudmobile_choose_taxes.create()
        self.hudmobile_choose_noble.create()

        for i in range(NB_NOBLE_AU_DEPART):
            self.hudwindow_more_info_supervisor.add()

        self.init_nobles()

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
        # Réafficher les HUDs cachés lorsque le joueur a cliqué sur l'action pour construire un village
        for f in self.to_show_if_cancel:
            f()

        self.to_show_if_cancel = []

    def init_nobles(self):
        # Ajouter un village au joueur
        square_id = self.engine_build_city()
        self.jeu.creer_noble(square_id, prenom_aleatoire())

        nom = nom_aleatoire_village()
        self.hudmobile_choose_village.add_option(nom, square_id)
        self.hudmobile_choose_taxes.add_village(nom, square_id)

        # Ajout des villages aléatoirement
        for noble in range(NB_NOBLE_AU_DEPART):
            square_id = self.engine_build_city()
            prenom = prenom_aleatoire()

            # + 1 Pour ne pas compter le premier noble (qui est le joueur)
            self.hudmobile_choose_noble.add_option(prenom, noble + 1)
            self.jeu.creer_noble(square_id, prenom)
