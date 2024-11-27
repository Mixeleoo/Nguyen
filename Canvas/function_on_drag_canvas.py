
import tkinter as tk

from parameter import *
from Canvas.animation_canvas import AnimationCanvas

class FunctionOnDragCanvas(AnimationCanvas):
    def __init__(self, master=None, cnf=None, **kw):
        # C'est PyCharm qui me dit de mettre ça au lieu de cnf={} directement dans les arguments donc...
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)
        self.tag_fod = {
            MAP_TAG: self.on_drag_map,
            SCROLLBAR_TAG: self.on_drag_scrollbar,
            MOVE_WINDOW: lambda e: self.hudwindow_more_info_supervisor.get_active_window().on_drag(e),
            DRAG_CORNER_MORE_INFO_WINDOW_TAG: lambda e: self.hudwindow_more_info_supervisor.get_active_window().on_drag_corner_window(e),
            NOTHING_TAG: lambda *args: None
        }

    def on_drag_map(self, event: tk.Event):
        dx = event.x - self.mouse_coor[0]
        dy = event.y - self.mouse_coor[1]

        # Déplace tous les carrés avec le tag "square"
        self.move(MAP_TAG, dx, dy)

    def on_drag_scrollbar(self, event: tk.Event):

        dy = event.y - self.mouse_coor[1]
        rectangle_history_id = self.find_withtag(HUD_RIGHT_SIDE)[0]
        scrollbar_id = self.find_withtag(SCROLLBAR_TAG)[0]

        if self.coords(scrollbar_id)[1] + dy < self.coords(rectangle_history_id)[1] + 25 or \
            self.coords(scrollbar_id)[3] + dy > self.coords(rectangle_history_id)[3] - 25:
            dy = 0

        # Déplace tous les carrés avec le tag "square"
        self.move("active", 0, dy)

        self.drag_history_text(dy)

    def drag_history_text(self, dy: int):
        self.move(HISTORY_TEXT, 0, -dy)
        self.hide_exceeding_text()

    def hide_exceeding_text(self):
        text_history_ids = self.find_withtag(HISTORY_TEXT)
        rectangle_history_id = self.find_withtag(HUD_RIGHT_SIDE)[0]
        i = 0

        # Tous les textes en haut du rectangle deviennent hidden
        while self.coords(text_history_ids[i])[1] < self.coords(rectangle_history_id)[1] + 10:
            self.itemconfigure(text_history_ids[i], state="hidden")
            i += 1

        # Ceux au milieu on les laisse
        while self.coords(text_history_ids[i])[1] < self.coords(rectangle_history_id)[3] - 10:
            self.itemconfigure(text_history_ids[i], state="normal")
            i += 1

        # Ceux en bas du rectangle deviennent hidden
        while i < len(text_history_ids):
            self.itemconfigure(text_history_ids[i], state="hidden")
            i += 1
