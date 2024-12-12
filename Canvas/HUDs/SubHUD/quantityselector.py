
from .base import SubHUDABC
from Canvas.Widget.StringVar import StringVar
from Canvas.hud_canvas import HUDCanvas
from parameter import *

class QuantitySelector(SubHUDABC):
    _instance_counter = 0
    def __init__(self, canvas: HUDCanvas, hud_tag: str, quantity_labeled: str,
                 min_quantity: int, max_quantity: int, callback: callable = None):
        super().__init__(canvas, hud_tag)
        self._quantity_labeled = quantity_labeled
        self._min_quantity = min_quantity
        self._max_quantity = max_quantity
        self.callback = callback

        self._index = QuantitySelector._instance_counter
        QuantitySelector._instance_counter += 1
        self._group_tag = "quantity_selector" + str(self._index)

        self._quantity = min_quantity
        self.ms_start = 500
        self.ms = 500
        self._text = StringVar(canvas)

    """def ajouter_fois_10_quantite_heuuuuupossiblkeenfonction_de_la_puissance_au_carre_de_la_valeur_retiree_juste_avant_si_il_y_a_pas_hinhin_retiré_salto_arriere_puissance_retire_en_fonction_de_la_meteo_par_evelyn_dhelia(self):
        pass"""

    @property
    def title(self):
        return self._quantity_labeled + str(self._quantity)

    @property
    def quantity(self) -> int:
        return self._quantity

    def create(self, center_x: float, center_y: float):

        text_width = get_width_text(self.title)
        button_width = 20
        button_height = 10
        pad_between_buttons = 2

        custom_font = font.nametofont("TkDefaultFont").copy()
        custom_font.config(size=6)

        self._text.id = self.canvas.create_text(
            center_x, center_y,
            text=self.title,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden",
            fill=FILL_TEXT
        )

        # Bouton ajouter effectif
        self.canvas.create_text_in_rectangle(
            center_x + text_width // 2,
            center_y - 11,
            center_x + text_width // 2 + button_width,
            center_y - 1,
            rectangle_tags=set_tags(highlight_tag="INC_" + self._group_tag, hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG),
            text="▲",
            text_font=custom_font,
            state="hidden"
        )

        self.canvas.new_highlight(
            "INC_" + self._group_tag,
            on_click=lambda: self.increase(1),
            on_release=self.canvas.unhighlight_clickable
        )

        # Bouton retirer effectif
        self.canvas.create_text_in_rectangle(
            center_x + text_width // 2,
            center_y + 1,
            center_x + text_width // 2 + button_width,
            center_y + 11,
            rectangle_tags=set_tags(highlight_tag="DEC_" + self._group_tag, hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG),
            text="▼",
            text_font=custom_font,
            state="hidden"
        )

        self.canvas.new_highlight(
            "DEC_" + self._group_tag,
            on_click=lambda: self.increase(-1),
            on_release=self.canvas.unhighlight_clickable
        )

    def update(self, max_quantity: int) -> None:
        self._max_quantity = max_quantity

    def increase(self, value_added: int):
        """
        Méthode pour démarrer l'incrémentation de la quantité voulue.
        """
        self.ms = self.ms_start
        self.canvas.highlight_clickable()
        self._inc_step(value_added)

    def _inc_step(self, value_added: int):
        """
        Méthode de chaque étape d'incrémentation de la quantité voulue.
        """
        if self._min_quantity <= self._quantity + value_added <= self._max_quantity:
            old_quantity = self._quantity
            self._quantity += value_added
            self._text.set(self.title)

            if self.callback is not None:
                self.callback(old_quantity)

            self.ms = self.ms - 50 if self.ms - 50 > 10 else 10
            self.canvas.after_quantity_selector_id = self.canvas.after(self.ms, self._inc_step, value_added)

    def reset(self):
        """
        Méthode qui remettra à zéro la quantité voulue.
        """
        self._quantity = self._min_quantity
        self._text.set(self.title)

    def deactivate(self):
        """
        Méthode pour désactiver les boutons du Widget.
        """
        pass

    def reactivate(self):
        """
        Méthode pour réactiver les boutons du Widget.
        """
        pass
