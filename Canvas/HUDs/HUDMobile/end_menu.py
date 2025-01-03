
from Canvas.HUDs.HUDMobile.base import HUDMobileABC
from Canvas.Widget.StringVar import StringVar
from parameter import *

win_phrases = [
    "Ô preux chevaliers et gentes dames, qu'il soit connu en toutes contrées que la victoire éclatante illumine désormais nos bannières ! Louée soit notre bravoure !",
    "Au son des cors et des cloches, j'annonce la glorieuse victoire de nos vaillants champions. Que leur nom soit chanté pour l’éternité !",
    "D'un bras fort et d'un cœur pur, ils ont triomphé, gravant leur nom dans les récits des âges. Oyez l'histoire de leur triomphe glorieux !",
    "Que les cloches de la cité sonnent à toute volée, car aujourd’hui, le destin a couronné nos efforts !",
    "Regardez le ciel, où flotte haut la bannière victorieuse, preuve de la force et de l’honneur de nos terres !",
    "Grâce divine nous a été accordée. En ce jour béni, nous avons triomphé avec foi et sagesse !",
    "Victoire ! Victoire ! Que résonne ce cri dans chaque rue et chaque vallée, car nous avons triomphé !",
    "Rassemblez-vous au château, nobles et manants, car en ce jour glorieux, nous fêterons la victoire des braves avec festins et chants !",
    "Le champ est à nous ! Voyez, ennemis en déroute et terres conquises. La victoire est assurée, et la gloire est nôtre !",
    "En ce jour, sous le regard des cieux, la victoire fut nôtre. Que cette pierre en témoigne pour les générations à venir."
]
lose_phrases = [
    "Hélas, nobles âmes, le destin a tourné en faveur de nos ennemis. La défaite est nôtre, mais gardons l’honneur !",
    "Ô peuple fidèle, nos forces ont cédé face à l'adversité. Que ce jour sombre soit inscrit dans nos mémoires comme un appel au courage.",
    "Par le glas des cloches, nous annonçons la chute. Que nos cœurs endurent cette épreuve et se relèvent plus forts.",
    "La bannière de nos ennemis flotte sur nos terres. Replions-nous, mais ne perdons jamais espoir.",
    "Dieu en Sa sagesse n’a pas souri sur nos efforts en ce jour. Acceptons l’épreuve avec humilité et foi.",
    "Le champ de bataille est perdu, mais l’esprit des braves demeure. Rejoignez le château pour fortifier nos défenses.",
    "Nos remparts ont cédé, nos forces sont dispersées. Réunissons-nous pour panser nos blessures et préparer l’avenir.",
    "Le héraut proclame tristement : aujourd’hui, l’ennemi triomphe. Mais le feu de la vengeance brûlera à nouveau !",
    "Chant lugubre des bardes : les preux chevaliers ont combattu vaillamment, mais le sort leur fut cruel.",
    "Gravez ce jour dans vos mémoires, car il est sombre. Pourtant, de l’obscurité peut jaillir une lumière nouvelle."
]


class EndMenu(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self._text_ambience = StringVar(self.canvas)
        self._text_reason = StringVar(self.canvas)

    def create(self, geometry_width, geometry_height):

        center_x = geometry_width // 2
        center_y = geometry_height // 2

        self.canvas.create_rectangle(
            0, 0, geometry_width, geometry_height,
            fill=FILL_ACTION_BOX,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,)
        )

        custom_font = font.nametofont("TkDefaultFont").copy()
        custom_font.configure(size=18)

        self._text_ambience.id = self.canvas.create_text(
            center_x, center_y - 120,
            tags=set_tags(hud_tag=self.tag),
            fill=FILL_TEXT,
            font=custom_font
        )

        self._text_reason.id = self.canvas.create_text(
            center_x, center_y - 200,
            tags=set_tags(hud_tag=self.tag),
            fill=FILL_TEXT,
            font=custom_font
        )

        self.canvas.add_button(
            self.tag,
            "SHOW_START_MENU",
            self.hide
        ).draw(
            center_x - 60,
            center_y - 40,
            center_x + 60,
            center_y - 20,
            text="Recommencer",
            is_temp=True
        )

        self.canvas.add_button(
            self.tag,
            "QUIT",
            lambda e: self.canvas.quit()
        ).draw(
            center_x - 60,
            center_y + 20,
            center_x + 60,
            center_y + 40,
            text="Sortez-moi de là",
            is_temp=True
        )

    def replace(self, *args) -> None:
        self.canvas.tag_raise(self.tag)

    def win(self, reason: str):
        """
        Méthode lancée pour afficher le menu de fin
        :param reason: Phrase affichée pour expliquer la raison de la fin de partie
        """
        self.canvas.tag_raise(self.tag)
        self._text_reason.set(reason)
        self._text_ambience.set(choice(win_phrases))
        self.show()

    def lose(self, reason: str):
        """
        Méthode lancée pour afficher le menu de fin
        :param reason: Phrase affichée pour expliquer la raison de la fin de partie
        """
        self.canvas.tag_raise(self.tag)
        self._text_reason.set(reason)
        self._text_ambience.set(choice(lose_phrases))
        self.show()
