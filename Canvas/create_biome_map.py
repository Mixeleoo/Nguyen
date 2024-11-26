import random
from parameter import *

def x_on_100_chance(x):
    return 1 if random.randint(0, 100) < x else 0


def create_biome_map(rows, cols):
    # Initialisation de la carte avec des "plaines" par défaut
    map_grid = [[PLAINE_TAG for _ in range(cols)] for _ in range(rows)]

    # Définir les centres des biomes
    place_biome_center(map_grid, rows, cols, LAKE_TAG, 3, 6, 0.05)  # Lacs, 5% de la carte
    place_biome_center(map_grid, rows, cols, FOREST_TAG, 5, 8, 0.25)  # Forêts, 25% de la carte
    place_biome_center(map_grid, rows, cols, MOUNTAIN_TAG, 4, 8, 0.15)  # Montagnes, 15% de la carte

    return map_grid


def place_biome_center(map_grid, rows, cols, terrain_type, min_size, max_size, coverage_ratio):
    # Calcule le nombre de cases que ce type de terrain doit couvrir
    target_cells = int(coverage_ratio * rows * cols)
    placed_cells = 0

    while placed_cells < target_cells:
        # Choisir une position aléatoire pour un "noyau" de biome
        center_row = random.randint(0, rows - 1)
        center_col = random.randint(0, cols - 1)

        # Taille du biome
        biome_size = random.randint(min_size, max_size)

        # Utiliser un "bfs" simple pour étendre ce biome autour du noyau
        queue = [(center_row, center_col)]
        for _ in range(biome_size ** 2):  # Nombre de cases dans le biome
            if not queue:
                break

            # Prendre une cellule dans la queue
            row, col = queue.pop(0)

            # Assurer que la cellule est dans la carte et pas déjà modifiée
            if 0 <= row < rows and 0 <= col < cols and map_grid[row][col] == PLAINE_TAG:
                map_grid[row][col] = terrain_type
                placed_cells += 1

                # Ajouter des cellules voisines à la file d'attente pour étendre le biome
                if placed_cells < target_cells:
                    queue.extend([
                        (row + x_on_100_chance(50), col),
                        (row - x_on_100_chance(50), col),
                        (row, col + x_on_100_chance(50)),
                        (row, col - x_on_100_chance(50))
                    ])
                else:
                    break