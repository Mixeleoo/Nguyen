import tkinter as tk

# Dictionnaire pour stocker les couleurs des rectangles
rect_colors = {}

def on_click(event):
    # Identifier l'élément cliqué
    item = canvas.find_withtag("current")
    if item:  # Si un élément est cliqué
        tag = canvas.gettags(item)[0]  # Récupérer le premier tag
        color = rect_colors.get(tag, "inconnu")
        print(f"Tu as cliqué sur un rectangle de couleur : {color}")

# Création de la fenêtre et du canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Création de plusieurs rectangles avec des couleurs différentes
colors = ["red", "blue", "green", "yellow"]
for i, color in enumerate(colors):
    x1, y1, x2, y2 = 50 * i + 10, 50, 50 * i + 60, 100
    tag = f"rect_{i}"
    rect = canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags=tag)
    rect_colors[tag] = color  # Associer la couleur au tag

# Associer le clic à la fonction
canvas.bind("<Button-1>", on_click)

root.mainloop()
