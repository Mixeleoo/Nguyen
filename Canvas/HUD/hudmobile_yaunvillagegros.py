
from parameter import *
from Canvas.HUD.HUDMobileABC import HUDMobileABC


class HUDMobileYaUnVillageGros(HUDMobileABC):
    def __init__(self, canvas):
        super().__init__(canvas)

    @property
    def tag(self):
        return TEMP_YAUNVILLAGEICIGROS_TAG

    def create(self) -> None:
        # On va créer l'HUD sur la première case
        village_coords = self.canvas.coords(self.canvas.find_withtag(MAP_TAG)[0])

        text = "y'a un village ici gros"

        width = get_width_text(text)
        height = 20

        x0_cadre = (village_coords[0] + village_coords[2]) // 2 - width // 2
        y0_cadre = village_coords[1] - 20
        x1_cadre = x0_cadre + width
        y1_cadre = y0_cadre + height

        self.canvas.create_polygon(x0_cadre, y0_cadre, x1_cadre, y0_cadre,
                            (village_coords[0] + village_coords[2]) // 2, (village_coords[1] + village_coords[3]) // 2,
                            fill=FILL_ACTION_BOX, tags=set_tags() + (TEMP_TAG, TEMP_YAUNVILLAGEICIGROS_TAG), width=1)

        self.canvas.create_text_in_rectangle(
            x0=x0_cadre,
            y0=y0_cadre,
            x1=x1_cadre,
            y1=y1_cadre,
            rectangle_tags=set_tags() + (TEMP_TAG, TEMP_YAUNVILLAGEICIGROS_TAG),
            text_tags=set_tags() + (TEMP_TAG, TEMP_YAUNVILLAGEICIGROS_TAG),
            text=text
        )

    def replace(self, village_id: int) -> None:

        center_x_village = (self.canvas.coords(village_id)[0] + self.canvas.coords(village_id)[2]) // 2
        center_y_village = (self.canvas.coords(village_id)[1] + self.canvas.coords(village_id)[3]) // 2

        dx = center_x_village - self.canvas.coords(self.canvas.find_withtag(self.tag)[0])[4]
        dy = center_y_village - self.canvas.coords(self.canvas.find_withtag(self.tag)[0])[5]

        self.canvas.move(self.tag, dx, dy)

    def show(self, village_id: int) -> None: super().show(village_id)
