import tkinter as tk

from parameter import *
from Canvas.HUD.HUDABC import HUDABC

class HUDPaysanOrArtisan(HUDABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self.desired_workforce = 1
        self.artisan_choice_id = 0
        self.paysan_choice_id = 0

    @property
    def tag(self):
        return PAYSAN_OR_ARTISAN_WINDOW_TAG

    def create(self, geometry_width, geometry_height):

        height = 150

        title_text = "Quelle sera la profession du villageois ?"

        # Mesurer la largeur et la hauteur du texte
        # Ici, ajout d'un pad sur la largeur pour éviter d'avoir un rectangle PARFAITEMENT à la largeur du texte
        text_width = get_width_text(title_text)

        # coordonnées du rectangle principal pour l'avoir au milieu de l'écran
        x0_cadre = geometry_width // 2 - text_width // 2
        y0_cadre = geometry_height // 2 - height // 2
        x1_cadre = x0_cadre + text_width
        y1_cadre = y0_cadre + height

        center_x = (x0_cadre + x1_cadre) // 2

        # Rectangle qui englobe tout ça
        self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre,
            fill=FILL_ACTION_BOX,
            tags=set_tags() + (TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
            state="hidden"
        )

        # Titre choix
        self.canvas.create_text(
            x0_cadre + text_width // 2, y0_cadre + pad_from_borders,
            text=title_text,
            tags=set_tags() + (TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
            state="hidden"
        )

        # Effectif souhaité
        text = "Effectif souhaité : 1"

        width_text = get_width_text(text)
        custom_font = font.nametofont("TkDefaultFont").copy()
        custom_font.config(size=6)

        self.canvas.create_text(
            center_x - 20, y0_cadre + pad_from_borders + 25,
            text=text,
            tags=set_tags() + (TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG, TEXT_NB_IMMIGRANTS),
            state="hidden"
        )

        # Bouton ajouter effectif
        self.canvas.create_text_in_rectangle(
            center_x - 20 + width_text // 2, y0_cadre + pad_from_borders + 15, center_x + width_text // 2, y0_cadre + pad_from_borders + 25,
            text="▲",
            rectangle_tags=set_tags(CLICKABLE_TAG, PLUS_IMMIGRANTS_TAG) + (TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
            text_tags=set_tags() + (TEXT_TAG, TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
            text_font=custom_font,
            state="hidden"
        )

        # Bouton retirer effectif
        self.canvas.create_text_in_rectangle(
            center_x - 20 + width_text // 2, y0_cadre + pad_from_borders + 27, center_x + width_text // 2, y0_cadre + pad_from_borders + 37,
            text="▼",
            rectangle_tags=set_tags(CLICKABLE_TAG, MINUS_IMMIGRANTS_TAG) + (TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
            text_tags=set_tags() + (TEXT_TAG, TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
            text_font=custom_font,
            state="hidden"
        )

        # Paysan choix
        self.paysan_choice_id = self.canvas.create_text_in_rectangle(
            x0_cadre + pad_from_borders,
            y0_cadre + pad_from_borders + 40,
                    (x0_cadre + x1_cadre) // 2,
            y1_cadre - 20,
            text="Paysan 1 PA",
            rectangle_tags=set_tags(highlight_tag=TOGGLEABLE_TAG) + (TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
            text_tags=set_tags() + (TEXT_TAG, TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
            state="hidden"
        )

        # Artisan choix
        self.artisan_choice_id = self.canvas.create_text_in_rectangle(
            (x0_cadre + x1_cadre) // 2,
            y0_cadre + pad_from_borders + 40,
            x1_cadre - pad_from_borders,
            y1_cadre - 20,
                    text="Artisan 2 PA",
            rectangle_tags=set_tags(highlight_tag=TOGGLEABLE_TAG) + (TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
            text_tags=set_tags() + (TEXT_TAG, TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
            state="hidden"
        )

        self.canvas.radiobuttons.add(self.canvas,
            (self.paysan_choice_id, self.artisan_choice_id),
            # Ok bouton
            ok_button_id=self.canvas.create_text_in_rectangle(
                x1_cadre - 25,
                y1_cadre - 15,
                x1_cadre + 5,
                y1_cadre + 5, "OK", fill=FILL_OK,
                rectangle_tags=set_tags(highlight_tag=CLICKABLE_TAG, trigger_tag=IMMIGRATE_TAG,
                                        color_tag=FILL_OK) + (TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
                text_tags=set_tags() + (TEXT_TAG, TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
                state="hidden"
            )
        )

        # Annuler bouton
        self.canvas.create_text_in_rectangle(
            x0_cadre - 5,
            y1_cadre - 15,
            x0_cadre + 55,
            y1_cadre + 5, "Annuler", fill=FILL_CANCEL,
            rectangle_tags=set_tags(highlight_tag=CLICKABLE_TAG, trigger_tag=CANCEL_IMMIGRATION_TAG,  color_tag=FILL_CANCEL) + (TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
            text_tags=set_tags() + (TEXT_TAG, TEMP_TAG, PAYSAN_OR_ARTISAN_WINDOW_TAG),
            state="hidden"
        )

    def replace(self, event: tk.Event) -> None:
        pass

    def show_animation(self) -> None:
        pass

    def hide_animation(self) -> None:
        pass

    def immigrate(self, e=None):

        print(self.canvas.radiobuttons.get_selected_option(self.canvas.gettags(IMMIGRATE_TAG)[4]))

        # Même comportement que si on ne voulait pas construire l'église, sauf qu'ici on la construit
        self.cancel_immigration()

    def cancel_immigration(self, e=None):
        self.canvas.radiobuttons.radiobuttons[self.canvas.gettags(IMMIGRATE_TAG)[4]].reset()

        for item_id in self.canvas.find_withtag(PAYSAN_OR_ARTISAN_WINDOW_TAG):
            self.canvas.itemconfigure(item_id, state="hidden")

        # On reset aussi l'effectif
        self.desired_workforce = 1

    def plus_immigrants(self, e=None):
        self.desired_workforce += 1 if self.desired_workforce + 1 <= 10 else 0

        if PA < self.desired_workforce * 2:
            # Griser le bouton artisan et ne le rendre plus clickable
            self.griser(self.artisan_choice_id)

            if PA < self.desired_workforce:
                # Griser le bouton paysan et ne le rendre plus clickable
                self.griser(self.paysan_choice_id)

        self.refresh_text()

    def minus_immigrants(self, e=None):
        self.desired_workforce -= 1 if self.desired_workforce - 1 > 0 else 0

        if PA >= self.desired_workforce:
            # Griser le bouton paysan et ne le rendre plus clickable
            self.degriser(self.paysan_choice_id)

            if PA >= self.desired_workforce * 2:
                # Griser le bouton artisan et ne le rendre plus clickable
                self.degriser(self.artisan_choice_id)

        self.refresh_text()

    def refresh_text(self):
        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.paysan_choice_id],
                      text=f"Paysan {self.desired_workforce} PA")
        self.canvas.itemconfigure(self.canvas.text_id_in_rectangle_id[self.artisan_choice_id],
                       text=f"Artisan {self.desired_workforce * 2} PA")
        self.canvas. itemconfigure(TEXT_NB_IMMIGRANTS, text=f"Effectif souhaité : {self.desired_workforce}")

    def griser(self, button_id: int):
        tags = list(self.canvas.gettags(button_id))
        tags[HIGHLIGHT_TAG_INDEX] = NOTHING_TAG
        self.canvas.itemconfigure(button_id, fill=fill_darker[tags[3]])
        self.canvas.itemconfigure(button_id, tags=tags)

    def degriser(self, button_id: int):
        tags = list(self.canvas.gettags(button_id))
        tags[HIGHLIGHT_TAG_INDEX] = TOGGLEABLE_TAG
        self.canvas.itemconfigure(button_id, fill=tags[3])
        self.canvas.itemconfigure(button_id, tags=tags)

