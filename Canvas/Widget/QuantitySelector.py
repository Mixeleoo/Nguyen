
from Canvas.HUDs.HUDMobile.HUDMobileABC import HUDMobileABC
from Canvas.Widget.StringVar import StringVar
from Canvas.hud_canvas import HUDCanvas
from parameter import *

class QuantitySelector(HUDMobileABC):
    def __init__(self, canvas: HUDCanvas, hud_tag: str, quantity_name: str):
        super().__init__(canvas)
        self.canvas = canvas
        self._tag = hud_tag
        self._quantity_name = quantity_name

        self._quantity = 0
        self.ms_start = 500
        self.ms = 500
        self._text = StringVar(canvas)

    # TODO méthodes: ajouter_quantité, _ajouter_step, reset, désactiver ?, réactiver ?

    """def ajouter_fois_10_quantite_heuuuuupossiblkeenfonction_de_la_puissance_au_carre_de_la_valeur_retiree_juste_avant_si_il_y_a_pas_hinhin_retiré_salto_arriere_puissance_retire_en_fonction_de_la_meteo_par_evelyn_dhelia(self):
        pass"""

    @property
    def tag(self):
        return self._tag

    @property
    def title(self):
        return self._quantity_name + str(self._quantity)

    def create(self, x0: float, y0: float):

        text_width = get_width_text(self.title)
        button_width = 20
        button_height = 10
        pad_between_buttons = 2

        custom_font = font.nametofont("TkDefaultFont").copy()
        custom_font.config(size=6)

        self._text.id = self.canvas.create_text(
            x0, y0,
            text=self.title,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden",
            fill=FILL_TEXT,
            anchor="nw"
        )

        # Bouton ajouter effectif
        self.canvas.create_text_in_rectangle(
            x0 + text_width,
            y0,
            x0 + text_width + button_width,
            y0 + button_height,
            rectangle_tags=set_tags(highlight_tag="PLUS_ARG", hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEMP_TAG, TEMP_TAG),
            text="▲",
            text_font=custom_font,
            state="hidden"
        )

        self.canvas.tag_highlight["PLUS_ARG"] = self._plus_arg_step
        self.canvas.tag_highlight["PLUS_ARG"] = self._plus_arg_step

        # Bouton retirer effectif
        self.canvas.create_text_in_rectangle(
            x0 + text_width,
            y0 + button_height + pad_between_buttons,
            x0 + text_width + button_width,
            y0 + button_height + pad_between_buttons + button_height,
            rectangle_tags=set_tags(highlight_tag="MINUS_ARG", hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG),
            text="▼",
            text_font=custom_font,
            state="hidden"
        )

        self.canvas.tag_highlight["MINUS_ARG"] = self._minus_arg_step

        self.canvas.tag_highlight["PLUS_ARG"] = self._plus_arg_step
        self.canvas.tag_highlight["PLUS_ARG"] = self._plus_arg_step

    def replace(self, *args) -> None:
        pass

    def increase(self, value_added: int):
        """
        Méthode pour démarrer l'incrémentation de la quantité voulue.
        """
        self.ms = self.ms_start
        self._inc_step(value_added)

    def _inc_step(self, value_added: int):
        """
        Méthode de chaque étape d'incrémentation de la quantité voulue.
        """
        if self.canvas.is_clicking:
            self._quantity += value_added
            self.ms -= 10
            self.canvas.after(self.ms, self._inc_step, value_added)

    def reset(self):
        """
        Méthode qui remettra à 0 la quantité voulue.
        """
        self._quantity = 0

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


class QuantitySelectorSupervisor:
    def __init__(self):

        self.current_group_id = 0
