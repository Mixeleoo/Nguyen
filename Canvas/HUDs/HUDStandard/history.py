
import tkinter as tk
from typing import Literal

from .base import HUDABC
from parameter import *

class History(HUDABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.rect_hiding_top_text_id = 0
        self.rect_hiding_bottom_text_id = 0
        self.last_text_id = 0

        self.state: Literal["normal", "hidden"] = "normal"
        self.hide_button_id = 0
        self.background_rect_id = 0
        self.thumb_id = 0

        self.longueur_texte = 0

    @property
    def tag(self):
        return HUD_RIGHT_SIDE

    @property
    def arrival_pos_show(self) -> Position: return Position(self.canvas.master.winfo_width() - 15, 0)
    @property
    def curr_show_pos(self) -> Position: return Position(self.canvas.coords(self.background_rect_id)[2], 0)
    @property
    def arrival_pos_hide(self) -> Position: return Position(self.canvas.master.winfo_width() - 5, 0)
    @property
    def curr_hide_pos(self) -> Position: return Position(self.canvas.coords(SHOW_OR_HIDE_HISTORY_TAG)[2], 0)

    def create(self, geometry_width: int, geometry_height: int):

        pady_from_top = 5
        # Gros rectangle contenant l'historique
        height = geometry_height - HEIGHT_BOTTOM_HUD - pady_from_top - 70  # valeur qui ne bouge pas en fonction de la taille de la fenêtre

        x1_cadre = geometry_width - pady_from_top
        x0_cadre = x1_cadre - WIDTH_HISTORY_HUD
        y0_cadre = PADY_BUILD_CITY_HUD
        y1_cadre = y0_cadre + height

        # Rectangle de l'historique
        self.background_rect_id = self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre,
            fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag)
        )

        # Rectangle pour ranger l'historique
        self.hide_button_id = self.canvas.add_button(
            hud_tag=self.tag,
            trigger_name=SHOW_OR_HIDE_HISTORY_TAG,
            func_triggered=self.show_or_hide
        ).draw(
            x0=x0_cadre - 20,
            y0=y1_cadre - 20,
            x1=x0_cadre - 5,
            y1=y1_cadre - 5,
            text="►"
        )

        # Scrollbar
        self.thumb_id = self.canvas.create_rectangle(
            geometry_width - 5 - 15,
            0,
            geometry_width - 5 - 5,
            0,
            fill=FILL_ACTION_BOX, tags=set_tags(DRAGGABLE_TAG, drag_tag=SCROLLBAR_TAG, hud_tag=self.tag)
        )

        self.canvas.tag_fod[SCROLLBAR_TAG] = self.on_drag_scrollbar

        self.add_text("Début de la partie !")
        for i in range(60):
            self.add_text(f"slt je suis le n°{('0' + str(i)) if i < 10 else i}")


        # to_hide_text_rectangle
        self.rect_hiding_top_text_id = self.canvas.create_rectangle(
            x0_cadre + 1,
            y0_cadre + 1,
            x1_cadre,
            y0_cadre + 20,
            fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag), width=0
        )

        self.rect_hiding_bottom_text_id = self.canvas.create_rectangle(
            x0_cadre + 1,
            y1_cadre - 20,
            x1_cadre,
            y1_cadre,
            fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag), width=0
        )

    def replace(self, event: tk.Event):
        """
        Replacer l'HUDs du bas:
        - mouvement sur x : L'ensemble reste à gauche de l'écran.
        - mouvement sur y : L'ensemble reste en haut de la fenêtre et
            il faut faire un homotéthie de l'historique en fonction de l'agrandissement de la fenêtre
        """
        self.canvas.move(
            self.tag,
            event.width - self.canvas.master.previous_geometry[0],
            PADY_BUILD_CITY_HUD - self.canvas.coords(self.canvas.find_withtag(self.rect_hiding_top_text_id)[0])[1]
        )

    def bhide(self):
        """
        La phase before hide, qui consiste à changer l'état du HUDs en "hidden" et lancer l'animation
        """
        self.state = "hidden"
        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.hide_button_id], text="◄")
        self.hide_animation()

    def bshow(self):
        """
        La phase before show, qui consiste à changer l'état du HUDs en "normal" et lancer l'animation
        """
        self.state = "normal"
        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.hide_button_id], text="►")
        self.show_animation()

    def show_or_hide(self, e=None):
        if self.state == "normal":
            self.bhide()

        else:
            self.bshow()

    def add_text(self, text: str) -> None:
        """
        Méthode qui ajoute du texte à l'historique.
        Elle coupera le texte pour qu'il rentre en largeur dans l'historique.
        Elle ajoutera sa taille en hauteur à la longueur totale des textes dans l'historique.
        Elle refera descendre l'historique à sa hauteur pour que le joueur voie quand il y a du nouveau.
        Elle ajoutera le nouveau texte au groupe en lui ajoutant le tag HISTORY_TEXT.
        Elle refera calculer la nouvelle taille du thumb de la scrollbar.
        """

        coords = self.canvas.coords(self.background_rect_id)

        # On doit savoir combien de fois il faut séparer le texte de \n pour qu'il rentre dans l'historique
        fractions = 1
        length = get_width_text(text)
        while length / fractions > WIDTH_HISTORY_HUD:
            fractions += 1

        text = separer_chaine_sans_couper(text, fractions)
        tags = list(set_tags(hud_tag=self.tag) + (TEXT_TAG,))

        # On ancre le texte au sud donc on met ses coordonnées en bas du rectangle
        # On ancre le texte à l'ouest donc on met ses coordonnées à gauche du rectangle
        text_id = self.canvas.create_text(
            coords[0] + 15, coords[3] - 20,
            text=text,
            tags=tags,
            anchor="sw",
            fill=FILL_TEXT
        )

        bbox = self.canvas.bbox(text_id)
        text_height = bbox[3] - bbox[1]
        self.longueur_texte += text_height

        # On simule la descente de la scrollbar tout en bas
        if self.last_text_id:
            self.drag_history_text(coords[3] - 20 - text_height - self.canvas.coords(self.last_text_id)[1])
            self.canvas.move(self.thumb_id, 0, coords[3] - self.canvas.coords(self.thumb_id)[3])

        # Dès que l'historique a été bien remonté pour que les textes ne se cheuvauchent pas,
        # On peut grouper le nouveau texte avec ses compatriotes.
        tags[GROUP_TAG_INDEX] = HISTORY_TEXT
        self.canvas.itemconfigure(text_id, tags=tags)
        self.last_text_id = text_id

        # On met bien les rectangles cachants le texte au-dessus d'eux
        self.canvas.tag_raise(self.rect_hiding_top_text_id, HISTORY_TEXT)
        self.canvas.tag_raise(self.rect_hiding_bottom_text_id, HISTORY_TEXT)

        # Après avoir mis à jour la longueur du texte, on met à jour la taille de lu thumb de la scrollbar
        self.resize_thumb()

        # On référence le texte vers le rectangle en dessous (pour le drag du texte)
        self.canvas.text_id_in_rectangle_id[text_id] = self.background_rect_id

    def resize_thumb(self):
        coords = self.canvas.coords(self.background_rect_id)
        height = coords[3] - coords[1]

        longueur_viewport = height - 50
        taille_scrollbar = height - 50
        # (longueur_viewport / longueur_contenu) * taille_scrollbar
        longueur_thumb = (longueur_viewport / self.longueur_texte) * taille_scrollbar

        # On limite la taille du thumb de la scrollbar quand même
        longueur_thumb = longueur_thumb if longueur_thumb > 20 else 20

        coords_thumb = self.canvas.coords(self.thumb_id)
        self.canvas.coords(self.thumb_id, coords_thumb[0], coords[3] - longueur_thumb - 25, coords_thumb[2], coords[3] - 25)

    def drag_history_text(self, dy: int | float):
        self.canvas.move(HISTORY_TEXT, 0, dy)
        self.hide_exceeding_text()

    def hide_exceeding_text(self):
        text_history_ids = self.canvas.find_withtag(HISTORY_TEXT)
        i = 0

        # Tous les textes en haut du rectangle deviennent hidden
        while i < len(text_history_ids) and self.canvas.coords(text_history_ids[i])[1] < self.canvas.coords(self.background_rect_id)[1] + 20:
            self.canvas.itemconfigure(text_history_ids[i], state="hidden")
            i += 1

        # Ceux au milieu, on les laisse
        while i < len(text_history_ids) and self.canvas.coords(text_history_ids[i])[1] < self.canvas.coords(self.background_rect_id)[3]:
            self.canvas.itemconfigure(text_history_ids[i], state="normal")
            i += 1

        # Ceux en bas du rectangle deviennent hidden
        while i < len(text_history_ids):
            self.canvas.itemconfigure(text_history_ids[i], state="hidden")
            i += 1

    def on_drag_scrollbar(self, event: tk.Event):

        dy = event.y - self.canvas.mouse_coor[1]

        if self.canvas.coords(self.thumb_id)[1] + dy < self.canvas.coords(self.background_rect_id)[1] + 25 or \
            self.canvas.coords(self.thumb_id)[3] + dy > self.canvas.coords(self.background_rect_id)[3] - 25:
            dy = 0

        # Déplace tous les carrés avec le tag "square"
        self.canvas.move("active", 0, dy)

        coords = self.canvas.coords(self.background_rect_id)
        height = coords[3] - coords[1]

        longueur_viewport = height - 50

        # distance_defilée = fraction défilée * taille totale du contenu
        # fraction defilée = distance effectuee / taille de la viewport
        distance_defilee = (dy / longueur_viewport) * self.longueur_texte
        self.drag_history_text(-distance_defilee)
