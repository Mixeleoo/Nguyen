
from typing import Optional
from abc import ABC, abstractmethod
import tkinter as tk

from Canvas.HUDs.Button import Button
from Canvas.HUDs.Radiobutton import Radiobutton
from Canvas.HUDs.HUDMobile.HUDMobileABC import HUDMobileABC
from Canvas.HUDs.StringVar import StringVar
from parameter import *

class HUDRadiobuttonInPageABC(HUDMobileABC, ABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.background_rectangle_id = 0
        self.ok_button: Optional[Button] = None
        self.cancel_button: Optional[Button] = None

        self.from_radiobutton_item_id_to_city_id: dict[int, int] = {}

        # Gestion des pages
        self.num_page = 1
        self.t_page: Optional[StringVar] = None

        self.last_radiobutton_index_choice = None
        self.radiobuttons: list[Radiobutton] = [self.canvas.add_radiobutton()]

        self.choices_id: list[int] = []
        self.choices_texts: list[StringVar] = []

        # Dictionnaire des index des checkbutton qui mènent vers leurs différentes catégories qui mènent vers
        # L'id des villages
        self.from_radiobutton_index_to_item_id_to_item: dict[int, dict[int, int]] = {0: {}}
        self.from_radiobutton_index_to_item_id_to_text: dict[int, dict[int, str]] = {0: {}}

    @property
    def cur_radiobutton(self):
        return self.radiobuttons[self.cur_radiobutton_index]

    @property
    def cur_radiobutton_index(self):
        return self.num_page - 1

    @property
    def selected_option(self):
        if self.last_radiobutton_index_choice is not None:
            return self.from_radiobutton_index_to_item_id_to_item[
                self.last_radiobutton_index_choice
            ][self.radiobuttons[self.last_radiobutton_index_choice].currently_selected]
        elif self.radiobuttons[0].currently_selected:
            return self.from_radiobutton_index_to_item_id_to_item[
                0
            ][self.radiobuttons[0].currently_selected]
        else:
            return None

    @property
    @abstractmethod
    def title(self):
        pass

    @abstractmethod
    def ok_trigger(self, event: tk.Event):
        pass

    def create(self) -> None:

        height = 20
        height_choice = 40

        title_text = self.title

        # Mesurer la largeur et la hauteur du texte
        # Ici, ajout d'un pad sur la largeur pour éviter d'avoir un rectangle PARFAITEMENT à la largeur du texte
        text_width = get_width_text(title_text)

        # coordonnées du rectangle principal pour l'avoir au milieu de l'écran
        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = text_width
        y1_cadre = height + RBTN_MAX_VIL * height_choice

        center_x = (x0_cadre + x1_cadre) // 2

        self.background_rectangle_id = self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre,
            fill=FILL_ACTION_BOX,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden"
        )

        self.canvas.create_text(
            center_x, y0_cadre + 10,
            text=title_text,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden",
                fill=FILL_TEXT
        )

        cur_height = height

        for i in range(RBTN_MAX_VIL):
            new_category_id = self.canvas.create_rectangle(
                x0_cadre, cur_height, x1_cadre, cur_height + height_choice,
                fill=FILL_ACTION_BOX,
                tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
                state="hidden",
            )

            text = StringVar(
                self.canvas,
                self.canvas.create_text(
                    center_x, (cur_height + cur_height + height_choice) // 2,
                    text="",
                    tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG),
                    state="hidden",
                    fill=FILL_TEXT
                )
            )

            cur_height += height_choice

            self.canvas.text_id_in_rectangle_id[text.id] = new_category_id
            self.canvas.text_id_in_rectangle_id[new_category_id] = text.id

            self.choices_texts.append(text)
            self.choices_id.append(new_category_id)


        # Bouton OK qui lance l'immigration
        self.ok_button = self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.ok_trigger, is_temp=True, state="hidden"
        )

        # Radiobutton du choix du village
        self.radiobutton_village_choix = self.canvas.add_radiobutton()

        # Bouton Annuler qui annule l'immigration
        self.cancel_button = self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.bhide, is_temp=True, state="hidden"
        )

        # Bouton pour changer de page (précédente)
        self.canvas.add_button(
            hud_tag=self.tag,
            trigger_name="CHANGE_PAGE_" + self.tag + "_M",
            func_triggered=self.change_page,
            for_which_game_mode=("basic",)
        ).draw(
            x0_cadre + 5,
            y0_cadre - 20,
            x0_cadre + 20,
            y0_cadre - 5,
            text="◄",  # ►◄↓↑→←▲▼
            is_temp=True,
            state="hidden"
        )

        # Bouton pour changer de page (suivante)
        self.canvas.add_button(
            hud_tag=self.tag,
            trigger_name="CHANGE_PAGE_" + self.tag + "_P",
            func_triggered=self.change_page,
            for_which_game_mode=("basic",)
        ).draw(
            x0_cadre + 25,
            y0_cadre - 20,
            x0_cadre + 40,
            y0_cadre - 5,
            text="►",  # ►◄↓↑→←▲▼
            is_temp=True,
            state="hidden"
        )

        self.t_page = StringVar(
            self.canvas,
            self.canvas.create_text(
                x0_cadre + 80,
                y0_cadre - 15,
                tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
                state="hidden"
            )
        ).set(f"page : 1 / {len(self.radiobuttons)}")

    def replace(self, *args) -> None:

        bbox = self.canvas.bbox(self.tag)

        dx = self.canvas.master.winfo_width() // 2 - (bbox[2] + bbox[0]) // 2
        dy = self.canvas.master.winfo_height() // 2 - (bbox[3] + bbox[1]) // 2

        self.canvas.move(self.tag, dx, dy)

    def add_option(self, name: str, item: int) -> int:
        """

        """
        # S'il y a RBTN_MAX_VIL choix sur le dernier checkbutton alors
        if self.radiobuttons[-1].nb_options == RBTN_MAX_VIL:

            # Créer une nouvelle page où il y aura un nouveau checkbutton
            self.radiobuttons.append(self.canvas.add_radiobutton())
            self.from_radiobutton_index_to_item_id_to_item[len(self.radiobuttons) - 1] = {}
            self.from_radiobutton_index_to_item_id_to_text[len(self.radiobuttons) - 1] = {}

            self.t_page.set(f"page : {self.num_page} / {len(self.radiobuttons)}")

        # Si le nouveau choix est sur la première page alors
        if len(self.radiobuttons) == 1:

            # Ajouter le texte dans les choix.
            self.choices_texts[self.radiobuttons[0].nb_options].set(name)

        """
        Ajouter un nouveau choix au dernier checkbutton
        """
        # Ajouter l'option infra au dernier checkbutton

        # J'associe l'id du village à l'id du choix (= le rectangle correspondant au choix)
        new_category_id = self.choices_id[self.radiobuttons[-1].nb_options]
        self.radiobuttons[-1].add_option(new_category_id)

        # On remet le group_tag de l'option au checkbutton actuel
        tags = list(self.canvas.gettags(new_category_id))
        tags[GROUP_TAG_INDEX] = self.cur_radiobutton.group_tag
        tags[HIGHLIGHT_TAG_INDEX] = TOGGLEABLE_TAG
        self.canvas.itemconfigure(new_category_id, tags=tags)

        self.from_radiobutton_index_to_item_id_to_item[len(self.radiobuttons) - 1][new_category_id] = item
        self.from_radiobutton_index_to_item_id_to_text[len(self.radiobuttons) - 1][new_category_id] = name

        return new_category_id

    def change_page(self, *args):
        """

        """

        """
        Si il y a un élément sélectionné sur la page actuelle ET que le dernier choix effectué était sur une autre page
            ça veut dire qu'il faut griser le dernier radiobutton dans lequel un choix a été cliqué
        Sinon il faut allumer le choix sélectionné du prochain radiobutton.
        """
        if self.last_radiobutton_index_choice is not None:
            if self.cur_radiobutton.currently_selected and self.last_radiobutton_index_choice != self.cur_radiobutton_index:
                self.radiobuttons[self.last_radiobutton_index_choice].reset()

        if self.cur_radiobutton.currently_selected:
            self.last_radiobutton_index_choice = self.cur_radiobutton_index
            self.cur_radiobutton.griser()

        # Différienciation entre page précédente (M) et page suivante (P)
        if self.canvas.gettags("active")[TRIGGER_TAG_INDEX][-1] == "M":
            self.num_page = self.num_page - 1 if self.num_page - 1 >= 1 else 1

        else:
            self.num_page = self.num_page + 1 if self.num_page + 1 <= len(self.radiobuttons) else len(self.radiobuttons)

        self.cur_radiobutton.degriser()

        for action_rect_id_i in range(self.cur_radiobutton.nb_options):

            # Modification du texte
            self.choices_texts[action_rect_id_i].set(
                self.from_radiobutton_index_to_item_id_to_text[self.num_page - 1][self.choices_id[action_rect_id_i]]
            )

            tags = list(self.canvas.gettags(self.choices_id[action_rect_id_i]))
            tags[HIGHLIGHT_TAG_INDEX] = TOGGLEABLE_TAG
            tags[GROUP_TAG_INDEX] = self.cur_radiobutton.group_tag

            # Modification des tags (pour savoir quelles fonctions vont être trigger)
            self.canvas.itemconfigure(
                self.choices_id[action_rect_id_i],
                tags=tags
            )

        for action_rect_id_i in range(RBTN_MAX_VIL - self.cur_radiobutton.nb_options):
            self.choices_texts[RBTN_MAX_VIL - action_rect_id_i - 1].set(
                ""
            )

            tags = list(self.canvas.gettags(self.choices_id[RBTN_MAX_VIL - action_rect_id_i - 1]))
            tags[HIGHLIGHT_TAG_INDEX] = NOTHING_TAG
            tags[GROUP_TAG_INDEX] = ""

            # Modification des tags (pour savoir quelles fonctions vont être trigger)
            self.canvas.itemconfigure(
                self.choices_id[RBTN_MAX_VIL - action_rect_id_i - 1],
                tags=tags
            )

        self.t_page.set(f"page : {self.num_page} / {len(self.radiobuttons)}")

    def bhide(self, *args):
        self.radiobutton_village_choix.reset()
        self.hide()
