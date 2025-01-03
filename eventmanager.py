
from Canvas.hud_canvas import HUDCanvas
from jeu import Jeu, EventInfo
from parameter import couleurs, PLAINE_TAG, MAP_TAG, set_tags


class EventManager:
    def __init__(self, jeu: Jeu, canvas: HUDCanvas):
        self.jeu = jeu
        self.canvas = canvas

        # Registre des événements
        self.events = {
            "Incendie": self.event_incendie,
            "Vassalisation": self.event_vassalisation,
        }

    def handle_event(self):
        """
        Gère les événements pré-tour du joueur.
        """
        eventinfo = self.jeu.evenement()

        # Affiche les informations de l'événement
        self.canvas.hud_event.set_text(eventinfo.type)
        self.canvas.hud_event.show_animation()

        # Exécute l'événement ou un handler par défaut
        return self.events.get(eventinfo.type, self.event_default)(eventinfo)

    def event_incendie(self, eventinfo: EventInfo) -> bool:
        if not len(self.jeu.joueur_actuel.dico_villages):
            self.canvas.lose("Un incendie a ravagé votre dernier village.\nVous avez perdu.")
            return False

        # Transforme le village en plaine
        self.canvas.itemconfigure(eventinfo.village_incendie.id, fill=couleurs[PLAINE_TAG]())
        self.canvas.itemconfigure(
            eventinfo.village_incendie.id, tags=set_tags(MAP_TAG, PLAINE_TAG, MAP_TAG)
        )
        self.canvas.hudmobile_choose_taxes.remove_village(eventinfo.village_incendie.id)
        self.canvas.hudmobile_more_info_event.refresh_text(eventinfo.village_incendie.nom)
        return True

    def event_vassalisation(self, eventinfo: EventInfo) -> bool:
        self.canvas.hudcentered_accept_vassal.show(eventinfo.noble_vassalise)
        self.canvas.hudmobile_more_info_event.refresh_text(eventinfo.descriptif)
        return True

    def event_default(self, eventinfo: EventInfo) -> bool:
        self.canvas.hudmobile_more_info_event.refresh_text(eventinfo.descriptif)
        self.canvas.update_hudtop()
        return True
