
import tkinter as tk

from .base import HUDABC
from ...Widget.StringVar import StringVar
from parameter import *


class TopSide(HUDABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.texts: list[StringVar] = []

        # PYREVERSE
        #self.texts = StringVar()

    @property
    def arrival_pos_show(self) -> Position: return Position(0, 0)
    @property
    def curr_show_pos(self) -> Position: return Position(0, 0)
    @property
    def arrival_pos_hide(self) -> Position: return Position(0, 0)
    @property
    def curr_hide_pos(self) -> Position: return Position(0, 0)

    def create(self, geometry_width: int, geometry_height: int) -> None:

        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = geometry_width
        y1_cadre = HEIGHT_HUD_TOP_SIDE

        self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre, fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag)
        )

        texts = self._get_texts()

        x = x0_cadre
        xstep = x1_cadre // len(texts)
        for text in texts:
            nx = x + xstep
            self.canvas.create_rectangle(
                x,
                y0_cadre,
                nx,
                y1_cadre,
                tags=set_tags(hud_tag=self.tag),
                fill=FILL_ACTION_BOX
            )

            t = StringVar(self.canvas)
            t.id = self.canvas.create_text(
                (x + nx) // 2, (y0_cadre + y1_cadre) // 2,
                text=text, tags=set_tags(hud_tag=self.tag), fill=FILL_TEXT
            )

            self.texts.append(t)

            x = int(nx)

    def replace(self, event: tk.Event) -> None:
        pass

    def _get_texts(self):
        if self.canvas.jeu.nb_joueurs > 0:
            joueur = self.canvas.jeu.get_joueur(0)

            return [
                f"PA {joueur.pa}",
                f"💰 {joueur.argent}",
                f"😊 {joueur.bonheur_general}",
                f"🍴 {joueur.ressources}",
                f"🧑🏻‍🌾 {joueur.population}",
                f"⚔🗡 {joueur.effectif_armee}",
                f"💥 {self.canvas.jeu.nb_joueurs - 1} / {NB_NOBLE_AU_DEPART}"
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