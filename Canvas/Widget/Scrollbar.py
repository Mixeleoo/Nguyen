
import tkinter as tk
from typing import Literal

from Canvas.self_made_canvas import SelfMadeCanvas
from parameter import (TEMP_TAG, FILL_ACTION_BOX, set_tags, DRAGGABLE_TAG, SCROLLBAR_TAG, get_width_text,
                       separer_chaine_sans_couper, WIDTH_HISTORY_HUD, FILL_TEXT, GROUP_TAG_INDEX)

class Scrollbar:
    _instance_counter = 0
    _instances = []

    @classmethod
    def all_default(cls):
        for instance in cls._instances:
            instance.default()

    def __init__(self, canvas: SelfMadeCanvas, hud_tag: str, text_group_tag: str):

        self.canvas = canvas
        self.tag = hud_tag
        self._text_group_tag = text_group_tag
        self._index = Scrollbar._instance_counter
        Scrollbar._instance_counter += 1
        Scrollbar._instances.append(self)

        self._rect_hiding_top_text_id = 0
        self._rect_hiding_bottom_text_id = 0
        self._last_text_id = 0
        self._thumb_id = 0

        self._longueur_texte = 0

        # Pour savoir où couper le texte qu'il ne dépasse pas
        self._width_hud = 0

    def default(self):
        self.canvas.delete(self._text_group_tag)
        self._last_text_id = 0
        self._longueur_texte = 0

    def create(self, x0: float, y0: float, x1: float, y1: float, is_temp: bool=False, state: Literal["normal", "hidden"] = "normal"):

        temp = (TEMP_TAG,) if is_temp else ()

        # Scrollbar
        self._thumb_id = self.canvas.create_rectangle(
            x1 - 15,
            0,
            x1 - 5,
            0,
            fill=FILL_ACTION_BOX,
            tags=set_tags(DRAGGABLE_TAG, drag_tag=SCROLLBAR_TAG + str(self._index), hud_tag=self.tag) + temp,
            state=state
        )

        self.canvas.tag_fod[SCROLLBAR_TAG + str(self._index)] = self.on_drag_scrollbar

        # to_hide_text_rectangle
        self._rect_hiding_top_text_id = self.canvas.create_rectangle(
            x0 + 1,
            y0 + 1,
            x1,
            y0 + 20,
            fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag) + temp,
            width=0,
            state=state
        )

        self._rect_hiding_bottom_text_id = self.canvas.create_rectangle(
            x0 + 1,
            y1 - 20,
            x1,
            y1,
            fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag) + temp,
            width=0,
            state=state
        )


    def add_text(self, text: str) -> None:
        """
        Méthode qui ajoute du texte à l'historique.
        Elle coupera le texte pour qu'il rentre en largeur dans l'historique.
        Elle ajoutera sa taille en hauteur à la longueur totale des textes dans l'historique.
        Elle refera descendre l'historique à sa hauteur pour que le joueur voie quand il y a du nouveau.
        Elle ajoutera le nouveau texte au groupe en lui ajoutant le tag self._text_group_tag.
        Elle refera calculer la nouvelle taille du thumb de la scrollbar.
        """
        # Si on a pas de texte, on ne rajoute rien
        if not text:
            return

        coords1 = self.canvas.coords(self._rect_hiding_top_text_id)
        coords2 = self.canvas.coords(self._rect_hiding_bottom_text_id)
        coords = [coords1[0], coords1[3], coords2[2], coords2[1]]

        # On doit savoir combien de fois, il faut séparer le texte de \n pour qu'il rentre dans l'historique
        fractions = 1
        length = get_width_text(text)
        #print(self.canvas.coords(self._thumb_id))
        while length / fractions > self.canvas.coords(self._thumb_id)[0] - coords[0]:
            fractions += 1

        text = separer_chaine_sans_couper(text, fractions)
        if fractions > 1 :
            for t in text :
                self.add_text(t)
            return
        tags = list(set_tags(hud_tag=self.tag))

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
        self._longueur_texte += text_height

        # On simule la descente de la scrollbar tout en bas
        if self._last_text_id:
            self.drag_text(coords[3] - 20 - text_height - self.canvas.coords(self._last_text_id)[1])
            self.canvas.move(self._thumb_id, 0, coords[3] - self.canvas.coords(self._thumb_id)[3])

        # Dès que l'historique a été bien remonté pour que les textes ne se cheuvauchent pas,
        # On peut grouper le nouveau texte avec ses compatriotes.
        tags[GROUP_TAG_INDEX] = self._text_group_tag
        self.canvas.itemconfigure(text_id, tags=tags)
        self._last_text_id = text_id

        # On met bien les rectangles cachants le texte au-dessus d'eux
        self.canvas.tag_raise(self._rect_hiding_top_text_id, self._text_group_tag)
        self.canvas.tag_raise(self._rect_hiding_bottom_text_id, self._text_group_tag)

        # Après avoir mis à jour la longueur du texte, on met à jour la taille de lu thumb de la scrollbar
        self.resize_thumb()

    def resize_thumb(self):

        coords1 = self.canvas.coords(self._rect_hiding_top_text_id)
        coords2 = self.canvas.coords(self._rect_hiding_bottom_text_id)
        coords = [coords1[0], coords1[3], coords2[2], coords2[1]]

        height = coords[3] - coords[1]

        longueur_viewport = height
        taille_scrollbar = height

        # (longueur_viewport / longueur_contenu) * taille_scrollbar
        longueur_thumb = (longueur_viewport // self._longueur_texte) * taille_scrollbar if self._longueur_texte > longueur_viewport else height - 1

        # On limite la taille du thumb de la scrollbar quand même
        longueur_thumb = longueur_thumb if longueur_thumb > 20 else 20

        coords_thumb = self.canvas.coords(self._thumb_id)
        self.canvas.coords(self._thumb_id, coords_thumb[0], coords[3] - longueur_thumb - 1, coords_thumb[2], coords[3] - 1)

    def drag_text(self, dy: int | float):
        self.canvas.move(self._text_group_tag, 0, dy)
        self.hide_exceeding_text()

    def hide_exceeding_text(self):
        text_history_ids = self.canvas.find_withtag(self._text_group_tag)
        i = 0

        # Tous les textes en haut du rectangle deviennent hidden
        while i < len(text_history_ids) and self.canvas.coords(text_history_ids[i])[1] < self.canvas.coords(self._rect_hiding_top_text_id)[1] + 20:
            self.canvas.itemconfigure(text_history_ids[i], state="hidden")
            i += 1

        # Ceux au milieu, on les laisse
        while i < len(text_history_ids) and self.canvas.coords(text_history_ids[i])[1] < self.canvas.coords(self._rect_hiding_bottom_text_id)[3]:
            self.canvas.itemconfigure(text_history_ids[i], state="normal")
            i += 1

        # Ceux en bas du rectangle deviennent hidden
        while i < len(text_history_ids):
            self.canvas.itemconfigure(text_history_ids[i], state="hidden")
            i += 1

    def on_drag_scrollbar(self, event: tk.Event):

        dy = event.y - self.canvas.mouse_coor[1]

        if self.canvas.coords(self._thumb_id)[1] + dy < self.canvas.coords(self._rect_hiding_top_text_id)[3] + 1 or \
            self.canvas.coords(self._thumb_id)[3] + dy > self.canvas.coords(self._rect_hiding_bottom_text_id)[1] - 1:
            dy = 0

        # Déplace tous les carrés avec le tag "square"
        self.canvas.move("active", 0, dy)

        coords1 = self.canvas.coords(self._rect_hiding_top_text_id)
        coords2 = self.canvas.coords(self._rect_hiding_bottom_text_id)
        coords = [coords1[0], coords1[3], coords2[2], coords2[1]]
        height = coords[3] - coords[1]

        longueur_viewport = height

        # distance_defilée = fraction défilée * taille totale du contenu
        # fraction defilée = distance effectuee / taille de la viewport
        distance_defilee = (dy / longueur_viewport) * self._longueur_texte
        self.drag_text(-distance_defilee)
