"""
    def paysan_or_artisan(self, event: tk.Event):

        height = 30
        pad = 40
        height_triangle = 20

        title_text = "Quelle est la profession du villageois ?"

        # On récupère la font de base pour calculer la taille des rectangles
        text_font = font.nametofont("TkDefaultFont").copy()
        text_font.config(size=12)

        # Mesurer la largeur et la hauteur du texte
        text_width = text_font.measure(title_text)

        x0_cadre = 30
        y0_cadre = self.winfo_height() - HEIGHT_BOTTOM_HUD - PADY_BOTTOM_HUD - height * 2 - height_triangle
        x1_cadre = x0_cadre + text_width
        y1_cadre = y0_cadre + height

        y0_cadre_choices = y1_cadre
        y1_cadre_choices = y0_cadre_choices + height
        center_x = (x0_cadre + x1_cadre) // 2

        choices_text = ["Paysan 1 PA", "Artisan 2 PA"]

        self.create_polygon(x0_cadre, y0_cadre, x1_cadre, y0_cadre,
                            center_x, y1_cadre_choices + height_triangle,
                            fill=FILL_ACTION_BOX, tags=set_tags() + (TEMP_TAG,), outline="black", width=1)

        # Donc, on crée deux rectangles, pour choisir entre paysan et artisan
        self.create_text_in_rectangle(
            x0=center_x - text_font.measure(choices_text[0]) - pad,
            y0=y0_cadre_choices,
            x1=center_x,
            y1=y1_cadre_choices,
            rectangle_tags=set_tags(highlight_tag=CLICKABLE_TAG) + (TEMP_TAG,),
            text_tags=set_tags() + (TEXT_TAG, TEMP_TAG,),
            text_font=text_font,
            content=choices_text[0]
        )

        self.create_text_in_rectangle(
            x0=center_x,
            y0=y0_cadre_choices,
            x1=center_x + text_font.measure(choices_text[1]) + pad,
            y1=y1_cadre_choices,
            rectangle_tags=set_tags(highlight_tag=CLICKABLE_TAG) + (TEMP_TAG,),
            text_tags=set_tags() + (TEXT_TAG, TEMP_TAG,),
            text_font=text_font,
            content=choices_text[1]
        )

        self.create_text_in_rectangle(
            x0=x0_cadre - pad // 2,
            y0=y0_cadre,
            x1=x1_cadre + pad // 2,
            y1=y1_cadre,
            rectangle_tags=set_tags() + (TEMP_TAG,),
            text_tags=set_tags() + (TEMP_TAG,),
            text_font=text_font,
            content=title_text
        )
"""

"""def reload_map(self, event: tk.Event = None):
        \"\"\"

        :param event:
        :return:
        \"\"\"
        pass

         ANCIEN CODE
        previous_canvas = copy.copy(self.canvas)

        # Le carré d'à gauche n'est que celui -1 et celui d'en haut est - (le nombre de carré sur une ligne)
        for id_square in previous_canvas.find_withtag("square"):
            square_types = []

            # En haut à gauche
            # En haut
            # En haut à droite
            # À droite
            # En bas à droite
            # En bas
            # En bas à gauche
            # À gauche

            for square in [-11, -10, -9, 1, 11, 10, 9, -1]:
                tags = previous_canvas.gettags(id_square + square)
                if tags:
                    square_types += [tags[1]]

            count = Counter(square_types)

            if 1 >= count[previous_canvas.gettags(id_square)[1]] >= 4:
                to_be = random.choice([PLAINE, FORET, MONTAGNE, LAC])

                square_tags = list(previous_canvas.gettags(id_square))
                square_tags[1] = to_be
                self.canvas.itemconfigure(id_square, fill=["#8AF87F", "#0D7901", "#B4B4B5", "#76DCF4"][int(to_be)],
                                          tags=tuple(square_tags))

        # self.after(50, self.reload_map)
        """