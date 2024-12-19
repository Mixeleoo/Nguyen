from collections import namedtuple
# -*- coding: utf-8 -*-

from random import randint, choice
from tkinter import font

MAX_WIDTH = 1024
MAX_HEIGHT = 600

CARRE_PAR_LIGNE = 60
CARRE_PAR_COLONNE = 40
SPS = 25

# nombre maximum de choix de villages pour changer de page
RBTN_MAX_VIL = 2

HEIGHT_HUD_TOP_SIDE = 60
HEIGHT_BOTTOM_HUD = 80
HEIGHT_EVENT = 50

PADY_BOTTOM_HUD = 5
PADX_BOTTOM_HUD = 5
SIZE_ACTION_ADDITIONAL_COST_TEXT = 12

PADY_BUILD_CITY_HUD = 5 + HEIGHT_HUD_TOP_SIDE
PADY_BUILD_CITY_HUD_HIDING = -20 + HEIGHT_HUD_TOP_SIDE

WIDTH_HISTORY_HUD = 150

PA = 10

DELTA_MS_ANIMATION = 1000 // 60  # 1000 ms = 1s / 60 (pour avoir 60 images par secondes)

# UNIQUEMENT POUR LES TESTS
NB_NOBLE_AU_DEPART = 4

# RIEN
NOTHING_TAG = "NOTHING"

# Hiérarchie MAP
MAP_TAG = "MAP"
PLAINE_TAG = "PLAIN"
FOREST_TAG = "FOREST"
MOUNTAIN_TAG = "MOUNTAIN"
LAKE_TAG = "LAKE"
VILLAGE_TAG = "VILLAGE"

# Tas de tag MAP
MAP_SQUARE_TOP_LEFT_TAG = "map_square_top_left"
MAP_SQUARE_BOTTOM_RIGHT_TAG = "map_square_bottom_right"

# Highlight tags
CLICKABLE_TAG = "CLICKABLE"
TOGGLEABLE_TAG = "TOGGLEABLE"
DRAGGABLE_TAG = "DRAGGABLE"
HIGHLIGHT_BUTTON_TAG = "HIGHLIGHT_BUTTON"

# Tas de tags HUDs
TEXT_TAG = "TEXT"
HISTORY_TEXT = "HISTORY_TEXT"
TEMP_TAG = "TEMP"

# Tag qui trigger les fonctions appropriées
MORE_INFO_TAG = "MORE_INFO"
CHANGE_PAGE_MINUS = "CPM"
CHANGE_PAGE_PLUS = "CPP"
SHOW_OR_HIDE_PAGE_TAG = "SHOW_OR_HIDE_PAGE"
SHOW_OR_HIDE_HISTORY_TAG = "SHOW_OR_HIDE_HISTORY"
SCROLLBAR_TAG = "SCROLLBAR_TAG"
RECTANGLE_ACTION = "RECTANGLE_ACTION"
BUILD_CITY = "BUILD_CITY"
BUILD_CHURCH = "BUILD_CHURCH"
PLUS_IMMIGRANTS_TAG = "ADD_IMMIGRANTS"
MINUS_IMMIGRANTS_TAG = "MINUS_IMMIGRANTS"
INFO_EVENT_TAG = "INFO_EVENT"
PAYSAN_OR_ARTISAN_TAG = "PAYSAN_OR_ARTISAN"
TAXES_TAG = "TAXES"
VASSALIZE_TAG = "VASSALIZE"
WAR_TAG = "WAR"

OPEN_WINDOW_TAG = "OPEN_WINDOW"

# si
si = 'si'

# Coûts des actions en fonction de leurs tag
ACTIONS_TAG_COST = {
    PAYSAN_OR_ARTISAN_TAG: 0,
    BUILD_CHURCH: 6,
    VASSALIZE_TAG: 4,
    BUILD_CITY: 8,
    TAXES_TAG: 5,
    WAR_TAG: 8
}

