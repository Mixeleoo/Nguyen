
import tkinter as tk

from .base import HUDMobileABC
from parameter import *

class VillageInfo(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.more_info_button_id = 0

    @property
    def tag(self):
        return TEMP_VILLAGE_INFO_TAG

    def create(self):

        largeur = 120

        self.canvas.create_text_in_rectangle(
            x0=0,
            y0=0,
            x1=largeur,
            y1=40,
            fill=FILL_ACTION_BOX,
            text="50 Villageois",
            rectangle_tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG,),
            state="hidden"
        )

        self.canvas.create_text_in_rectangle(
            x0=0,
            y0=40,
            x1=largeur,
            y1=80,
            fill=FILL_ACTION_BOX,
            text="50 Ressources",
            rectangle_tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG,),
            state="hidden"
        )

        self.canvas.create_text_in_rectangle(
            x0=0,
            y0=80,
            x1=largeur,
            y1=120,
            fill=FILL_ACTION_BOX,
            text="2 / 10 Bonheur",
            rectangle_tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG,),
            state="hidden"
        )

        self.more_info_button_id = self.canvas.add_button(
            hud_tag=self.tag,
            trigger_name=MORE_INFO_TAG,
            func_triggered=lambda *args: self.canvas.hudwindow_more_info_supervisor.get_active_window().show(),
        ).draw(
            x0=0,
            y0=120,
            x1=largeur,
            y1=160,
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

        active_village_tags = self.canvas.gettags("active")

        tags = list(self.canvas.gettags(self.more_info_button_id))
        tags[GROUP_TAG_INDEX] = active_village_tags[GROUP_TAG_INDEX]

        self.canvas.itemconfigure(self.more_info_button_id, tags=tags)
