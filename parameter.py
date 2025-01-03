from collections import namedtuple
from dataclasses import dataclass
# -*- coding: utf-8 -*-

from random import randint, choice
from tkinter import font
from typing import Literal

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

@dataclass
class ActionCost:
    pa: int
    argent: int = 0
    ressources: int = 0

ACTIONS_NAME_COST: [str, ActionCost] = {
    PAYSAN_OR_ARTISAN_TAG: ActionCost(1),
    "Soldat": ActionCost(2, argent=20),
    BUILD_CHURCH: ActionCost(6, 100, 50),
    VASSALIZE_TAG: ActionCost(4),
    BUILD_CITY: ActionCost(8, 300, 150),
    TAXES_TAG: ActionCost(5),
    WAR_TAG: ActionCost(8, ressources=100)
}

# LES ACTIONS SONT DANS L'ORDRE SUIVANT : DE GAUCHE A DROITE **PUIS** DE HAUT EN BAS
ACTION_FOR_YOUR_TURN = [
    {
        "text": "Agrandir population",
        "PA": "1-10 PA",
        "additionalcost": "0-100 💰",
        "do": PAYSAN_OR_ARTISAN_TAG
    },
    {
        "text": "Construire une église",
        "PA": f"{ACTIONS_NAME_COST[BUILD_CHURCH].pa} PA",
        "additionalcost": "100 💰, 50 🍴",
        "do": BUILD_CHURCH
    },
    {
        "text": "Vassaliser",
        "PA": f"{ACTIONS_NAME_COST[VASSALIZE_TAG].pa} PA",
        "additionalcost": "Y 💰, Z 🍴",
        "do": VASSALIZE_TAG
    },
    {
        "text": "Construire un village",
        "PA": f"{ACTIONS_NAME_COST[BUILD_CITY].pa} PA",
        "additionalcost": "300 💰, 150 🍴",
        "do": BUILD_CITY
    },
    {
        "text": "Impôt",
        "PA": f"{ACTIONS_NAME_COST[TAXES_TAG].pa} PA",
        "additionalcost": "",
        "do": TAXES_TAG
    },
    {
        "text": "Déclarer la guerre",
        "PA": f"{ACTIONS_NAME_COST[WAR_TAG].pa} PA",
        "additionalcost": "100 🍴",
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


def eclaircir_couleur(hex_color: str, facteur: float) -> str:
    """
    Éclaircit une couleur hexadécimale.

    Args:
        hex_color (str): Couleur au format hexadécimal (ex: "#123456").
        facteur (float): Facteur d'éclaircissement (entre 0 et 1).
                         0.1 correspond à un léger éclaircissement, 1 pour un blanc total.

    Returns:
        str: Nouvelle couleur éclaircie au format hexadécimal.
    """
    if not (0 <= facteur <= 1):
        raise ValueError("Le facteur doit être compris entre 0 et 1.")

    # Convertir le hex en valeurs RGB
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)

    # Appliquer l'éclaircissement
    r = int(r + (255 - r) * facteur)
    g = int(g + (255 - g) * facteur)
    b = int(b + (255 - b) * facteur)

    # Retourner le nouveau hex
    return f"#{r:02x}{g:02x}{b:02x}"


# Exemple d'utilisation
couleur_claire = eclaircir_couleur("#123456", 0.3)
print(couleur_claire)  # Affiche une couleur éclaircie


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

    texts = text.split("\n")
    max_width = 0

    for text in texts:
        if max_width < text_font.measure(text):
            max_width = text_font.measure(text)

    return max_width + pad_from_borders

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
    return segments

Position = namedtuple('Position', ['x', 'y'])

# Quantité de ressources associée au type de terre sur la carte
capacite_prod_terre = {"PLAIN" : 1, "MOUNTAIN" : 0.8, "LAKE" : 1, "FOREST" : 1.2}

def dummy(*args):
    pass