# LES ACTIONS SONT DANS L'ORDRE SUIVANT : DE GAUCHE A DROITE **PUIS** DE HAUT EN BAS
ACTION_FOR_YOUR_TURN = [
    {
        "text": "Agrandir population",
        "PA": "1-10 PA",
        "additionalcost": "0-40, 0-40 res",
        "do": PAYSAN_OR_ARTISAN_TAG
    },
    {
        "text": "Construire une église",
        "PA": f"{ACTIONS_TAG_COST[BUILD_CHURCH]} PA",
        "additionalcost": "100 arg, 50 res",
        "do": BUILD_CHURCH
    },
    {
        "text": "Vassaliser",
        "PA": f"{ACTIONS_TAG_COST[VASSALIZE_TAG]} PA",
        "additionalcost": "Y arg, Z res",
        "do": VASSALIZE_TAG
    },
    {
        "text": "Construire un village",
        "PA": f"{ACTIONS_TAG_COST[BUILD_CITY]} PA",
        "additionalcost": "300 arg, 150 res",
        "do": BUILD_CITY
    },
    {
        "text": "Impôt",
        "PA": f"{ACTIONS_TAG_COST[TAXES_TAG]} PA",
        "additionalcost": "",
        "do": TAXES_TAG
    },
    {
        "text": "Déclarer la guerre",
        "PA": f"{ACTIONS_TAG_COST[WAR_TAG]} PA",
        "additionalcost": "100 res",
        "do": WAR_TAG
    }
]
NB_ACTIONS = len(ACTION_FOR_YOUR_TURN)
NB_ACTION_PER_PAGE = 2

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def mountain_color():
    a = randint(120, 200)
    return rgb_to_hex(a, a, a)

couleurs = {
    PLAINE_TAG: lambda: rgb_to_hex(randint(63, 139), randint(200, 230), randint(17, 114)),
    FOREST_TAG: lambda: rgb_to_hex(randint(20, 50), randint(120, 150), randint(20, 50)),
    MOUNTAIN_TAG: mountain_color,
    LAKE_TAG: lambda: rgb_to_hex(randint(50 , 127), randint(144, 160), 255)
}

FILL_TEXT = "#CCCCCC"

FILL_ACTION_BOX = "#333333"
FILL_CANCEL = "#BA0A0A"
FILL_OK = "#1C6203"
FILL_INFO = "#266CB6"

fill_brighter = {
    FILL_ACTION_BOX: "#514E4E",
    FILL_CANCEL: "#DB4E4E",
    FILL_OK: "#278E02",
    FILL_INFO: "#5397E0"
}

fill_darker = {
    FILL_ACTION_BOX: "#272626",
}


HIGHLIGHT_TAG_INDEX = 0
TRIGGER_TAG_INDEX = 1
DRAG_TAG_INDEX = 2
COLOR_TAG_INDEX = 3
HUD_TAG_INDEX = 4
GROUP_TAG_INDEX = 5

def set_tags(highlight_tag=NOTHING_TAG, trigger_tag=NOTHING_TAG, drag_tag=NOTHING_TAG,
             color_tag=FILL_ACTION_BOX, hud_tag=NOTHING_TAG, group_tag=""):
    """
    Méthode qui sert à uniformiser tous les éléments du canvas, ils ont tous comme tags ceux en paramètres.

    :param highlight_tag: Le tag déterminant ce qui est trigger lors du clic gauche (généralement le feedback).
    :param trigger_tag: Le tag déterminant ce qui est trigger lors du clic gauche confirmé (= après relâchement sans mouvement de la souris entre le clic et le relâchement).
    :param drag_tag: Le tag déterminant ce qui est trigger lors du drag clic gauche.
    :param color_tag: Le tag déterminant la couleur d'origine (sert pour remettre la couleur d'origine après un highlight)
    :param hud_tag: Le tag déterminant l'HUD auquel appartient l'élément.
    :param group_tag: Le tag déterminant l'éventuel groupe auquel appartient l'élément (sert dans le cas de comportements spécifiques).
    :return: Tous les tags avec une valeur par défaut
    """
    return highlight_tag, trigger_tag, drag_tag, color_tag, hud_tag, group_tag

