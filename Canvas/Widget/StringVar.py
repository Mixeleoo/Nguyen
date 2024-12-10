
from Canvas.highlight_canvas import HighlightCanvas

class StringVar:
    def __init__(self, canvas: HighlightCanvas):
        self._canvas = canvas
        self._text = ""
        self._id = None

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, text_id: int):
        self._id = text_id

    @property
    def text(self) -> str:
        return self._text

    def set(self, text: str):
        """
        Méthode qui mettera à jour le texte en jeu
        :param text:
        :return:
        """
        self._text = text
        self._canvas.itemconfigure(self._id, text=text)

        return self
