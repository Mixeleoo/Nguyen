
import tkinter as tk

from parameter import *
from Canvas.HUD.HUDMobileABC import HUDMobileABC

class HUDMobileVillageInfo(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

    @property
    def tag(self):
        return TEMP_VILLAGE_INFO_TAG

    def create(self):

        largeur = 120

        # Affichage du rectangle
        for categorie_i in range(len(ACTION_FOR_VILLAGE)):
            categorie_i_dim = categorie_i * 40

            self.canvas.create_text_in_rectangle(
                x0=0,
                y0=categorie_i_dim,
                x1=largeur,
                y1=categorie_i_dim + 40,
                fill=FILL_ACTION_BOX,
                text=ACTION_FOR_VILLAGE[categorie_i],
                rectangle_tags=ACTION_ID_FOR_VILLAGE[categorie_i],
                text_tags=ACTION_TEXT_TAG_FOR_VILLAGE[categorie_i],
                state="hidden"
            )

    def replace(self, event: tk.Event) -> None:

        dx = event.x - self.canvas.coords(self.canvas.find_withtag(TEMP_VILLAGE_INFO_TAG)[0])[0]
        dy = event.y - self.canvas.coords(self.canvas.find_withtag(TEMP_VILLAGE_INFO_TAG)[0])[1]

        # Si le rectangle dépasse la longueur de la fenêtre par le bas, l'afficher par le haut
        if event.y + 160 > self.canvas.master.winfo_height():
            print(self.canvas.gettags(self.canvas.find_withtag(TEMP_VILLAGE_INFO_TAG)[-2]))
            dy = event.y - self.canvas.coords(self.canvas.find_withtag(TEMP_VILLAGE_INFO_TAG)[-2])[3]

        # Si le rectangle dépasse la longueur de la fenêtre par le bas, l'afficher par le haut
        if event.x + 100 > self.canvas.master.winfo_width():
            dx = event.x - self.canvas.coords(self.canvas.find_withtag(TEMP_VILLAGE_INFO_TAG)[0])[2]

        self.canvas.move(TEMP_VILLAGE_INFO_TAG, dx, dy)

        for item_id in self.canvas.find_withtag(TEMP_VILLAGE_INFO_TAG):
            self.canvas.itemconfigure(item_id, state="normal")
