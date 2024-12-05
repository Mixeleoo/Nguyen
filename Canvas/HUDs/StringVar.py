
from Canvas.highlight_canvas import HighlightCanvas


class StringVar:
    def __init__(self, canvas: HighlightCanvas, text: str, text_id: str):
        self._canvas = canvas
        self._text = text
        self._id = text_id

    @property
    def text(self):
        return self._text

    def draw(self) -> int:
        pass

    def set(self, text: str):
        """
        Méthode qui mettera à jour le texte en jeu
        :param text:
        :return:
        """
        self._text = text
        self._canvas.itemconfigure(self._id, text=text)

