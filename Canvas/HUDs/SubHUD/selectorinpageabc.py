
from abc import ABC, abstractmethod

from Canvas.HUDs.SubHUD.base import SubHUDABC
from Canvas.Widget.StringVar import StringVar
from Canvas.Widget.Radiobutton import SelectorsABC
from parameter import *

class SelectorInPageABC(SubHUDABC, ABC):
    def __init__(self, canvas, hud_tag: str):
        super().__init__(canvas, hud_tag)

        # Gestion des pages
        self.num_page = 1
        self.t_page = StringVar(self.canvas)

        # Liste des choix (rectangles et textes dessus)
        self.choices_id: list[int] = []
        self.choices_texts: list[StringVar] = []

        # Dictionnaire des index des checkbutton qui mènent vers leurs différentes catégories qui mènent vers
        # L'id des villages
        self.from_selector_index_to_item_id_to_item: dict[int, dict[int, int]] = {0: {}}
        self.from_selector_index_to_item_id_to_text: dict[int, dict[int, str]] = {0: {}}

    @property
    def cur_selector(self) -> SelectorsABC:
        return self.selectors[self.cur_selector_index]

    @property
    def cur_selector_index(self) -> int:
        return self.num_page - 1

    @property
    @abstractmethod
    def selectors(self) -> list[SelectorsABC]:
        """
        Méthode qui retournera les sélecteurs de l'HUD
        """
        pass

    @property
    @abstractmethod
    def selected_option(self):
        """
        Méthode qui retournera les options sélectionnées sur le selecteur
        """
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        """
        Méthode qui retournera le titre de l'HUD
        """
        pass

    @property
    @abstractmethod
    def add_selector(self) -> callable:
        """
        Méthode qui retourne la fonction nécessaire pour ajouter un sélecteur
        """
        pass

    def create(self, x0_cadre: float, y0_cadre: float) -> tuple[float, float, float, float]:

        height = 20
        height_choice = 40

        title_text = self.title

        # Mesurer la largeur et la hauteur du texte
        # Ici, ajout d'un pad sur la largeur pour éviter d'avoir un rectangle PARFAITEMENT à la largeur du texte
        text_width = get_width_text(title_text)

        # coordonnées du rectangle principal pour l'avoir au milieu de l'écran
        x1_cadre = x0_cadre + text_width
        y1_cadre = y0_cadre + height + RBTN_MAX_VIL * height_choice

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

            text = StringVar(self.canvas)
            text.id = self.canvas.create_text(
                center_x, (cur_height + cur_height + height_choice) // 2,
                text="",
                tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG),
                state="hidden",
                fill=FILL_TEXT
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

        self.t_page.id = self.canvas.create_text(
            x0_cadre + 80,
            y0_cadre - 15,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden"
        )
        self.t_page.set(f"page : 1 / {len(self.selectors)}")

        return x0_cadre, y0_cadre, x1_cadre, y1_cadre

    def add_option(self, name: str, item_id: int) -> int:
        """

        """
        # S'il y a RBTN_MAX_VIL choix sur le dernier checkbutton alors
        if self.selectors[-1].nb_options == RBTN_MAX_VIL:

            # Créer une nouvelle page où il y aura un nouveau checkbutton
            self.selectors.append(self.add_selector())
            self.from_selector_index_to_item_id_to_item[len(self.selectors) - 1] = {}
            self.from_selector_index_to_item_id_to_text[len(self.selectors) - 1] = {}

            self.t_page.set(f"page : {self.num_page} / {len(self.selectors)}")

        # Si le nouveau choix est sur la première page alors
        if len(self.selectors) == 1:

            # Ajouter le texte dans les choix.
            self.choices_texts[self.selectors[0].nb_options].set(name)

        """
        Ajouter un nouveau choix au dernier checkbutton
        """
        # Ajouter l'option infra au dernier checkbutton

        # J'associe l'id du village à l'id du choix (= le rectangle correspondant au choix)
        new_category_id = self.choices_id[self.selectors[-1].nb_options]
        self.selectors[-1].add_option(new_category_id)

        # On remet le group_tag de l'option au checkbutton actuel
        tags = list(self.canvas.gettags(new_category_id))
        tags[GROUP_TAG_INDEX] = self.cur_selector.group_tag
        tags[HIGHLIGHT_TAG_INDEX] = TOGGLEABLE_TAG
        self.canvas.itemconfigure(new_category_id, tags=tags)

        self.from_selector_index_to_item_id_to_item[len(self.selectors) - 1][new_category_id] = item_id
        self.from_selector_index_to_item_id_to_text[len(self.selectors) - 1][new_category_id] = name

        return new_category_id

    def change_page(self, *args):
        """
        Méthode appelée lors d'un click sur page suivant ou page précédente.
        """

        self.griser()

        # Différienciation entre page précédente (M) et page suivante (P)
        if self.canvas.gettags("active")[TRIGGER_TAG_INDEX][-1] == "M":
            self.num_page = self.num_page - 1 if self.num_page - 1 >= 1 else 1

        else:
            self.num_page = self.num_page + 1 if self.num_page + 1 <= len(self.selectors) else len(self.selectors)

        self.degriser()

        for action_rect_id_i in range(self.cur_selector.nb_options):

            # Modification du texte
            self.choices_texts[action_rect_id_i].set(
                self.from_selector_index_to_item_id_to_text[self.num_page - 1][self.choices_id[action_rect_id_i]]
            )

            tags = list(self.canvas.gettags(self.choices_id[action_rect_id_i]))
            tags[HIGHLIGHT_TAG_INDEX] = TOGGLEABLE_TAG
            tags[GROUP_TAG_INDEX] = self.cur_selector.group_tag

            # Modification des tags (pour savoir quelles fonctions vont être trigger)
            self.canvas.itemconfigure(
                self.choices_id[action_rect_id_i],
                tags=tags
            )

        for action_rect_id_i in range(RBTN_MAX_VIL - self.cur_selector.nb_options):
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

        self.t_page.set(f"page : {self.num_page} / {len(self.selectors)}")

    def reset_selectors(self):
        for s in self.selectors:
            s.reset()

    def setup_before_display(self, *args):
        self.reset_selectors()

    @abstractmethod
    def griser(self, *args) -> None:
        """
        Méthode qui "grisera" les choix sélectionnés (= cachera les choix sélectionnés).
        """
        pass

    @abstractmethod
    def degriser(self, *args) -> None:
        """
        Méthode qui "degrisera" les choix sélectionnés (= highlightera les choix sélectionnés).
        """
        pass
