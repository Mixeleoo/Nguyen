
import tkinter as tk

from .base import HUDMobileABC
from parameter import *
from ...Widget.StringVar import StringVar


class VillageInfo(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.more_info_button_id = 0
        self.texts: list[StringVar] = []

    @property
    def tag(self):
        return TEMP_VILLAGE_INFO_TAG

    def create(self):

        width = 120

        y = 0
        ystep = 40
        for i in range(3):
            ny = y + ystep
            self.canvas.create_rectangle(
                0,
                y,
                width,
                ny,
                tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
                fill=FILL_ACTION_BOX,
                state="hidden"
            )

            t = StringVar(self.canvas)
            t.id = self.canvas.create_text(
                width // 2, (y + ny) // 2,
                text="",
                tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG),
                fill=FILL_TEXT,
                state="hidden"
            )

            self.texts.append(t)

            y = int(ny)

        self.more_info_button_id = self.canvas.add_button(
            hud_tag=self.tag,
            trigger_name=MORE_INFO_TAG,
            func_triggered=lambda *args: self.canvas.hudwindow_more_info_supervisor.get_active_window().show(),
        ).draw(
            x0=0,
            y0=y,
            x1=width,
            y1=y + ystep,
            text="Plus d'info",
            state="hidden",
            is_temp=True
        )

    def replace(self, event: tk.Event) -> None:

        dx = event.x - self.canvas.coords(self.canvas.find_withtag(self.tag)[0])[0]
        dy = event.y - self.canvas.coords(self.canvas.find_withtag(self.tag)[0])[1]

        # Si le rectangle dépasse la longueur de la fenêtre par le bas, l'afficher par le haut
        if event.y + 160 > self.canvas.master.winfo_height():
            dy = event.y - self.canvas.coords(self.canvas.find_withtag(self.tag)[-2])[3]

        # Si le rectangle dépasse la longueur de la fenêtre par le bas, l'afficher par le haut
        if event.x + 100 > self.canvas.master.winfo_width():
            dx = event.x - self.canvas.coords(self.canvas.find_withtag(self.tag)[0])[2]

        self.canvas.move(self.tag, dx, dy)

        active_village_id = self.canvas.find_withtag("active")[0]
        self._refresh_text(active_village_id)

        active_village_tags = self.canvas.gettags(active_village_id)

        tags = list(self.canvas.gettags(self.more_info_button_id))
        tags[GROUP_TAG_INDEX] = active_village_tags[GROUP_TAG_INDEX]

        self.canvas.itemconfigure(self.more_info_button_id, tags=tags)

    def _refresh_text(self, village_id: int) -> None:
        texts = self._get_texts(village_id)
        for i in range(len(texts)):
            self.texts[i].set(texts[i])

    def _get_texts(self, village_id: int) -> list[str]:
        """
        Méthode retournant les infos du village clické si le village appartient au joueur sinon retourne Inconnu
        """
        village = self.canvas.jeu.get_village(village_id)
        if village is not None:
            return [
                f"🧑🏻‍🌾 {village.population}",
                f"🍴 {village.ressources}",
                f"😊 {village.bonheur_general}"
            ]

        else: return [
            "Inconnu", "Inconnu", "Inconnu"
        ]
