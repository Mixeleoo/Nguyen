
import tkinter as tk

from parameter import *
from Canvas.HUD.HUDMobileABC import HUDMobileABC

class HUDMobileVillageInfo(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.more_info_button_id = 0

    @property
    def tag(self):
        return TEMP_VILLAGE_INFO_TAG

    def create(self):

        largeur = 120

        last_item_id = 0

        # Affichage du rectangle
        for categorie_i in range(len(ACTION_FOR_VILLAGE)):
            categorie_i_dim = categorie_i * 40

            last_item_id = self.canvas.create_text_in_rectangle(
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

        self.more_info_button_id = last_item_id

    def replace(self, event: tk.Event) -> None:

        dx = event.x - self.canvas.coords(self.canvas.find_withtag(TEMP_VILLAGE_INFO_TAG)[0])[0]
        dy = event.y - self.canvas.coords(self.canvas.find_withtag(TEMP_VILLAGE_INFO_TAG)[0])[1]

        # Si le rectangle dépasse la longueur de la fenêtre par le bas, l'afficher par le haut
        if event.y + 160 > self.canvas.master.winfo_height():
            dy = event.y - self.canvas.coords(self.canvas.find_withtag(TEMP_VILLAGE_INFO_TAG)[-2])[3]

        # Si le rectangle dépasse la longueur de la fenêtre par le bas, l'afficher par le haut
        if event.x + 100 > self.canvas.master.winfo_width():
            dx = event.x - self.canvas.coords(self.canvas.find_withtag(TEMP_VILLAGE_INFO_TAG)[0])[2]

        self.canvas.move(TEMP_VILLAGE_INFO_TAG, dx, dy)

        active_village_tags = self.canvas.gettags("active")

        tags = list(self.canvas.gettags(self.more_info_button_id))
        tags[GROUP_TAG_INDEX] = active_village_tags[GROUP_TAG_INDEX]

        self.canvas.itemconfigure(self.more_info_button_id, tags=tags)

        for item_id in self.canvas.find_withtag(TEMP_VILLAGE_INFO_TAG):
            self.canvas.itemconfigure(item_id, state="normal")
