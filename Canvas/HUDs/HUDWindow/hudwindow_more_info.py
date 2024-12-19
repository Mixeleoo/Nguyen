
from Territoire.village import Village
from .base import HUDWindowABC
from Canvas.hud_canvas import HUDCanvas

# TODO Léo: Dans la fenêtre plus d'info, permettre d'afficher tous les villageois sous forme de scrollbar (automatiser la scrollbar du coup flemme de la refaire), et si on clique sur un villageois afficher ses détails dans la même fenêtre + un bouton pour revenir en arrière.

class HUDMoreInfoWindow(HUDWindowABC):
    def __init__(self, canvas: HUDCanvas, village: Village):
        super().__init__(canvas)

        self._village = village

    @property
    def title(self):
        return self._village.nom

    @property
    def id(self) -> int:
        return self._village.id

    def replace(self, *args) -> None:
        t = f"🧑🏻‍🌾 {self._village.population}/80\n"\
            f"🍴 {self._village.ressources}\n"\
            f"😊 {self._village.bonheur_general}\n(vachement plus d'info ici n'est ce pas)"

        self._text.set(t)

class HUDWindowSupervisor:
    def __init__(self, canvas: HUDCanvas):
        self.canvas = canvas

        self.windows: dict[str: HUDWindowABC] = {}

    def add_more_info(self, village: Village):
        w = HUDMoreInfoWindow(self.canvas, village)

        self.windows["p" + w.tag] = w
        self.windows[w.tag] = self.windows["p" + w.tag]
        self.windows["p" + w.tag].create()

    def get_active_window(self, tag: str) -> HUDWindowABC: return self.windows[tag]

    def show_window(self, tag: str): self.get_active_window(tag).show()
