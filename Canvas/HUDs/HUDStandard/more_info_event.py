
from .base import HUDStandardABC
from parameter import *
from ...Widget.StringVar import StringVar


class MoreInfoEvent(HUDStandardABC):
    def __init__(self, canvas):
        super().__init__(canvas)

        self._text = StringVar(self.canvas)
        self.backgroud_rect_id = 0

    def create(self, geometry_width, geometry_height):

        width = 150
        height = 20

        x0_cadre = geometry_width // 2 + 50
        y0_cadre = HEIGHT_EVENT + HEIGHT_HUD_TOP_SIDE + 50
        x1_cadre = x0_cadre + width
        y1_cadre = y0_cadre + height

        """
        self.triangle_id = self.canvas.create_polygon(x0_cadre, y0_cadre, x1_cadre, y0_cadre,
                            (village_coords[0] + village_coords[2]) // 2, (village_coords[1] + village_coords[3]) // 2,
                            fill=FILL_ACTION_BOX, tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,), width=1, state="hidden")
        """

        self.backgroud_rect_id = self.canvas.create_rectangle(
            x0_cadre, y0_cadre, x1_cadre, y1_cadre,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            fill=FILL_ACTION_BOX,
            state="hidden"
        )

        self._text.id = self.canvas.create_text(
            x0_cadre + 10,
            y0_cadre + 10,
            tags=set_tags(hud_tag=self.tag) + (TEMP_TAG,),
            state="hidden",
            anchor="nw",
            fill=FILL_TEXT
        )

    def replace(self, *args) -> None:
        pass

    def refresh_text(self, texts: tuple[str, ...]):
        height = 20
        final_text = ""
        max_width = 0

        for t in texts:
            height += 20
            final_text += t + "\n"
            w = get_width_text(t)
            if w > max_width:
                max_width = w

        final_text = final_text[:-1]
        self._text.set(final_text)
        coords = self.canvas.coords(self.backgroud_rect_id)
        self.canvas.coords(self.backgroud_rect_id, coords[0], coords[1], coords[0] + max_width, coords[1] + height)
