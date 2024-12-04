import tkinter as tk

def on_button_press(event):
    """Simule l'enfoncement du bouton."""
    canvas.itemconfig(rect_outer, fill="darkgrey")  # Ombre extérieure plus sombre
    canvas.itemconfig(rect_inner, fill="grey")     # Fond intérieur légèrement foncé
    canvas.move(rect_inner, 1, 1)                 # Décale l'intérieur pour simuler l'enfoncement
    canvas.move(button_text, 1, 1)                # Décale le texte avec le bouton

def on_button_release(event):
    """Simule le relâchement du bouton."""
    canvas.itemconfig(rect_outer, fill="lightgrey")  # Rétablit l'ombre extérieure
    canvas.itemconfig(rect_inner, fill="white")      # Rétablit le fond intérieur clair
    canvas.move(rect_inner, -1, -1)                 # Ramène l'intérieur à sa position initiale
    canvas.move(button_text, -1, -1)                # Ramène le texte à sa position initiale

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Bouton 3D Amélioré")

canvas = tk.Canvas(root, width=400, height=300, bg="lightblue")
canvas.pack()

# Dimensions du bouton
x1, y1, x2, y2 = 120, 100, 280, 150

# Rectangle extérieur (ombre)
rect_outer = canvas.create_rectangle(x1, y1, x2, y2, fill="lightgrey", outline="darkgrey", width=3, tags="button")

# Rectangle intérieur (fond du bouton)
rect_inner = canvas.create_rectangle(x1 + 3, y1 + 3, x2 - 3, y2 - 3, fill="white", outline="grey", width=1, tags="button")

# Texte du bouton
button_text = canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="Clique-moi", font=("Arial", 14), tags="button")

# Ajout des événements pour les interactions
canvas.tag_bind("button", "<ButtonPress-1>", on_button_press)
canvas.tag_bind("button", "<ButtonRelease-1>", on_button_release)

root.mainloop()
