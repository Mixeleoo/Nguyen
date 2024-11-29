
from random import randint, choice
from tkinter import font

MAX_WIDTH = 1024
MAX_HEIGHT = 600

CARRE_PAR_LIGNE = 60
CARRE_PAR_COLONNE = 40
SPS = 25

HEIGHT_HUD_TOP_SIDE = 60

HEIGHT_BOTTOM_HUD = 80
PADY_BOTTOM_HUD = 5
PADX_BOTTOM_HUD = 5
SIZE_ACTION_ADDITIONAL_COST_TEXT = 8

PADY_BUILD_CITY_HUD = 5 + HEIGHT_HUD_TOP_SIDE
PADY_BUILD_CITY_HUD_HIDING = -20 + HEIGHT_HUD_TOP_SIDE

HIGHLIGHT_TAG_INDEX = 0
TRIGGER_TAG_INDEX = 1
DRAG_TAG_INDEX = 2
COLOR_TAG_INDEX = 3
HUD_TAG_INDEX = 4
GROUP_TAG_INDEX = 5

PA = 10

DELTA_MS_ANIMATION = 1000 // 60  # 1000 ms = 1s / 60 (pour avoir 60 images par secondes)

# UNIQUEMENT POUR LES TESTS
NB_NOBLE_AU_DEPART = 4

"""
Sans hiérarchie des tags, il est plus fastidieux de savoir quel élément se comporte comment, alors qu'avec une hiérarchie,
    on peut regrouper certains comportements, comme le comportement des clickable par exemple, qui auront leur fonction pour
    les mettre en surbrillance

Hiérarchie des tags:
                                                      HUD_TAG
                                      NOTHING_TAG     TEXT_TAG     CLICKABLE_TAG
                                                  _{id_rectangle}  {tag_function_triggered}
                                            
                                            
                                            
                                                       MAP_TAG
                                PLAINE_TAG FOREST_TAG MOUNTAIN_TAG LAKE_TAG VILLAGE_TAG
                                
Tags sans hiérarchie (placés à la fin) :
MAP_SQUARE_TOP_LEFT_TAG
MAP_SQUARE_BOTTOM_RIGHT_TAG
HUD_BOTTOM
HUD_RIGHT_SIDE
HISTORY_TEXT
TEXT_PAGE
TEXT_ACTION
TEMP_TAG
"""

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

# Tas de tags HUD
TEXT_TAG = "TEXT"
HUD_BOTTOM = "HUD_BOTTOM"
HUD_RIGHT_SIDE = "HUD_RIGHT_SIDE"
HUD_BUILD_CITY = "HUD_BUILD_CITY"
HUD_BUILD_CHURCH = "HUD_BUILD_CHURCH"
HUD_EVENT = "HUD_EVENT"
HUD_TOP_SIDE = "HUD_TOP_SIDE"
HISTORY_TEXT = "HISTORY_TEXT"
TEXT_PAGE = "TEXT_PAGE"
TEXT_NB_IMMIGRANTS = "TEXT_NB_IMMIGRANTS"
TEXT_ACTION = "TEXT_ACTION"
TEMP_TAG = "TEMP"
TEMP_YAUNVILLAGEICIGROS_TAG = "TEMP_YAUNVILLAGEICIGROS"
TEMP_VILLAGE_INFO_TAG = "TEMP_VILLAGE_INFO"
PAYSAN_OR_ARTISAN_WINDOW_TAG = "PAYSAN_OR_ARTISAN_WINDOW"
MORE_INFO_WINDOW = "MORE_INFO_WINDOW"
CHOOSE_VILLAGE_TAG = "CHOOSE_VILLAGE"

