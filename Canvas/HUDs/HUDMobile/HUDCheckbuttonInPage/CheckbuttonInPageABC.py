
from typing import Optional
from abc import ABC

from Canvas.HUDs.HUDMobile.HUDMobileABC import HUDMobileABC
from Canvas.HUDs.Radiobutton import Checkbutton
from Canvas.HUDs.StringVar import StringVar
from parameter import *


class CheckbuttonInPageABC(HUDMobileABC, ABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        # Gestion des pages
        self.num_page = 1
        self.t_page: Optional[StringVar] = None

        self.checkbuttons: list[Checkbutton] = [self.canvas.add_checkbutton()]

        self.choices_id: list[int] = []
        self.choices_texts: list[StringVar] = []

        # Dictionnaire des index des checkbutton qui mènent vers leurs différentes catégories qui mènent vers
        # L'id des villages
        self.from_checkbutton_index_to_item_id_to_item_id: dict[int, dict[int, int]] = {0: {}}
        self.from_checkbutton_index_to_item_id_to_text: dict[int, dict[int, str]] = {0: {}}

    @property
    def cur_checkbutton(self):
        return self.checkbuttons[self.num_page - 1]

    def create(self, titre: str) -> tuple[int, int, int, int]:

        height = 20
        height_choice = 40

        title_text = titre

        # Mesurer la largeur et la hauteur du texte
        # Ici, ajout d'un pad sur la largeur pour éviter d'avoir un rectangle PARFAITEMENT à la largeur du texte
        text_width = get_width_text(title_text)

        # coordonnées du rectangle principal pour l'avoir au milieu de l'écran
        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = text_width
        y1_cadre = height + RBTN_MAX_VIL * height_choice

        center_x = (x0_cadre + x1_cadre) // 2

        self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, height,
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

        """
        Création de RBTN_MAX_VIL rectangles de choix
        """
        cur_height = height

        for i in range(RBTN_MAX_VIL):
            new_category_id = self.canvas.create_rectangle(
            x0_cadre, cur_height, x1_cadre, cur_height + height_choice,
            fill = FILL_ACTION_BOX,
            tags = set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state = "hidden",
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
        ).set(f"page : 1 / {len(self.checkbuttons)}")

        return x0_cadre, y0_cadre, x1_cadre, y1_cadre

    def add_option_update_HUD(self, name: str, item_id: int) -> int:
        """

        """
        # S'il y a RBTN_MAX_VIL choix sur le dernier checkbutton alors
        if self.checkbuttons[-1].nb_options == RBTN_MAX_VIL:

            # Créer une nouvelle page où il y aura un nouveau checkbutton
            self.checkbuttons.append(self.canvas.add_checkbutton())
            self.from_checkbutton_index_to_item_id_to_item_id[len(self.checkbuttons) - 1] = {}
            self.from_checkbutton_index_to_item_id_to_text[len(self.checkbuttons) - 1] = {}

        # Si le nouveau choix est sur la première page alors
        if len(self.checkbuttons) == 1:

            # Ajouter le texte dans les choix.
            self.choices_texts[self.checkbuttons[0].nb_options].set(name)

        """
        Ajouter un nouveau choix au dernier checkbutton
        """
        # Ajouter l'option infra au dernier checkbutton

        # J'associe l'id du village à l'id du choix (= le rectangle correspondant au choix)
        new_category_id = self.choices_id[self.checkbuttons[-1].nb_options]
        self.checkbuttons[-1].add_option(new_category_id)

        # On remet le group_tag de l'option au checkbutton actuel
        tags = list(self.canvas.gettags(new_category_id))
        tags[GROUP_TAG_INDEX] = self.cur_checkbutton.group_tag
        tags[HIGHLIGHT_TAG_INDEX] = TOGGLEABLE_TAG
        self.canvas.itemconfigure(new_category_id, tags=tags)

        self.from_checkbutton_index_to_item_id_to_item_id[len(self.checkbuttons) - 1][new_category_id] = item_id
        self.from_checkbutton_index_to_item_id_to_text[len(self.checkbuttons) - 1][new_category_id] = name

        self.t_page.set(f"page : {self.num_page} / {len(self.checkbuttons)}")

        return new_category_id

    def change_page(self, *args):
        self.cur_checkbutton.griser()

        # Différienciation entre page précédente (M) et page suivante (P)
        if self.canvas.gettags("active")[TRIGGER_TAG_INDEX][-1] == "M":
            self.num_page = self.num_page - 1 if self.num_page - 1 >= 1 else 1

        else:
            self.num_page = self.num_page + 1 if self.num_page + 1 <= len(self.checkbuttons) else len(self.checkbuttons)

        self.cur_checkbutton.degriser()

        for action_rect_id_i in range(self.cur_checkbutton.nb_options):

            # Modification du texte
            self.choices_texts[action_rect_id_i].set(
                self.from_checkbutton_index_to_item_id_to_text[self.num_page - 1][self.choices_id[action_rect_id_i]]
            )

            tags = list(self.canvas.gettags(self.choices_id[action_rect_id_i]))
            tags[HIGHLIGHT_TAG_INDEX] = TOGGLEABLE_TAG
            tags[GROUP_TAG_INDEX] = self.cur_checkbutton.group_tag

            # Modification des tags (pour savoir quelles fonctions vont être trigger)
            self.canvas.itemconfigure(
                self.choices_id[action_rect_id_i],
                tags=tags
            )

        for action_rect_id_i in range(RBTN_MAX_VIL - self.cur_checkbutton.nb_options):
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

        self.t_page.set(f"page : {self.num_page} / {len(self.checkbuttons)}")

    def bhide(self, *args):
        for c in self.checkbuttons:
            c.reset()

        self.hide()

    def get_items_choosed(self):
        return [
            self.from_checkbutton_index_to_item_id_to_item_id[i][item_id]
            for i in range(len(self.checkbuttons))
            for item_id in self.checkbuttons[i].currently_selected
        ]