
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
        self._tutorial_list = [
            lambda: self.show(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, "Bienvenue dans notre jeu.\nPour suivre ce tutoriel, veuillez me cliquer dessus."),
            lambda: self.show(self.canvas.winfo_width() // 2, HEIGHT_HUD_TOP_SIDE + 40, "Voilà l'HUD qui affiche vos informations."),
            lambda: self.show(self.canvas.hud_top_side.get_abscissa_square(0) + 50, HEIGHT_BOTTOM_HUD * 1.5, "Ici sont vos PA (ou point d'actions)."),
            lambda: self.show(self.canvas.hud_top_side.get_abscissa_square(1), HEIGHT_BOTTOM_HUD * 1.5, "Ici sont vos écus."),
            lambda: self.show(self.canvas.hud_top_side.get_abscissa_square(2), HEIGHT_BOTTOM_HUD * 1.5, "Ici sont vos ressources."),
            lambda: self.show(self.canvas.hud_top_side.get_abscissa_square(3), HEIGHT_BOTTOM_HUD * 1.5, "Ici est le bonheur global de tous vos villages."),
            lambda: self.show(self.canvas.hud_top_side.get_abscissa_square(4), HEIGHT_BOTTOM_HUD * 1.5, "Ici est la population globale de tous vos villages."),
            lambda: self.show(self.canvas.hud_top_side.get_abscissa_square(5), HEIGHT_BOTTOM_HUD * 1.5, "Ici est l'effectif de votre armée."),
            lambda: self.show(self.canvas.hud_top_side.get_abscissa_square(6) - 60, HEIGHT_BOTTOM_HUD * 1.5, "Ici est le nombre de noble\nqu'il reste à vaincre."),
            lambda: self.show(self.canvas.winfo_width() - WIDTH_HISTORY_HUD * 2, self.canvas.winfo_height() // 2, "Ici voici l'historique.\nIl vous permettra de suivre les actions de vos adversaires \n(et des votres si vous êtes perdu)"),
            lambda: self.show(self.canvas.winfo_width() - WIDTH_HISTORY_HUD * 2, self.canvas.winfo_height() - HEIGHT_BOTTOM_HUD * 2, "En bas à droite est le bouton de fin de tour.\nÀ utiliser avec précaution."),
            lambda: self.show(self.canvas.winfo_width() // 3, self.canvas.winfo_height() - HEIGHT_BOTTOM_HUD * 2, "Ici sont disposées vos actions sous forme de page.\nIl y a 6 actions, reparties sur 3 pages.\nLes détails des coûts des actions sont également affichés."),
            lambda: self.show(self.canvas.winfo_width() // 4, self.canvas.winfo_height() - HEIGHT_BOTTOM_HUD * 2, "Agrandir population sert à, comme son nom l'indique,\nagrandir la population d'un village"),
            self._agrandir_population,
            lambda: self.show(self.canvas.winfo_width() // 3, self.canvas.winfo_height() - HEIGHT_BOTTOM_HUD * 2 - 60, "Construire une église dans un village permet, à chaque début de tour,\nd'appliquer un don aléatoire sur un de vos villageois.\nLes dons sont :\n- Bonus de bonheur.\n- Bonus d'espérance de vie.\n- Bonus de capacité de production."),
            self._vassaliser,
            self._imposer,
            self._build_city,
            self._build_church,
            self._event,
            self._end
        ]

    def create(self, *args) -> None:

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
            justify="left"
        )

        self.canvas.text_id_in_rectangle_id[self._text.id] = self._rect_id

    def replace(self, x: int, y: int, text: str) -> None:
        width_text = get_width_text(text)
        height_text = len(text.split("\n")) * 28
        self._text.set(text)

        self.canvas.coords(self._rect_id, x - width_text // 2, y - height_text // 2, x + width_text // 2, y + height_text // 2)
        self.canvas.coords(self._text.id, x, y)

    def show(self, x: int, y: int, text: str): super().show(x, y, text)

    def next(self, *args):
        # Explique l'HUD top_side

        self.canvas.tag_raise(self.tag)

        if self._tutorial_index < len(self._tutorial_list):
            self._tutorial_list[self._tutorial_index]()

        else:
            self.canvas.game_mode = "basic"
            self.hide()
            self._tutorial_index = -1

        self._tutorial_index += 1

    def _agrandir_population(self):
        self.canvas.hudmobile_choose_type_villager.show()
        bbox = self.canvas.hudmobile_choose_type_villager.bbox()
        self.show(
            (bbox[0] + bbox[2]) // 2, (bbox[3] + bbox[1]) // 2 - 140,
            "Vous aurez comme choix:\n"
            "- Paysan (villageois qui démarre sans économies)\n"
            "- Artisan (villageois qui démarre avec économies)\n"
            "- Soldat (n'est pas un villageois)"),

    def _vassaliser(self):
        self.canvas.hud_actions.next_page()
        self.canvas.hud_actions.change_page()
        self.show(
            self.canvas.winfo_width() // 4, self.canvas.winfo_height() - HEIGHT_BOTTOM_HUD * 2 - 60,
            "Vassaliser un noble sert à le mettre sous vos ordres.\n"
            "C'est à dire que :\n"
            "- Il vous accompagnera lui ainsi que ses soldats à la guerre.\n"
            "- Il ne pourra plus faire la guerre de lui-même.\n"
            "- Vous pourrez le soumettre à l'impôt.\n"
            "Notez que si ce noble refuse, une guerre éclate."
        )

    def _imposer(self):
        self.canvas.hud_actions.next_page()
        self.canvas.hud_actions.change_page()
        self.show(
            self.canvas.winfo_width() // 3, self.canvas.winfo_height() - HEIGHT_BOTTOM_HUD * 2 - 20,
            "Vous pouvez soumettre à l'impôt vos nobles et vos villages.\nCependant cela les rend malheureux.\n"
            "Notez que si vos villageois sont trop malheureux, une révolte peut éclater."
        )

    def _build_city(self):
        self.canvas.hud_build_city.show_animation()
        bbox = self.canvas.hud_event.bbox()
        self.show(self.canvas.winfo_width() // 2, bbox[3] + HEIGHT_HUD_TOP_SIDE * 2,
          "Ici est l'HUD qui vous indique que vous êtes en mode construction de village.")

    def _build_church(self):
        self.canvas.hud_build_city.hide_animation()
        self.canvas.hud_build_church.show_animation()
        bbox = self.canvas.hud_event.bbox()
        self.show(self.canvas.winfo_width() // 2, bbox[3] + HEIGHT_HUD_TOP_SIDE * 2,
          "Ici est l'HUD qui vous indique que vous êtes en mode construction d'église.")

    def _event(self):
        self.canvas.hud_build_church.hide_animation()
        self.canvas.hud_event.show_animation()
        bbox = self.canvas.hud_event.bbox()
        self.show(self.canvas.winfo_width() // 2, bbox[3] + HEIGHT_HUD_TOP_SIDE * 2,
          "Ici est l'HUD qui affichera les évènements qui se produiront en début de chaque tour.\nPlus d'informations sont expliquées sur le bouton \"i\"\nen haut à droite du parchemin.")

    def _end(self):
        self.canvas.hud_event.hide_animation()
        self.show(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2,
          "Si vous vous sentez submergés, vous pouvez retirer tous les HUD avec le clic droit.\nVous avez tout le savoir nécessaire pour jouer à ce \"jeu\".\nBon courage,\n\nAmitiés distinguées, les développeurs.")