# Tag qui trigger les fonctions appropriées
MORE_INFO_TAG = "MORE_INFO"
CHANGE_PAGE_MINUS = "CPM"
CHANGE_PAGE_PLUS = "CPP"
SHOW_OR_HIDE_PAGE_TAG = "SHOW_OR_HIDE_PAGE"
SHOW_OR_HIDE_HISTORY_TAG = "SHOW_OR_HIDE_HISTORY"
SCROLLBAR_TAG = "SCROLLBAR_TAG"
RECTANGLE_ACTION = "RECTANGLE_ACTION"
BUILD_CITY = "BUILD_CITY"
CANCEL_BUILD_CITY_TAG = "CANCEL_BUILD_CITY"
BUILD_CHURCH = "BUILD_CHURCH"
CANCEL_BUILD_CHURCH = "CANCEL_BUILD_CHURCH"
CHOOSE_VILLAGE_TO_IMMIGRATE_TAG = "CHOOSE_VILLAGE_TO_IMMIGRATE"
IMMIGRATE_TAG = "IMMIGRATE"
CANCEL_IMMIGRATION_TAG = "CANCEL_IMMIGRATE"
PLUS_IMMIGRANTS_TAG = "ADD_IMMIGRANTS"
MINUS_IMMIGRANTS_TAG = "MINUS_IMMIGRANTS"
OK_EVENT_TAG = "OK_EVENT"
INFO_EVENT_TAG = "INFO_EVENT"
PAYSAN_OR_ARTISAN_TAG = "PAYSAN_OR_ARTISAN"
MOVE_WINDOW = "MOVE_WINDOW"
CLOSE_MORE_INFO_WINDOW = "CLOSE_MORE_INFO_WINDOW"
PIN_MORE_INFO_WINDOW = "PIN_MORE_INFO_WINDOW"
DRAG_CORNER_MORE_INFO_WINDOW_TAG = "DRAG_CORNER_MORE_INFO_WINDOW"
CANCEL_CHOOSE_VILLAGE_TO_IMMIGRATE_TAG = "CANCEL_CHOOSE_VILLAGE_TO_IMMIGRATE"

# si
si = 'si'


text_categories = ["text", "PA", "additionalcost"]
# LES ACTIONS SONT DANS L'ORDRE SUIVANT : DE GAUCHE A DROITE **PUIS** DE HAUT EN BAS
ACTION_FOR_YOUR_TURN = [
    {
        "text": "Immigration",
        "PA": "1 PA",
        "additionalcost": "",
        "do": PAYSAN_OR_ARTISAN_TAG
    },
    {
        "text": "Construire une église",
        "PA": "6 PA",
        "additionalcost": "100 arg, 50 res",
        "do": BUILD_CHURCH
    },
    {
        "text": "Vassaliser",
        "PA": "4 PA",
        "additionalcost": "Y arg, Z res",
        "do": NOTHING_TAG
    },
    {
        "text": "Construire un village",
        "PA": "8 PA",
        "additionalcost": "300 arg, 150 res",
        "do": BUILD_CITY
    },
    {
        "text": "Impôt",
        "PA": "5 PA",
        "additionalcost": "",
        "do": NOTHING_TAG
    },
    {
        "text": "Recruter soldat",
        "PA": "2 PA",
        "additionalcost": "40 arg, 40 res",
        "do": NOTHING_TAG
    },
    {
        "text": "Déclarer la guerre",
        "PA": "8 PA",
        "additionalcost": "100 res",
        "do": NOTHING_TAG
    },
    {
        "text": "H",
        "PA": "X PA",
        "additionalcost": "Y arg, Z res",
        "do": NOTHING_TAG
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

FILL_ACTION_BOX = "#646464"
FILL_CANCEL = "#D43353"
FILL_OK = "#31BC25"
FILL_INFO = "#266CB6"

fill_brighter = {
    FILL_ACTION_BOX: "#A5A5A5",
    FILL_CANCEL: "#DC657C",
    FILL_OK: "#68E35D",
    FILL_INFO: "#5397E0"
}

fill_darker = {
    FILL_ACTION_BOX: "#474646",
}


def set_tags(highlight_tag=NOTHING_TAG, trigger_tag=NOTHING_TAG, drag_tag=NOTHING_TAG, color_tag=FILL_ACTION_BOX, hud_tag=NOTHING_TAG, group_tag=""):
    return highlight_tag, trigger_tag, drag_tag, color_tag, hud_tag, group_tag

pad_from_borders = 15

def get_width_text(text: str):

    # On récupère la font de base pour calculer la taille des rectangles
    text_font = font.nametofont("TkDefaultFont")

    # Mesurer la largeur et la hauteur du texte
    # Ici, ajout d'un pad sur la largeur pour éviter d'avoir un rectangle PARFAITEMENT à la largeur du texte
    return text_font.measure(text) + pad_from_borders

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

def nom_aleatoire_village():
    return choice([noms_village])

def prenom_aleatoire() :
    return choice([prenoms_perso])

def dummy(*args):
    pass