pad_from_borders = 15

def get_width_text(text: str):

    # On récupère la font de base pour calculer la taille des rectangles
    text_font = font.nametofont("TkDefaultFont")

    # Mesurer la largeur et la hauteur du texte
    # Ici, ajout d'un pad sur la largeur pour éviter d'avoir un rectangle PARFAITEMENT à la largeur du texte
    return text_font.measure(text) + pad_from_borders


def separer_chaine_sans_couper(chaine, n):
    # Vérifie que n est un entier positif
    if n <= 0:
        raise ValueError("n doit être un entier positif non nul")

    # Cas où n == 1 : toute la chaîne dans un seul segment
    if n == 1:
        return chaine.strip()

    # Calcul de la longueur d'un segment approximatif
    segment_length = len(chaine) // n
    if segment_length == 0:
        raise ValueError("n est trop grand par rapport à la longueur de la chaîne.")

    # Liste pour stocker les segments
    segments = []
    segment = ""

    # Parcours des mots
    for mot in chaine.split():
        # Ajoute le mot si le segment ne dépasse pas la longueur cible
        if len(segment) + len(mot) + 1 <= segment_length:
            segment += (mot + " ")
        else:
            # Ajoute le segment terminé à la liste et démarre un nouveau
            segments.append(segment.strip())
            segment = mot + " "

    # Ajoute le dernier segment
    if segment:
        segments.append(segment.strip())

    # Assemble les segments avec "\n"
    return '\n'.join(segments)


Position = namedtuple('Position', ['x', 'y'])

noms_village = [
    "Lande-Cendrée",
    "Bois-Ruiné",
    "Gorgemort",
    "Ombrecombe",
    "Rochebrèche",
    "Val-Silencieux",
    "Tertre-Vaillant",
    "Creux-du-Déchu",
    "Abîmeclair",
    "Couronne-Froide",
    "Haute-Désolation",
    "Fosse-du-Purgé",
    "Larmes-Grises",
    "Tourbe-Sombre",
    "Havre-Funèbre",
    "Sépultroc",
    "Pointe-Flétrie",
    "Nécroval",
    "Cime-Morne",
    "Pierrefeu",
    "Flammecreuse",
    "Aube-Délétère",
    "Brise-Ombre",
    "Chant-du-Vide",
    "Fanal-Terreux",
    "Ravin-Spectral",
    "Monts-Saignants",
    "Graviombre",
    "Givreclair",
    "Linceul-de-Vers",
    "Halte-Pâle",
    "Grondeval",
    "Terre-Fumante",
    "Veine-Sanguine",
    "Pic-du-Vernis",
    "Grotte-des-Lamentations",
    "Vent-Glacial",
    "Clairière-Creuse",
    "Failles-Grondantes",
    "Rive-Austère",
    "Fort-Plaie",
    "Brasier-Cinéraire",
    "Cœur-Brisé",
    "Plaine-Hurlante",
    "Bastion-Froid",
    "Détroit-du-Malheur",
    "Aiguilles-Mortelles",
    "Hauts-Rendus",
    "Lac-Sépia",
    "Fond-du-Désespoir"
]

def nom_aleatoire_village():
    return choice(noms_village)

