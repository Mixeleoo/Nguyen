
from Canvas.HUDs.HUDMobile.HUDMobileABC import HUDMobileABC
from Canvas.HUDs.StringVar import StringVar
from parameter import *


class HUDMobileChooseArgRes(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.arg_text = StringVar(self.canvas)

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

        # Effectif souhaité
        text = "Arg : 1"

        width_text = get_width_text(text)
        custom_font = font.nametofont("TkDefaultFont").copy()
        custom_font.config(size=6)

        self.arg_text.id = self.canvas.create_text(
            center_x - 20, y0_cadre + pad_from_borders, text="💰 : 0", tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,), state="hidden"
        )

        # Bouton ajouter effectif
        self.canvas.add_button(
            hud_tag=self.tag,
            func_triggered=self.plus_arg,
            trigger_name="PLUS_ARG"
        ).draw(
            center_x - 40,
            y0_cadre + pad_from_borders + 15,
            center_x - 20,
            y0_cadre + pad_from_borders + 25,
            text="▲",
            text_font=custom_font,
            state="hidden",
            is_temp=True
        )

        # Bouton retirer effectif
        self.canvas.add_button(
            hud_tag=self.tag,
            func_triggered=self.minus_arg,
            trigger_name="MINUS_ARG",
        ).draw(
            center_x - 40,
            y0_cadre + pad_from_borders + 27,
            center_x - 20,
            y0_cadre + pad_from_borders + 37,
            text="▼",
            text_font=custom_font,
            state="hidden",
            is_temp=True
        )

        self.arg_text.id = self.canvas.create_text(
            center_x + 20, y0_cadre + 10, text="🍴 : 0", tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,), state="hidden"
        )

        # Bouton ajouter effectif
        self.canvas.add_button(
            hud_tag=self.tag,
            func_triggered=self.plus_arg,
            trigger_name="PLUS_ARG"
        ).draw(
            center_x - 20 + width_text // 2,
            y0_cadre + pad_from_borders + 15,
            center_x + width_text // 2,
            y0_cadre + pad_from_borders + 25,
            text="▲",
            text_font=custom_font,
            state="hidden",
            is_temp=True
        )

        # Bouton retirer effectif
        self.canvas.add_button(
            hud_tag=self.tag,
            func_triggered=self.minus_arg,
            trigger_name="MINUS_ARG",
        ).draw(
            center_x - 20 + width_text // 2,
            y0_cadre + pad_from_borders + 27,
            center_x + width_text // 2,
            y0_cadre + pad_from_borders + 37,
            text="▼",
            text_font=custom_font,
            state="hidden",
            is_temp=True
        )

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

    def plus_arg(self, *args):
        pass

    def minus_arg(self, *args):
        pass

    def imposer(self, *args):
        # self.canvas.jeu.imposer(self.hudmobile_choose_villages.selected_option)
        print(self.canvas.hudmobile_choose_taxes.hudmobile_choose_nobles.selected_option)
        print(self.canvas.hudmobile_choose_taxes.hudmobile_choose_nobles.selected_option)

    def bhide(self, *args):
        self.hide()
