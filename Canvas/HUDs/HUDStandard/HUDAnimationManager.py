
from abc import ABC, abstractmethod
from math import ceil

from Canvas.hud_canvas import HUDCanvas
from parameter import *

class HUDAnimationManager(ABC):
    def __init__(self, canvas: HUDCanvas):
        self.canvas = canvas
        self.is_showing = False  # Indique si l'animation "show" est en cours
        self.is_hiding = False  # Indique si l'animation "hide" est en cours
        self.after_id = None    # Référence pour annuler un after en cours

    @property
    @abstractmethod
    def tag(self):
        """
        Méthode pour retourner le tag de l'HUD
        """
        pass

    @property
    @abstractmethod
    def curr_show_pos(self) -> Position:
        """
        Point de départ en abscisses de l'animation.
        """
        pass

    @property
    @abstractmethod
    def curr_hide_pos(self) -> Position:
        """
        Point de départ en abscisses de l'animation.
        """
        pass

    @property
    @abstractmethod
    def arrival_pos_show(self) -> Position:
        """
        Point de départ en abscisses de l'animation.
        """
        pass

    @property
    @abstractmethod
    def arrival_pos_hide(self) -> Position:
        """
        Point de départ en abscisses de l'animation.
        """
        pass

    def show_animation(self):
        """
        Lance l'animation pour afficher le HUD.
        """
        if self.is_showing:
            return  # L'animation "show" est déjà en cours, on ignore

        # Si "hide" est en cours, on l'interrompt
        if self.is_hiding:
            self.cancel_animation()
            self.is_hiding = False

        self.is_showing = True
        self._show_step()        # Commencer l'animation

    def _show_step(self):
        """
        Étape individuelle de l'animation 'show'.
        """
        self.canvas.move(
            self.tag,
            ceil((self.arrival_pos_show.x - self.curr_show_pos.x) / 10),
            ceil((self.arrival_pos_show.y - self.curr_show_pos.y) / 10)
        )

        if self.is_hiding:  # Vérifier si "hide" a été déclenchée
            self.cancel_animation()
            return

        if self.curr_show_pos.x == self.arrival_pos_show.x and self.curr_show_pos.y == self.arrival_pos_show.y:  # Vérifier si l'animation est terminée
            self.is_showing = False
        else:
            self.after_id = self.canvas.after(DELTA_MS_ANIMATION, self._show_step)  # Appeler la prochaine étape

    def hide_animation(self):
        """Lance l'animation pour cacher le HUD."""
        if self.is_hiding:
            return  # L'animation "hide" est déjà en cours, on ignore

        # Si "show" est en cours, on l'interrompt
        if self.is_showing:
            self.cancel_animation()
            self.is_showing = False

        self.is_hiding = True
        self._hide_step()        # Commencer l'animation

    def _hide_step(self):
        """Étape individuelle de l'animation 'hide'."""
        self.canvas.move(
            self.tag,
            ceil((self.arrival_pos_hide.x - self.curr_hide_pos.x) / 10),
            ceil((self.arrival_pos_hide.y - self.curr_hide_pos.y) / 10)
        )

        if self.is_showing:  # Vérifier si "show" a été déclenchée
            self.cancel_animation()
            return

        if self.curr_hide_pos.x == self.arrival_pos_hide.x and self.curr_hide_pos.y == self.arrival_pos_hide.y:  # Vérifier si l'animation est terminée
            self.is_hiding = False
        else:
            self.after_id = self.canvas.after(DELTA_MS_ANIMATION, self._hide_step)  # Appeler la prochaine étape

    def cancel_animation(self):
        """Annule une animation en cours."""
        if self.after_id is not None:
            self.canvas.after_cancel(self.after_id)  # Annuler le `after`
            self.after_id = None
        self.is_showing = False
        self.is_hiding = False