prenoms_perso = [ "Alaric", "Béranger", "Adélaïde", "Eudes", "Clotilde", "Léonard", "Ysabeau", "Godefroy", "Agnès", "Hugues",
    "Géraldine", "Baudoin", "Armand", "Isabeau", "Aimé", "Perrin", "Tanguy", "Clothilde", "Florent", "Sygarde",
    "Gildas", "Théodora", "Renaud", "Béatrice", "Geoffroy", "Hildegarde", "Roland", "Mathilde", "Thierry", "Gertrude",
    "Bernard", "Edwige", "Louis", "Aubrée", "Gérald", "Renée", "Frédéric", "Alix", "Frédérique", "Foulques",
    "Hélène", "Henri", "Aude", "Mathieu", "Judith", "Galeran", "Constance", "Géraud", "Solange", "Renaude",
    "Esteban", "Eustache", "Brunehaut", "Déodat", "Lancelot", "Lison", "Eléonore", "Sénéchal", "Aldegarde", "Béatrice",
    "Térence", "Iseult", "Roger", "Pépin", "Blanche", "Godefroy", "Tiberius", "Hildebrand", "Eadric", "Sigismond",
    "Gaétane", "Éléonore", "Thibault", "Isolde", "Géron", "Luce", "Guy", "Sibylle", "Bertrand", "Mathurin",
    "Lothaire", "Théodore", "Hermenegilde", "Aldric", "Adeline", "Justine", "Yvain", "Guibert", "Pétronille", "Floriane",
    "Valérie", "Ulric", "Adhémar", "Bérengère", "Gauthier", "Adalbert", "Lambert", "Gervais", "Clovis", "Eugénie",
    "Héribert", "Philomène", "Mathias", "Frédégonde", "Hildegarde", "Édouard", "Pétronille", "Arsène", "Carlotta", "Geoffroy",
    "Aldebert", "Aymon", "Béna", "Géraldine", "Alvéran", "Théophane", "Maud", "Roland", "Odilon", "Arnaud",
    "Adèle", "Maïeul", "Cécile", "Thierry", "Milburge", "Madeleine", "Hildegarde", "Olivier", "Rémacle", "Hélier",
    "Hélène", "Eberhard", "Côme", "Eustache", "Éva", "Grégoire", "Aimée", "Fulbert", "Agnès", "Baudouin",
    "Désiré", "Arnould", "Sybille", "Agathe", "Enguerrand", "Yvette", "Roderick", "Ivo", "Guillaume", "Otton",
    "Léon", "Claire", "Dido", "Ernestine", "Clément", "Irène", "Gauthier", "Béatrix", "Anselme", "Godefroy",
    "Quentin", "Madeleine", "Liévin", "Olric", "Odon", "Géraud", "Venance", "Alix", "Eloise", "Engelbert",
    "Gauthier", "Raoul", "Théobald", "Perrine", "Ethelred", "Gisèle", "Mathilde", "Thierry", "François", "Orabel",
    "Sigismond", "Léonidas", "Godfrey", "Alice", "Audebert", "Romain", "Berthe", "André", "Maurin", "Agnès",
    "Godefroy", "Norbert", "Millicent", "Eulalie", "Bertrade", "Hermenegilde", "Louis", "Gilbert", "Beatrix", "Gildas"]

def prenom_aleatoire() :
    return choice(prenoms_perso)

noms_eglises = [
    "Église Saint-Pierre",
    "Église Notre-Dame",
    "Église Sainte-Marie",
    "Église Saint-Jean-Baptiste",
    "Église Saint-Paul",
    "Église Saint-Louis",
    "Église Saint-Augustin",
    "Église Saint-Antoine",
    "Église Sainte-Catherine",
    "Église Saint-Joseph",
    "Église Saint-François",
    "Église Saint-André",
    "Église Sainte-Thérèse",
    "Église Saint-Honoré",
    "Église Saint-Sulpice",
    "Église Sainte-Claire",
    "Église Saint-Denis",
    "Église Saint-Alexandre",
    "Église Sainte-Anne",
    "Église Saint-Michel",
    "Église Saint-Roch",
    "Église Sainte-Rita",
    "Église Saint-Étienne",
    "Église Sainte-Élisabeth",
    "Église Saint-Jean-de-Latran",
    "Église Saint-Martin",
    "Église Sainte-Bernadette",
    "Église Saint-Benoît",
    "Église Saint-Marc",
    "Église Sainte-Madeleine",
    "Église Saint-Basile",
    "Église Saint-Hubert",
    "Église Saint-Pierre-et-Saint-Paul",
    "Église Sainte-Véronique",
    "Église Saint-Augustin-de-Canterbury",
    "Église Saint-Jean-de-Dieu",
    "Église Saint-Cyr",
    "Église Sainte-Victoire",
    "Église Saint-Hélier",
    "Église Saint-Léon",
    "Église Sainte-Famille",
    "Église Saint-Georges",
    "Église Saint-Jacques",
    "Église Sainte-Rose",
    "Église Saint-Nicolas",
    "Église Sainte-Marthe",
    "Église Saint-Jean-Eudes",
    "Église Saint-Étienne-de-Montluc",
    "Église Saint-Dominique",
    "Église Saint-Louis-de-Gonzague",
    "Église Saint-Alban"
]

