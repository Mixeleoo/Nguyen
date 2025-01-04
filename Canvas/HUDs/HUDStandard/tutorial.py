
from . import HUDStandardABC
from parameter import get_width_text, set_tags, FILL_TEXT, HEIGHT_HUD_TOP_SIDE, FILL_ACTION_BOX, TEXT_TAG, \
    WIDTH_HISTORY_HUD, HEIGHT_BOTTOM_HUD
from ...Widget.StringVar import StringVar

class Tutorial(HUDStandardABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self._rect_id = 0
        self._text = StringVar(self.canvas)
        self._tutorial_index = 0

    def create(self) -> None:

        width = get_width_text("salut comment ça va ")
        height = 20

        x0_cadre = 0
        y0_cadre = 0
        x1_cadre = width
        y1_cadre = height

        self._rect_id = self.canvas.create_rectangle(
            x0_cadre, y0_cadre,
            x1_cadre, y1_cadre,
            tags=set_tags(trigger_tag="NEXTTUTORIAL", hud_tag=self.tag),
            fill=FILL_ACTION_BOX,
            state="hidden"
        )

        self.canvas.tutoriel_mode_tag_foc["NEXTTUTORIAL"] = self.next

        self._text.id = self.canvas.create_text(
            (x0_cadre + x1_cadre) // 2, (y0_cadre + y1_cadre) // 2,
            tags=set_tags(hud_tag=self.tag) + (TEXT_TAG,),
            fill=FILL_TEXT,
            state="hidden",
            justify="center"
        )

        self.canvas.text_id_in_rectangle_id[self._text.id] = self._rect_id

    def replace(self, x: int, y: int, text: str) -> None:
        width_text = get_width_text(text)
        height_text = len(text.split("\n")) * 30
        self._text.set(text)

        self.canvas.coords(self._rect_id, x - width_text // 2, y - height_text // 2, x + width_text // 2, y + height_text // 2)
        self.canvas.coords(self._text.id, x, y)

    def show(self, x: int, y: int, text: str): super().show(x, y, text)

    def next(self, *args):
        # Explique l'HUD top_side
        self_bbox = self.bbox()

        if self._tutorial_index == 0:
            self.show(self.canvas.winfo_width() // 2, HEIGHT_HUD_TOP_SIDE + 40, "Voilà l'HUD qui affiche vos informations\nCliquez-moi dessus pour continuer")

        elif self._tutorial_index == 1:
            self.show(self.canvas.winfo_width() - WIDTH_HISTORY_HUD * 2, self.canvas.winfo_height() // 2, "Ici voici l'historique,\nil vous permettra de suivre les actions de vos adversaires \n(et des votres si vous êtes perdu)")

        elif self._tutorial_index == 2:
            self.show(self.canvas.winfo_width() // 3, self.canvas.winfo_height() - HEIGHT_BOTTOM_HUD * 2, "Ici sont disposées vos actions sous forme de page.\nIl y a 6 actions, reparties sur 3 pages.\nLes détails des coûts des actions sont également affichés.")

        elif self._tutorial_index == 3:
            self.canvas.hud_event.show_animation()
            bbox = self.canvas.hud_event.bbox()
            self.show(self.canvas.winfo_width() // 2, bbox[3] + HEIGHT_HUD_TOP_SIDE * 2, "Ici est l'HUD qui affichera les évènements qui se produiront en début de chaque tour.\nPlus d'informations sont expliquées sur le bouton \"i\"")

        elif self._tutorial_index == 4:
            self.canvas.hud_event.hide_animation()
            self.show(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, "Vous avez tout le savoir nécessaire pour jouer à ce \"jeu\".\nBon courage (sincèrement)")

        else:
            self.canvas.game_mode = "basic"
            self.hide()
            self._tutorial_index = -1

        self._tutorial_index += 1
