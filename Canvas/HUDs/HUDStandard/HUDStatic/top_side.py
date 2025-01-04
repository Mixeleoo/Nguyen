
import tkinter as tk

from ..HUDStaticABC import HUDStaticABC
from Canvas.Widget.StringVar import StringVar
from parameter import *


class TopSide(HUDStaticABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.texts: list[StringVar] = []

        # PYREVERSE
        #self.texts = StringVar()

        self.rect_ids: list[int] = []

    @property
    def arrival_pos_show(self) -> Position: return Position(0, 0)
    @property
    def curr_show_pos(self) -> Position: return Position(0, 0)
    @property
    def arrival_pos_hide(self) -> Position: return Position(0, 0)
    @property
    def curr_hide_pos(self) -> Position: return Position(0, 0)

    def create(self, geometry_width: int, geometry_height: int) -> None:

        texts = self._get_texts()

        for text in texts:
            rect_id = self.canvas.create_rectangle(
                0, 0, 0, 0,
                tags=set_tags(hud_tag=self.tag),
                fill=FILL_ACTION_BOX
            )

            t = StringVar(self.canvas)
            t.id = self.canvas.create_text(
                0, 0,
                text=text, tags=set_tags(hud_tag=self.tag), fill=FILL_TEXT
            )

            self.rect_ids.append(rect_id)
            self.texts.append(t)

    def get_abscissa_square(self, square_index: int):
        length_square = self.canvas.winfo_width() // len(self.texts)
        return length_square * square_index + length_square // 1.5

    def replace(self, event: tk.Event) -> None:
        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = event.width
        y1_cadre = HEIGHT_HUD_TOP_SIDE

        x = x0_cadre
        xstep = x1_cadre // len(self.texts)
        for i in range(len(self.rect_ids)):
            nx = x + xstep
            self.canvas.coords(
                self.rect_ids[i],
                x,
                y0_cadre,
                nx,
                y1_cadre
            )

            self.canvas.coords(
                self.texts[i].id,
                (x + nx) // 2, (y0_cadre + y1_cadre) // 2
            )

            x = int(nx)

    def _get_texts(self):
        if self.canvas.jeu.nb_joueurs > 0:
            joueur = self.canvas.jeu.get_joueur(0)

            return [
                f"PA {joueur.pa}",
                f"💰 {joueur.argent}",
                f"🍴 {joueur.ressources}",
                f"😊 {joueur.bonheur_general}",
                f"🧑🏻‍🌾 {joueur.population}",
                f"⚔🗡 {joueur.effectif_armee}",
                f"💥 {self.canvas.jeu.nb_joueurs - 1} / {self.canvas.nb_nobles}"
            ]

        else:
            return ["", "", "", "", "", "", ""]

    def update(self):
        texts = self._get_texts()

        for i in range(len(texts)):
            self.texts[i].set(texts[i])

    def _show_animation(self) -> None:
        pass

    def _hide_animation(self) -> None:
        pass