def nom_aleatoire_eglise() :
    return choice(noms_eglises)

noms_pretres = [
    "Père Augustin",
    "Père Bernard",
    "Père Thomas",
    "Père François",
    "Père Dominique",
    "Père Anselme",
    "Père Bonaventure",
    "Père Grégoire",
    "Père Pierre",
    "Père Benoît",
    "Père Grégoire",
    "Père Jean",
    "Père Athanase",
    "Père Jérôme",
    "Père Ignace",
    "Père Cyprien",
    "Père Hilaire",
    "Père Ambroise",
    "Père Léon",
    "Père Isidore",
    "Père Martine",
    "Père Nicolas",
    "Père Jean",
    "Père François",
    "Père Pierre",
    "Père Vincent",
    "Père Louis",
    "Père Clément",
    "Père Polycarpe",
    "Père Ephrem",
    "Père Fulgence",
    "Père Augustin",
    "Père Grégoire",
    "Père Firmin",
    "Père Remi",
    "Père Évode",
    "Père Richard",
    "Père Wenceslas",
    "Père Thomas",
    "Père Boniface",
    "Père Lambert",
    "Père Gérard",
    "Père Hyacinthe",
    "Père Albin",
    "Père Martin",
    "Père Gaudentius",
    "Père Jean",
    "Père Théodore",
    "Père Basil",
    "Père Sévérin"
]

def nom_aleatoire_pretres() :
    return choice([noms_pretres])

noms_nobles =[
    "Sir Guillaume",
    "Dame Éléonore",
    "Duc Geoffroy",
    "Comtesse Isabelle",
    "Baron Robert",
    "Seigneur Richard",
    "Princesse Béatrice",
    "Sir Henri",
    "Dame Marguerite",
    "Vicomte Gilbert",
    "Duchesse Agnès",
    "Baronne Catherine",
    "Seigneur Thomas",
    "Comte Baudouin",
    "Princesse Alice",
    "Duc Philippe",
    "Dame Mathilde",
    "Sir Bertrand",
    "Comtesse Marie",
    "Seigneur Hugues",
    "Baronne Alice",
    "Sir Eustache",
    "Duchesse Jeanne",
    "Seigneur Édouard",
    "Comtesse Blanche",
    "Baron Guillaume",
    "Dame Cécile",
    "Duc Édouard",
    "Sir Thomas",
    "Princesse Hélène",
    "Seigneur Alexandre",
    "Comtesse Éléonore",
    "Baron Richard",
    "Duchesse Mathilde",
    "Sir Jean",
    "Dame Isabelle",
    "Vicomte Robert",
    "Duc Henri",
    "Comtesse Sibylle",
    "Seigneur Simon",
    "Princesse Marguerite",
    "Baronne Jeanne",
    "Sir Robert",
    "Duchesse Agnès",
    "Dame Alice",
    "Comtesse Jeanne",
    "Seigneur Raymond",
    "Baronne Isabelle",
    "Sir Guy"]

def nom_aleatoire_nobles() :
    return choice([noms_nobles])

# Quantité de ressources associée au type de terre sur la carte
capacite_prod_terre = {"PLAIN" : 7, "MOUNTAIN" : 2, "LAKE" : 5, "FOREST" : 9}

def dummy(*args):
    pass