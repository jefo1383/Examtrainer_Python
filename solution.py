def spiral_weaver(size: int) -> list[list[int]]:
    # 1. Cas d'erreur ou taille nulle
    if size <= 0:
        return []

    # 2. Création de la matrice remplie de zéros
    matrix = [[0] * size for _ in range(size)]
    
    # 3. Initialisation des 4 frontières (limites actuelles de la spirale)
    top = 0
    bottom = size - 1
    left = 0
    right = size - 1
    
    # Le compteur qui va de 1 à size*size
    num = 1

    # On tourne tant que les frontières ne se sont pas croisées
    while top <= bottom and left <= right:
        
        # ÉTAPE A : Remplir la ligne du haut (de gauche à droite)
        for i in range(left, right + 1):
            matrix[top][i] = num
            num += 1
        top += 1  # La ligne du haut est finie, on descend la frontière haute

        # ÉTAPE B : Remplir la colonne de droite (de haut en bas)
        for i in range(top, bottom + 1):
            matrix[i][right] = num
            num += 1
        right -= 1  # La colonne est finie, on décale la frontière droite vers la gauche

        # ÉTAPE C : Remplir la ligne du bas (de droite à gauche)
        for i in range(right, left - 1, -1):
            matrix[bottom][i] = num
            num += 1
        bottom -= 1  # On remonte la frontière basse

        # ÉTAPE D : Remplir la colonne de gauche (de bas en haut)
        for i in range(bottom, top - 1, -1):
            matrix[i][left] = num
            num += 1
        left += 1  # On décale la frontière gauche vers la droite

    return matrix