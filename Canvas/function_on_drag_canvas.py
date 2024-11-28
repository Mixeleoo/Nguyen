
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
            SCROLLBAR_TAG: self.hud_history.on_drag_scrollbar,
            MOVE_WINDOW: lambda e: self.hudwindow_more_info_supervisor.get_active_window().on_drag(e),
            DRAG_CORNER_MORE_INFO_WINDOW_TAG: lambda e: self.hudwindow_more_info_supervisor.get_active_window().on_drag_corner_window(e),
            NOTHING_TAG: lambda *args: None
        }

    def on_drag_map(self, event: tk.Event):
        dx = event.x - self.mouse_coor[0]
        dy = event.y - self.mouse_coor[1]

        # Déplace tous les carrés avec le tag "square"
        self.move(MAP_TAG, dx, dy)
