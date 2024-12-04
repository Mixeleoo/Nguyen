import tkinter as tk

def on_button_press(event):
    canvas.itemconfig(rect_border, outline="#CCCCCC")     # Bord éclairé
    canvas.itemconfig(rect_inner, outline="grey")       # Bord interne clair
    canvas.itemconfig(rect_inner, fill="#333333")      # Bord interne foncé
    print("Bouton pressé !")  # Vérification visuelle

def on_button_release(event):
    canvas.itemconfig(rect_border, outline="darkgrey")  # Bord plus sombre
    canvas.itemconfig(rect_inner, outline="black")      # Bord interne foncé
    canvas.itemconfig(rect_inner, fill="#514E4E")      # Bord interne foncé
    print("Bouton relâché !")  # Vérification visuelle

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Bouton 3D")

canvas = tk.Canvas(root, width=400, height=200, bg="lightblue")
canvas.pack()

# Création du bouton rectangle avec un tag
x1, y1, x2, y2 = 100, 80, 200, 120
rect_border = canvas.create_rectangle(x1 + 1, y1 + 1, x2, y2, outline="#CCCCCC", width=2, tags="button")
rect_inner = canvas.create_rectangle(x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill="#333333", outline="grey", tags="button")

# Ajout des événements pour les interactions sur le tag "button"
canvas.tag_bind("button", "<ButtonPress-1>", on_button_press)
canvas.tag_bind("button", "<ButtonRelease-1>", on_button_release)

button = canvas.create_rectangle(x1 + 1 + 110, y1 + 1, x2 + 110, y2, fill="#333333", tags="old_button")

canvas.tag_bind("old_button", "<ButtonPress-1>", lambda e: canvas.itemconfigure(button, fill="#514E4E"))
canvas.tag_bind("old_button", "<ButtonRelease-1>", lambda e: canvas.itemconfigure(button, fill="#333333"))

root.mainloop()
