
import tkinter as tk

from Canvas.Widget.Button import Button
from ..HUDHideable import HUDHideableABC
from ..HUDStaticABC import HUDStaticABC
from Canvas.Widget.StringVar import StringVar
from parameter import *

class Actions(HUDStaticABC, HUDHideableABC):
    def __init__(self, canvas):
        HUDHideableABC.__init__(self, canvas)
        HUDStaticABC.__init__(self, canvas)

        self.num_page = 1

        self.actions_rectangle_ids = []

        self.t_page = StringVar(canvas)
        self.ts_title_action: list[StringVar] = []

        self.ts_additionnal_cost: list[StringVar] = []

        self.ts_PA: list[StringVar] = []

        self.title_font = self.canvas.font.copy()
        self.title_font.config(weight="bold")

        self.temp_tag_storage: list[str] = ["", ""]

    @property
    def curr_show_pos(self) -> Position: return Position(0, self.canvas.coords(self.actions_rectangle_ids[0])[3])
    @property
    def curr_hide_pos(self) -> Position: return Position(0, self.canvas.coords(SHOW_OR_HIDE_PAGE_TAG)[3])
    @property
    def arrival_pos_show(self) -> Position: return Position(0, self.canvas.master.winfo_height() - PADY_BOTTOM_HUD - 10)
    @property
    def arrival_pos_hide(self) -> Position: return Position(0, self.canvas.master.winfo_height() - 5)
    @property
    def hide_symbol(self) -> str: return "▼"
    @property
    def show_symbol(self) -> str: return "▲"

    def create(self, geometry_width, geometry_height):

        # Gros rectangle contenant les 4 rectangles d'actions
        width = 480
        height = HEIGHT_BOTTOM_HUD  # valeurs qui ne bougent pas en fonction de la taille de la fenêtre

        x0_cadre = PADX_BOTTOM_HUD
        x1_cadre = x0_cadre + width
        y1_cadre = geometry_height - PADY_BOTTOM_HUD
        y0_cadre = y1_cadre - height

        centre_x = (x0_cadre + x1_cadre) // 2

        # Comme la création des carrés, on va créer les rectangles d'actions automatiquement,
        # D'abord le rectangle allant de x0_cadre à centre_x et de y0_cadre à centre_y
        # Puis le rectangle allant de centre_x à x1_cadre et de y0_cadre à centre_y, etc.
        x_values = [x0_cadre, centre_x, x1_cadre]
        pad = 5

        # Commentaire numéro 10
        for x_value_i in range(len(x_values) - 1):
            # Commentaire numéro 11 Ok, on est bon
            id_rectangle = self.canvas.create_rectangle(
                x_values[x_value_i], y0_cadre, x_values[x_value_i + 1], y1_cadre,
                fill=FILL_ACTION_BOX,
                tags=set_tags(CLICKABLE_TAG, ACTION_FOR_YOUR_TURN[x_value_i]["do"], hud_tag=self.tag) + (RECTANGLE_ACTION,)
            )

            # Titre de l'action
            text = StringVar(self.canvas)
            text.id = self.canvas.create_text(
                x_values[x_value_i] + pad, y0_cadre + pad,
                anchor="nw",
                tags=set_tags(hud_tag=self.tag) + (TEXT_TAG,),
                font=self.title_font,
                fill=FILL_TEXT
            )
            text.set(ACTION_FOR_YOUR_TURN[x_value_i]["text"])

            self.ts_title_action.append(text)
            self.canvas.text_id_in_rectangle_id[text.id] = id_rectangle

            # Nombre de points d'actions utilisés
            text = StringVar(self.canvas)
            text.id = self.canvas.create_text(
                x_values[x_value_i + 1] - pad, y0_cadre + pad,
                anchor="ne",
                tags=set_tags(hud_tag=self.tag) + (TEXT_TAG,),
                fill=FILL_TEXT
            )
            text.set(ACTION_FOR_YOUR_TURN[x_value_i]["PA"])

            self.ts_PA.append(text)
            self.canvas.text_id_in_rectangle_id[text.id] = id_rectangle

            # Coûts supplémentaires potentiels (argent, ressources)
            text = StringVar(self.canvas)
            text.id = self.canvas.create_text(
                x_values[x_value_i + 1] - pad, y0_cadre + pad + 40,
                anchor="ne",
                font=("", SIZE_ACTION_ADDITIONAL_COST_TEXT),
                tags=set_tags(hud_tag=self.tag) + (TEXT_TAG,),
                fill=FILL_TEXT
            )
            text.set(ACTION_FOR_YOUR_TURN[x_value_i]["additionalcost"])

            self.ts_additionnal_cost.append(text)
            self.canvas.text_id_in_rectangle_id[text.id] = id_rectangle
            self.actions_rectangle_ids.append(id_rectangle)

        self.t_page = StringVar(self.canvas)
        self.t_page.id = self.canvas.create_text(
            x0_cadre + 80,
            y0_cadre - 15,
            tags=set_tags(hud_tag=self.tag)
        )
        self.t_page.set(f"page : 1 / {len(ACTION_FOR_YOUR_TURN) // 2}")

        # Bouton pour changer de page (précédente)
        Button(
            self.canvas,
            hud_tag=self.tag,
            trigger_name=CHANGE_PAGE_MINUS,
            func_triggered=self.on_change_page,
            for_which_game_mode=("basic",)
        ).draw(
            x0_cadre + 5,
            y0_cadre - 20,
            x0_cadre + 20,
            y0_cadre - 5,
            text="◄",  # ►◄↓↑→←▲▼
        )

        # Bouton pour changer de page (suivante)
        Button(
            self.canvas,
            hud_tag=self.tag,
            trigger_name=CHANGE_PAGE_PLUS,
            func_triggered=self.on_change_page,
            for_which_game_mode=("basic",)
        ).draw(
            x0_cadre + 25,
            y0_cadre - 20,
            x0_cadre + 40,
            y0_cadre - 5,
            text="►",  # ►◄↓↑→←▲▼
        )

        # Bouton pour cacher l'hud du bas
        self.hide_button_id = Button(
            self.canvas,
            hud_tag=self.tag,
            trigger_name=SHOW_OR_HIDE_PAGE_TAG,
            func_triggered=self.show_or_hide,
            for_which_game_mode=("basic",)
        ).draw(
            x1_cadre - 20,
            y0_cadre - 20,
            x1_cadre - 5,
            y0_cadre - 5,
            text="▼"
        )

    def replace(self, event: tk.Event):
        """
        Replacer l'HUDs du bas:
        - mouvement sur x : Son centre reste au centre de l'image donc on prend la distance entre l'ancien centre et
            le nouveau et on déplace tous les éléments du HUDs de cette distance
        - mouvement sur y : On déplace tous les éléments
        """
        self.canvas.move(
            self.tag,
            PADX_BOTTOM_HUD + 5 - self.canvas.coords(self.canvas.find_withtag(CHANGE_PAGE_MINUS)[0])[0],
            event.height - self.canvas.master.previous_geometry[1]
        )

    def next_page(self):
        self.num_page = (self.num_page + 1) if self.num_page + 1 <= NB_ACTIONS // NB_ACTION_PER_PAGE else NB_ACTIONS // NB_ACTION_PER_PAGE

    def previous_page(self):
        self.num_page = (self.num_page - 1) if self.num_page - 1 >= 1 else 1

    def on_change_page(self, event: tk.Event):
        # Différenciation entre page précédente (M) et page suivante (P)
        if self.canvas.gettags("active")[TRIGGER_TAG_INDEX][-1] == "M":
            self.previous_page()

        else:
            self.next_page()

        self.change_page()

    def change_page(self):
        for action_rect_id_i in range(len(self.actions_rectangle_ids)):

            action_i = (self.num_page - 1) * NB_ACTION_PER_PAGE + action_rect_id_i

            # Modification du texte
            self.ts_title_action[action_rect_id_i].set(ACTION_FOR_YOUR_TURN[action_i]["text"])
            self.ts_additionnal_cost[action_rect_id_i].set(ACTION_FOR_YOUR_TURN[action_i]["additionalcost"])
            self.ts_PA[action_rect_id_i].set(ACTION_FOR_YOUR_TURN[action_i]["PA"])

            # Modification des tags (pour savoir quelles fonctions vont être trigger)
            self.canvas.itemconfigure(
                self.actions_rectangle_ids[action_rect_id_i],
                tags=set_tags(
                    highlight_tag=CLICKABLE_TAG,
                    trigger_tag=ACTION_FOR_YOUR_TURN[action_i]["do"],
                    hud_tag=self.tag
                )
            )

        self.t_page.set(f"page : {self.num_page} / {len(ACTION_FOR_YOUR_TURN) // 2}")
