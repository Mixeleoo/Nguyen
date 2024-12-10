
from Canvas.HUDs.HUDMobileABC import HUDMobileABC
from parameter import *

class HUDMobileChooseArgRes(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.quantity_selector_arg = self.canvas.add_quantity_selector(
            self.tag, "💰 : ",
            min_quantity=0,
            max_quantity=0
        )
        self.quantity_selector_res = self.canvas.add_quantity_selector(
            self.tag, "🍴 : ",
            min_quantity=0,
            max_quantity=0
        )

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

        self.quantity_selector_arg.create(
            center_x - 40, y0_cadre + pad_from_borders
        )

        self.quantity_selector_res.create(
            center_x + 40, y0_cadre + pad_from_borders
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

        self.quantity_selector_arg.setup_before_display(max_quantity=self.canvas.jeu.joueur_actuel.argent)
        self.quantity_selector_res.setup_before_display(max_quantity=self.canvas.jeu.joueur_actuel.ressources)

        bbox = self.canvas.bbox(self.tag)

        dx = self.canvas.master.winfo_width() // 2 - (bbox[2] + bbox[0]) // 2
        dy = self.canvas.master.winfo_height() // 2 - (bbox[3] + bbox[1]) // 2

        self.canvas.move(self.tag, dx, dy)

    def imposer(self, *args):
        # self.canvas.jeu.imposer(self.hudmobile_choose_villages.selected_option)
        print(self.canvas.hudmobile_choose_taxes.hudmobile_choose_nobles.selected_option)
        print(self.canvas.hudmobile_choose_taxes.hudmobile_choose_nobles.selected_option)

    def bhide(self, *args):
        self.hide()
