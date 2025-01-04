
import tkinter as tk

from .base import HUDStandardABC
from parameter import *
from ...Widget.Button import Button
from ...Widget.StringVar import StringVar


class AllyVillageInfo(HUDStandardABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.more_info_button_id = 0
        self.texts: list[StringVar] = []

    def create(self):

        width = 120

        y = 0
        ystep = 40
        for i in range(3):
            ny = y + ystep
            rect_id = self.canvas.create_rectangle(
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

            self.canvas.text_id_in_rectangle_id[t.id] = rect_id

            self.texts.append(t)

            y = int(ny)

        self.more_info_button_id = Button(
            self.canvas,
            hud_tag=self.tag
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
        if event.x + 120 > self.canvas.master.winfo_width():
            dx = event.x - self.canvas.coords(self.canvas.find_withtag(self.tag)[0])[2]

        # Déplacement de l'HUD là où il a été cliqué
        self.canvas.move(self.tag, dx, dy)

        # Récupération de l'id du carré du village qui a été cliqué
        active_village_id = self.canvas.find_withtag("active")[0]

        # Mise à jour du texte de l'HUD en fonction des infos du village.
        self._refresh_text(active_village_id)

        # Le bouton reçoit le tag OPEN_WINDOW_TAG + l'identifiant de la fenêtre dans son emplacement "TRIGGER_TAG"
        tags = list(self.canvas.gettags(self.more_info_button_id))
        tags[TRIGGER_TAG_INDEX] = OPEN_WINDOW_TAG + str(active_village_id)

        self.canvas.itemconfigure(self.more_info_button_id, tags=tags)

    def _refresh_text(self, village_id: int) -> None:
        texts = self._get_texts(village_id)
        for i in range(len(texts)):
            self.texts[i].set(texts[i])

    def _get_texts(self, village_id: int) -> list[str]:
        """
        Méthode retournant les infos du village clické
        """
        village = self.canvas.jeu.joueur_actuel.get_village_allie(village_id)
        return [
            f"🧑🏻‍🌾 {village.population}/{village.population_max}",
            f"🍴 {village.ressources}",
            f"😊 {village.bonheur_general}"
        ]
