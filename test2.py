import os


def count_lines_in_files(folder_path):
    nb_ligne_total = 0
    nb_fichiers_lu = 0

    """Compte le nombre de lignes dans tous les fichiers d'un dossier."""
    if not os.path.isdir(folder_path):
        print(f"Le chemin '{folder_path}' n'est pas un dossier valide.")
        return

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.py') and not file_path.startswith('./venv/'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        line_count = sum(1 for _ in file)
                    print(f"Fichier : {file_path} - {line_count} lignes")
                    nb_ligne_total += line_count
                    nb_fichiers_lu += 1

                except Exception as e:
                    print(f"Erreur lors de la lecture de '{file_path}': {e}")

    return nb_ligne_total, nb_fichiers_lu


# Exemple d'utilisation
dossier = input("Entrez le chemin du dossier : ")
res = count_lines_in_files(dossier)
print("Total -", res[0], "lignes\nNombre de fichiers lus -", res[1])
