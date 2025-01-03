
import tkinter as tk

from .base import HUDStandardABC
from parameter import *
from ...Widget.StringVar import StringVar


class EnemyVillageInfo(HUDStandardABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.more_info_button_id = 0
        self.text = StringVar(self.canvas)
        self._rect_id = 0

    def create(self):

        self._rect_id = self.canvas.create_rectangle(
            0,
            0,
            0,
            60,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            fill=FILL_ACTION_BOX,
            state="hidden"
        )

        self.text.id = self.canvas.create_text(
            0, 60 // 2,
            text="",
            tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG),
            fill=FILL_TEXT,
            state="hidden",
            justify="center"
        )


    def replace(self, event: tk.Event) -> None:

        # Récupération de l'id du carré du village qui a été cliqué
        active_village_id = self.canvas.find_withtag("active")[0]

        # Mise à jour du texte de l'HUD en fonction des infos du village.
        self._refresh_text(active_village_id)

        dx = event.x - self.canvas.coords(self.canvas.find_withtag(self.tag)[0])[0]
        dy = event.y - self.canvas.coords(self.canvas.find_withtag(self.tag)[0])[1]

        # Si le rectangle dépasse la longueur de la fenêtre par le bas, l'afficher par le haut
        if event.y + 60 > self.canvas.master.winfo_height():
            dy = event.y - self.canvas.coords(self.canvas.find_withtag(self.tag)[-2])[3]

        # Si le rectangle dépasse la longueur de la fenêtre par le bas, l'afficher par le haut
        if event.x + 120 > self.canvas.master.winfo_width():
            dx = event.x - self.canvas.coords(self.canvas.find_withtag(self.tag)[0])[2]

        # Déplacement de l'HUD là où il a été cliqué
        self.canvas.move(self.tag, dx, dy)

    def _refresh_text(self, village_id: int) -> None:
        village_joueur = self.canvas.jeu.village_de(village_id)
        self.text.set(f"Village nommé {village_joueur.get_village(village_id).nom}\nAppartenant à {village_joueur.nom}")

        width = get_width_text(self.text.content)
        self.canvas.coords(self._rect_id, 0, 0, width, 60)
        self.canvas.coords(self.text.id, width // 2, 60 // 2)
