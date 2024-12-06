
from typing import Optional

from Canvas.HUDs.Button import Button
from Canvas.HUDs.Radiobutton import Checkbutton
from Canvas.HUDs.StringVar import StringVar
from parameter import *
from Canvas.HUDs.HUDMobile.HUDMobileABC import HUDMobileABC

class HUDMobileChooseTaxes(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.num_page_villages = 1
        self.t_villages_page: Optional[StringVar] = None

        self.background_rectangle_id = 0
        self.ok_button: Optional[Button] = None
        self.cancel_button: Optional[Button] = None

        # id du dernier village choisi
        self.last_choice_made = 0
        self.checkbuttons_village: list[Checkbutton] = []

        self.village_choices_id: list[int] = []
        self.villages_choices_texts: list[StringVar] = []

        # Dictionnaire des index des checkbutton qui mènent vers leurs différentes catégories qui mènent vers
        # L'id des villages
        self.from_checkbutton_index_to_item_id_to_city_id: dict[int, dict[int, int]] = {}
        self.from_checkbutton_index_to_item_id_to_text: dict[int, dict[int, str]] = {}

    @property
    def tag(self):
        return HUD_CHOOSE_TAXES

    @property
    def cur_checkbutton(self):
        return self.checkbuttons_village[self.num_page_villages - 1]

    def create(self) -> None:

        height = 20

        title_text = "Quel village imposer ?"

        # Mesurer la largeur et la hauteur du texte
        # Ici, ajout d'un pad sur la largeur pour éviter d'avoir un rectangle PARFAITEMENT à la largeur du texte
        text_width = get_width_text(title_text)

        # coordonnées du rectangle principal pour l'avoir au milieu de l'écran
        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = text_width
        y1_cadre = height

        center_x = (x0_cadre + x1_cadre) // 2

        self.background_rectangle_id = self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre, fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,), state="hidden"
        )

        self.canvas.create_text(
            center_x, y0_cadre + 10,
            text=title_text,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden",
                fill=FILL_TEXT
        )

        # Bouton pour changer de page (précédente)
        self.canvas.add_button(
            hud_tag=self.tag,
            trigger_name="CHANGE_PAGE_VASSALS_M",
            func_triggered=self.change_vassals_page,
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
            trigger_name="CHANGE_PAGE_VASSALS_P",
            func_triggered=self.change_vassals_page,
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

        self.t_villages_page = StringVar(
            self.canvas,
            self.canvas.create_text(
                x0_cadre + 80,
                y0_cadre - 15,
                tags=set_tags(hud_tag=self.tag)
            )
        ).set(f"page : 1 / {len(self.checkbuttons_village)}")

        # Bouton OK qui lance l'immigration
        self.ok_button = self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.imposer, is_temp=True, state="hidden"
        )

        # Bouton Annuler qui annule l'immigration
        self.cancel_button = self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.bhide, is_temp=True, state="hidden"
        )

        # Radiobutton du choix du village
        self.checkbuttons_village.append(self.canvas.add_checkbutton())
        self.from_checkbutton_index_to_item_id_to_city_id[0] = {}
        self.from_checkbutton_index_to_item_id_to_text[0] = {}

    def replace(self) -> None:

        bbox = self.canvas.bbox(self.tag)

        dx = self.canvas.master.winfo_width() // 2 - (bbox[2] + bbox[0]) // 2
        dy = self.canvas.master.winfo_height() // 2 - (bbox[3] + bbox[1]) // 2

        self.canvas.move(self.tag, dx, dy)

    def add_village_update_HUD(self, name: str, city_id: int) -> int:
        """
        S'il y a moins de RBTN_MAX_VIL choix sur le premier checkbutton alors
            Mettre à jour la taille du rectangle en background
            Créer un rectangle du nouveau choix
            Déplacer le bouton OK et le bouton Annuler en bas
        Sinon s'il y a RBTN_MAX_VIL choix sur le dernier checkbutton alors
            Créer une nouvelle page où il y aura un nouveau checkbutton

        Ajouter l'option infra au dernier checkbutton
        """
        if self.checkbuttons_village[0].nb_options < RBTN_MAX_VIL:
            """
            Mettre à jour la taille du rectangle en background et déplacer les boutons
            """
            coords = self.canvas.coords(self.background_rectangle_id)

            coords[3] += 40

            self.canvas.coords(self.background_rectangle_id, coords[0], coords[1], coords[2], coords[3])

            new_category_id = self.canvas.create_rectangle(
                coords[0], coords[3] - 40, coords[2], coords[3],
                fill=FILL_ACTION_BOX,
                tags=set_tags(highlight_tag=TOGGLEABLE_TAG, hud_tag=self.tag) + (TEMP_TAG,),
                state="hidden",
            )

            text = StringVar(
                self.canvas,
                self.canvas.create_text(
                    (coords[0] + coords[2]) // 2, (coords[3] - 40 + coords[3]) // 2,
                    text=name,
                    tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG),
                    state="hidden",
                    fill=FILL_TEXT
                )
            )

            self.canvas.text_id_in_rectangle_id[text.id] = new_category_id
            self.canvas.text_id_in_rectangle_id[new_category_id] = text.id

            self.villages_choices_texts.append(text)
            self.village_choices_id.append(new_category_id)

            self.canvas.tag_lower(new_category_id, self.ok_button.id)
            self.canvas.tag_lower(self.canvas.text_id_in_rectangle_id[new_category_id], self.ok_button.id)

            # Déplacer vers le bas de la hauteur de la nouvelle catégorie les deux boutons
            self.ok_button.move(0, 40)
            self.cancel_button.move( 0, 40)

        elif self.checkbuttons_village[-1].nb_options == RBTN_MAX_VIL:
            """
            Créer une nouvelle page avec un checkbutton
            """
            self.checkbuttons_village.append(self.canvas.add_checkbutton())
            self.from_checkbutton_index_to_item_id_to_city_id[len(self.checkbuttons_village) - 1] = {}
            self.from_checkbutton_index_to_item_id_to_text[len(self.checkbuttons_village) - 1] = {}

        """
        Ajouter un nouveau choix au dernier checkbutton
        """

        # J'associe l'id du village à l'id du choix (= le rectangle correspondant au choix)
        new_category_id = self.village_choices_id[self.checkbuttons_village[-1].nb_options]
        self.checkbuttons_village[-1].add_option(new_category_id)

        # On remet le group_tag de l'option au checkbutton actuel
        tags = list(self.canvas.gettags(new_category_id))
        tags[GROUP_TAG_INDEX] = self.cur_checkbutton.group_tag
        self.canvas.itemconfigure(new_category_id, tags=tags)

        self.from_checkbutton_index_to_item_id_to_city_id[len(self.checkbuttons_village) - 1][new_category_id] = city_id
        self.from_checkbutton_index_to_item_id_to_text[len(self.checkbuttons_village) - 1][new_category_id] = name

        self.t_villages_page.set(f"page : {self.num_page_villages} / {len(self.checkbuttons_village)}")

        return new_category_id

    def change_vassals_page(self, *args):

        self.cur_checkbutton.griser()

        # Différienciation entre page précédente (M) et page suivante (P)
        if self.canvas.gettags("active")[TRIGGER_TAG_INDEX][-1] == "M":
            self.num_page_villages = self.num_page_villages - 1 if self.num_page_villages - 1 >= 1 else 1

        else:
            self.num_page_villages = self.num_page_villages + 1 if self.num_page_villages + 1 <= len(self.checkbuttons_village) else len(self.checkbuttons_village)

        self.cur_checkbutton.degriser()

        for action_rect_id_i in range(self.cur_checkbutton.nb_options):

            # Modification du texte
            self.villages_choices_texts[action_rect_id_i].set(
                self.from_checkbutton_index_to_item_id_to_text[self.num_page_villages - 1][self.village_choices_id[action_rect_id_i]]
            )

            tags = list(self.canvas.gettags(self.village_choices_id[action_rect_id_i]))
            tags[HIGHLIGHT_TAG_INDEX] = TOGGLEABLE_TAG
            tags[GROUP_TAG_INDEX] = self.cur_checkbutton.group_tag

            # Modification des tags (pour savoir quelles fonctions vont être trigger)
            self.canvas.itemconfigure(
                self.village_choices_id[action_rect_id_i],
                tags=tags
            )

        for action_rect_id_i in range(RBTN_MAX_VIL - self.cur_checkbutton.nb_options):
            self.villages_choices_texts[RBTN_MAX_VIL - action_rect_id_i - 1].set(
                ""
            )

            tags = list(self.canvas.gettags(self.village_choices_id[RBTN_MAX_VIL - action_rect_id_i - 1]))
            tags[HIGHLIGHT_TAG_INDEX] = NOTHING_TAG
            tags[GROUP_TAG_INDEX] = ""

            # Modification des tags (pour savoir quelles fonctions vont être trigger)
            self.canvas.itemconfigure(
                self.village_choices_id[RBTN_MAX_VIL - action_rect_id_i - 1],
                tags=tags
            )

        self.t_villages_page.set(f"page : {self.num_page_villages} / {len(self.checkbuttons_village)}")

    def imposer(self, *args):
        for i in range(len(self.checkbuttons_village)):
            print(self.from_checkbutton_index_to_item_id_to_city_id[i])

    def bhide(self, *args):
        for c in self.checkbuttons_village:
            c.reset()

        self.hide()
