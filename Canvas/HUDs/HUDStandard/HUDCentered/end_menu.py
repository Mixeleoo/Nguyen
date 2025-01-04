
import tkinter as tk

from Canvas.HUDs.HUDStandard.HUDCenteredABC import HUDCenteredABC
from Canvas.Widget.Button import Button
from Canvas.Widget.StringVar import StringVar
from parameter import FILL_TEXT, FILL_ACTION_BOX, set_tags, TEMP_TAG

class EndMenu(HUDCenteredABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self._text_reason = StringVar(self.canvas)
        self._background_id = 0

    def create(self, geometry_width, geometry_height):

        center_x = geometry_width // 2
        center_y = geometry_height // 2

        self._background_id = self.canvas.create_rectangle(
            0, 0, geometry_width, geometry_height,
            fill=FILL_ACTION_BOX,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,)
        )

        custom_font = tk.font.nametofont("TkDefaultFont").copy()
        custom_font.configure(size=18)

        self._text_reason.id = self.canvas.create_text(
            center_x, center_y - 200,
            tags=set_tags(hud_tag=self.tag),
            fill=FILL_TEXT,
            font=custom_font,
            justify="center"
        )

        Button(
            self.canvas,
            self.tag,
            "SHOW_START_MENU",
            self.canvas.restart
        ).draw(
            center_x - 70,
            center_y - 60,
            center_x + 70,
            center_y - 20,
            text="Recommencer",
            is_temp=True,
            justify="center"
        )

        Button(
            self.canvas,
            self.tag,
            "QUIT",
            lambda e: self.canvas.quit()
        ).draw(
            center_x - 70,
            center_y + 20,
            center_x + 70,
            center_y + 60,
            text="Quitter le jeu",
            is_temp=True,
            justify="center"
        )

    def replace(self, *args) -> None:
        super().replace(*args)
        self.canvas.coords(self._background_id, 0, 0, self.canvas.master.winfo_width(), self.canvas.master.winfo_height())

    def show(self, *args) -> None:
        self.canvas.tag_raise(self.tag)
        super().show(*args)

    def update(self, *args):
        pass

    def win(self, reason: str):
        """
        Méthode lancée pour afficher le menu de fin
        :param reason: Phrase affichée pour expliquer la raison de la fin de partie
        """
        self.canvas.tag_raise(self.tag)
        self._text_reason.set(reason)
        self.show()

    def lose(self, reason: str):
        """
        Méthode lancée pour afficher le menu de fin
        :param reason: Phrase affichée pour expliquer la raison de la fin de partie
        """
        self.canvas.tag_raise(self.tag)
        self._text_reason.set(reason)
        self.show()
