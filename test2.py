import tkinter as tk
from tkinter import font


def draw_rectangle_with_text(canvas, text, x, y, padding=10):
    # Définir une police
    text_font = font.Font(family="Arial", size=16)

    # Mesurer la largeur et la hauteur du texte
    text_width = text_font.measure(text)
    text_height = text_font.metrics("linespace")

    # Dessiner le rectangle autour du texte
    canvas.create_rectangle(
        x, y,
        x + text_width + 2 * padding, y + text_height + 2 * padding,
        fill="lightblue"
    )

    # Dessiner le texte
    canvas.create_text(
        x + padding, y + padding,
        anchor="nw", text=text, font=text_font
    )


# Fenêtre Tkinter
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# Exemple
draw_rectangle_with_text(canvas, "Bonjour, Tkinter!", 50, 50)

root.mainloop()
