from Canvas.HUDs.HUDMobile.HUDMobileABC import HUDMobileABC
from Canvas.Widget.StringVar import StringVar
from parameter import *

class HUDMobileChooseArgRes(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.amount_arg = 0
        self.arg_text = StringVar(self.canvas)

        self.amount_res = 0
        self.res_text = StringVar(self.canvas)

        self.starting_ms = 500
        self.ms = 500

    @property
    def tag(self):
        return "HUDMobileChooseArgRes"

    def create(self, *args):

        width = 300
        height = 100

        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = y0_cadre + width
        y1_cadre = y0_cadre + height

        center_x = (x0_cadre + x1_cadre) // 2

        self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre, fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,), state="hidden"
        )

        custom_font = font.nametofont("TkDefaultFont").copy()
        custom_font.config(size=6)

        # TODO Créer un nouveau Widget QuantiySelector

        self.arg_text.id = self.canvas.create_text(
            center_x - 20, y0_cadre + pad_from_borders,
            text=f"💰 : {self.amount_arg}",
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden",
            fill=FILL_TEXT
        )

        # Bouton ajouter effectif
        self.canvas.create_text_in_rectangle(
            center_x - 35,
            y0_cadre + pad_from_borders + 15,
            center_x - 15,
            y0_cadre + pad_from_borders + 25,
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
            center_x - 35,
            y0_cadre + pad_from_borders + 27,
            center_x - 15,
            y0_cadre + pad_from_borders + 37,
            rectangle_tags=set_tags(highlight_tag="MINUS_ARG", hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG),
            text="▼",
            text_font=custom_font,
            state="hidden"
        )

        self.canvas.tag_highlight["MINUS_ARG"] = self._minus_arg_step

        self.res_text.id = self.canvas.create_text(
            center_x + 20, y0_cadre + pad_from_borders,
            text=f"🍴 : {self.amount_res}",
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden",
            fill=FILL_TEXT
        )

        # Bouton ajouter effectif
        self.canvas.create_text_in_rectangle(
            center_x + 15,
            y0_cadre + pad_from_borders + 15,
            center_x + 35,
            y0_cadre + pad_from_borders + 25,
            rectangle_tags=set_tags(highlight_tag="PLUS_RES", hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG),
            text="▲",
            text_font=custom_font,
            state="hidden",
        )

        self.canvas.tag_highlight["PLUS_RES"] = self._plus_res_step

        # Bouton retirer effectif
        self.canvas.create_text_in_rectangle(
            center_x + 15,
            y0_cadre + pad_from_borders + 27,
            center_x + 35,
            y0_cadre + pad_from_borders + 37,
            rectangle_tags=set_tags(highlight_tag="MINUS_RES", hud_tag=self.tag) + (TEMP_TAG,),
            text_tags=set_tags(hud_tag=self.tag) + (TEXT_TAG, TEMP_TAG,),
            text="▼",
            text_font=custom_font,
            state="hidden"
        )

        self.canvas.tag_highlight["MINUS_RES"] = self._minus_res_step

        # Bouton OK qui lance l'immigration
        self.canvas.create_ok_button(
            x1_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.imposer, is_temp=True, state="hidden"
        )

        # Bouton Annuler qui annule l'immigration
        self.canvas.create_cancel_button(
            x0_cadre, y1_cadre, hud_tag=self.tag, func_triggered=self.bhide, is_temp=True, state="hidden"
        )

    def replace(self, *args) -> None:

        bbox = self.canvas.bbox(self.tag)

        dx = self.canvas.master.winfo_width() // 2 - (bbox[2] + bbox[0]) // 2
        dy = self.canvas.master.winfo_height() // 2 - (bbox[3] + bbox[1]) // 2

        self.canvas.move(self.tag, dx, dy)

    def _minus_arg_step(self):
        if self.canvas.is_clicking:
            self.amount_arg -= 1 if self.amount_arg - 1 > 0 else 0
            self.arg_text.set(f"💰 : {self.amount_arg}")
            self.ms -= 10 if self.ms - 10 > 10 else 0

            self.canvas.after(self.ms, self._minus_arg_step)

        else:
            self.ms = self.starting_ms

    def _plus_arg_step(self):
        if self.canvas.is_clicking:
            self.amount_arg += 1 if self.amount_arg + 1 <= self.canvas.jeu.joueur_actuel.argent else 0
            self.arg_text.set(f"💰 : {self.amount_arg}")
            self.ms -= 10 if self.ms - 10 > 10 else 0

            self.canvas.after(self.ms, self._minus_arg_step)

        else:
            self.ms = self.starting_ms

    def _minus_res_step(self):
        if self.canvas.is_clicking:
            self.amount_res -= 1 if self.amount_res - 1 > 0 else 0
            self.res_text.set(f"🍴 : {self.amount_res}")
            self.ms -= 10 if self.ms - 10 > 10 else 0

            self.canvas.after(self.ms, self._minus_res_step)

        else:
            self.ms = self.starting_ms

    def _plus_res_step(self):
        if self.canvas.is_clicking:
            self.amount_res += 1 if self.amount_res + 1 <= self.canvas.jeu.joueur_actuel.ressources else 0
            self.res_text.set(f"🍴 : {self.amount_res}")
            self.ms -= 10 if self.ms - 10 > 10 else 0

            self.canvas.after(self.ms, self._plus_res_step)

        else:
            self.ms = self.starting_ms

    def imposer(self, *args):
        # self.canvas.jeu.imposer(self.hudmobile_choose_villages.selected_option)
        print(self.canvas.hudmobile_choose_taxes.hudmobile_choose_nobles.selected_option)
        print(self.canvas.hudmobile_choose_taxes.hudmobile_choose_nobles.selected_option)

    def bhide(self, *args):
        self.hide()
