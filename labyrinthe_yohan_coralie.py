import os
from mysql.connector import connect, Error
import random
import time

# ---------------------variables globales--------------------------------
nbrLi = 20
nbrCo = 20
rencontre = False
score = 0
grille = [
    ['+', 'P', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+'],
    ['+', ' ', '+', '+', '+', '+', '+', '+', '+', ' ', ' ', ' ', ' ', ' ', ' ', 'O', '+', ' ', ' ', '+'],
    ['+', ' ', ' ', '+', ' ', ' ', ' ', '+', '+', ' ', '+', ' ', '+', '+', '+', '+', '+', ' ', ' ', '+'],
    ['+', '+', ' ', ' ', '+', '+', ' ', ' ', ' ', ' ', '+', ' ', '+', '+', '+', '+', '+', ' ', '+', '+'],
    ['+', ' ', '+', ' ', '+', '+', ' ', '+', ' ', '+', ' ', ' ', ' ', ' ', '+', '+', '+', ' ', '+', '+'],
    ['+', ' ', '+', ' ', '+', ' ', ' ', '+', ' ', '+', ' ', '+', ' ', '+', ' ', ' ', ' ', ' ', '+', '+'],
    ['+', ' ', '+', ' ', '+', ' ', '+', ' ', ' ', '+', ' ', '+', ' ', '+', ' ', '+', ' ', '+', ' ', '+'],
    ['+', ' ', ' ', ' ', '+', ' ', '+', '+', ' ', '+', ' ', ' ', ' ', ' ', ' ', '+', ' ', '+', ' ', '+'],
    ['+', ' ', '+', ' ', '+', ' ', '+', ' ', ' ', '+', ' ', '+', ' ', '+', '+', '+', ' ', '+', ' ', '+'],  # 9
    ['+', '+', '+', ' ', ' ', ' ', '+', ' ', '+', '+', ' ', '+', ' ', '+', '+', '+', ' ', '+', ' ', '+'],
    ['+', '+', '+', ' ', '+', ' ', '+', ' ', ' ', ' ', ' ', '+', ' ', '+', '+', '+', ' ', ' ', ' ', '+'],
    ['+', ' ', ' ', ' ', '+', ' ', '+', '+', '+', '+', '+', '+', ' ', ' ', '+', '+', '+', '+', ' ', '+'],  # 12
    ['+', ' ', '+', ' ', '+', ' ', '+', '+', '+', ' ', '+', '+', '+', '+', '+', ' ', ' ', ' ', ' ', '+'],
    ['+', ' ', '+', ' ', '+', ' ', '+', ' ', ' ', ' ', '+', ' ', ' ', ' ', ' ', ' ', '+', '+', '+', '+'],
    ['+', ' ', '+', ' ', '+', ' ', '+', '0', '+', ' ', ' ', ' ', ' ', '+', ' ', ' ', '+', '+', '+', '+'],
    ['+', ' ', '+', '+', '+', ' ', '+', '+', '+', ' ', '+', '+', ' ', '+', ' ', '+', '+', '+', '+', '+'],
    ['+', ' ', ' ', ' ', ' ', ' ', '+', '+', '+', ' ', ' ', ' ', '+', ' ', ' ', ' ', ' ', '+', ' ', '+'],
    ['+', '+', ' ', '+', ' ', '+', '+', '+', '+', '+', ' ', ' ', '+', ' ', '+', '+', ' ', '+', ' ', '+'],
    ['+', '+', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '+', ' ', ' ', ' ', ' ', ' ', '+', ' ', ' ', ' ', '+'],
    ['+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+', '+']]


# ----------------------------------------------------------------------------

# -----------------------------Affectation aléatoire de la position de la sortie et du minotaure-----------------------
def pre_sortie(grille):
    """ Affecte une position aléatoire à la sortie dans la labyrinthe"""
    sortie_ecrite = False
    cote = random.randint(0, 3)  # sélectionne au hasard le côté sur lequel se trouvera la sortie
    random_x = random.randint(0, 19)
    random_y = random.randint(0, 19)
    if cote == 0 and grille[1][random_y] == ' ':  # vérifie que la sortie est accessible au joueur
        grille[0][random_y] = 'S'
        sortie_ecrite = True
    elif cote == 1 and grille[18][random_y] == ' ':
        grille[19][random_y] = 'S'
        sortie_ecrite = True
    elif cote == 2 and grille[random_x][1] == ' ':
        grille[random_x][0] = 'S'
        sortie_ecrite = True
    elif cote == 3 and grille[random_x][18] == ' ':
        grille[random_x][19] = 'S'
        sortie_ecrite = True
    else:
        sortie_ecrite = False

    return random_x, random_y, sortie_ecrite


def positionSortie(
        grille):  # cette fonction permet de s'assurer que la fonction pre_sortie s'exécutera au moins une fois
    random_x, random_y, sortie_ecrite = pre_sortie(grille)
    while grille[1][random_y] != ' ' or grille[18][random_y] != ' ' or grille[random_x][1] != ' ' or grille[random_x][
        18] != ' ' and not sortie_ecrite:
        pre_sortie(grille)


def Sortie(grille):
    for x in range(nbrLi):
        for y in range(nbrCo):
            if grille[x][y] == 'S':
                return x, y
    raise Exception("Pas de sortie dans la grille.")


def pre_Minotaure(grille):  # affecte aléatoirement une position au minotaure dans le labyrinthe
    minotaure_ecrit = False
    random_xM = random.randint(0, 19)
    random_yM = random.randint(0, 19)
    if grille[random_xM][random_yM] == ' ':
        grille[random_xM][random_yM] = 'M'
        minotaure_ecrit = True
    else:
        minotaure_ecrit = False
    return random_xM, random_yM, minotaure_ecrit


def affectationMinotaure(grille):  # pour s'assurer que la fonction pre_minaotaure s'exécute au moins une fois
    random_xM, random_yM, minotaure_ecrit = pre_Minotaure(grille)
    while grille[random_xM][random_yM] != ' ' and minotaure_ecrit == False:
        pre_Minotaure(grille)
    return random_xM, random_yM


positionSortie(grille)
affectationMinotaure(grille)
xS, yS = Sortie(grille)


# -------------------------les recherches de positions ----------------------------
def positionMinautore(grille):
    for x in range(nbrLi):
        for y in range(nbrCo):
            if grille[x][y] == 'M':
                return x, y
    raise Exception("Pas de minotaure dans la grille.")


def positionJoueur(grille):
    for x in range(nbrLi):
        for y in range(nbrCo):
            if grille[x][y] == 'P':
                return x, y
    raise Exception("Pas de joueur dans la grille.")


def teleporter(grille):
    for x in range(nbrLi):
        for y in range(nbrCo):
            if grille[x][y] == '0':
                return x, y


# ----------------------------------------------------------------------------------
def connexion(Pseudo):
    """Accès à la bdd et insertion du pseudo du joueur dans la table"""
    connection = connect(
        host="localhost",
        user="root",
        password="",
        database="labyrinthe", )
    insert_joueur_query = """INSERT INTO joueur (pseudoJoueur) VALUES (%s)"""
    cursor = connection.cursor()
    cursor.execute(insert_joueur_query, (Pseudo,))
    connection.commit()
    return connection


def scores(score, Pseudo, ma_connexion):
    insert_scores_query = """UPDATE joueur SET score = %s  WHERE pseudoJoueur = %s"""
    select_max_score = """SELECT MIN(score) FROM joueur"""
    cursor = ma_connexion.cursor()
    valeurs = (score, Pseudo)
    cursor.execute(insert_scores_query, valeurs)
    cursor.execute(select_max_score)
    result = cursor.fetchall()
    best_score = result[0][0]  # result est une liste, or on ne veut afficher qu'un seul entier pour le score.
    ma_connexion.commit()
    if best_score <= score:
        print("Il vous a fallu ", score,
              " coups pour sortir du Labyrinthe en ayant vaincu le minotaure ! Le meilleur score est de ", best_score,
              ".")
    else:
        print("Bravo ! Vous avez battu le record qui était de ", best_score, " avec un score de ", score, " !")


def voisins(
        grille):  # cherche les coordonnées de la case vide à côté des téléporteurs. C'est la case sur laquelle le joueur apparaîtra.
    x, y = 0, 0
    if grille[teleporter(grille)[0] - 1][teleporter(grille)[1]] == ' ':
        x, y = teleporter(grille)[0] - 1, teleporter(grille)[1]
    elif grille[teleporter(grille)[0] + 1][teleporter(grille)[1]] == ' ':
        x, y = teleporter(grille)[0] + 1, teleporter(grille)[1]
    elif grille[teleporter(grille)[0]][teleporter(grille)[1] - 1] == ' ':
        x, y = teleporter(grille)[0], teleporter(grille)[1] - 1
    elif grille[teleporter(grille)[0]][teleporter(grille)[1] + 1] == ' ':
        x, y = teleporter(grille)[0], teleporter(grille)[1] + 1
    else:
        raise Exception("Pas normal")
    return x, y


xV, yV = voisins(grille)


def fin_du_jeu():
    os.system(
        'cls')  # permet d'afficher qu'un seul labyrinthe au lieu d'en afficher un nouveau dans le terminal à chaque coup
    affichage(grille)
    print("Vous avez triomphé du labyrhinte ! BRAVOOO")
    scores(score, Pseudo, ma_connexion)
    exit()


def legal(grille, direction):
    """ fin de jeu + gestion de la légalité des coups du joueur """
    global score, Pseudo
    x, y = positionJoueur(grille)
    if (x == xS and y == yS) and rencontre == True:
        fin_du_jeu()
    if direction == 'z':
        return grille[x - 1][y] != '+'  # return True si la case n'est pas un mur
    elif direction == 's':
        return grille[x + 1][y] != '+'
    elif direction == 'q':
        return grille[x][y - 1] != '+'
    elif direction == 'd':
        return grille[x][y + 1] != '+'
    return False


def minotaure_deplacement(grille):
    """
    Il se deplace forcement dans une case vide a chaque tour
    """
    global rencontre

    x, y = positionJoueur(grille)
    xM, yM = positionMinautore(grille)
    while True:
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # random déplacement du minotaure
        if grille[xM + dx][yM + dy] == 'P':  # On ajoute à sa position le random du sens de deplacement
            rencontre = True
            grille[xM + dx][yM + dy] == 'P'
            grille[x][y] == ' '
            break
        if grille[xM + dx][yM + dy] == ' ':
            grille[xM][yM] = ' '
            grille[xM + dx][yM + dy] = 'M'
            break


def deplacement(grille, direction):
    """Pour chaque deplacement on verifie si la direction du coup ne mene pas sur un coup spécial:
            -Le minotaure -> rencontre devient True
            -La sortie -> fin du jeu Si rencontre = True
            -Le portail d'entrée
        Sinon déplacement et mise en place du fil d'ariane '°'
    """
    global score, rencontre
    if not legal(grille, direction):
        return
    x, y = positionJoueur(grille)
    if rencontre == False:  # il y rentre SI le minotaure existe encore
        minotaure_deplacement(grille)
    if direction == 'z':
        # déplacements spéciaux
        if grille[x - 1][y] == 'M':
            rencontre = True
            print("Vous avez vaincu le minotaure")
            time.sleep(1)
        elif grille[x - 1][y] == "S" and rencontre == False:
            return
        elif grille[x - 1][y] == "O":
            grille[xV][yV] = "P"
            grille[x][y] = "°"
            return
        # déplacement simple
        grille[x][y] = '°'  # fil d'ariane
        grille[x - 1][y] = 'P'
    elif direction == 's':
        # déplacements spéciaux
        if grille[x + 1][y] == 'M':
            rencontre = True
            print("Vous avez vaincu le minotaure")
            time.sleep(1)
        elif grille[x + 1][y] == 'S' and rencontre == False:
            return
        elif grille[x + 1][y] == "O":
            grille[xV][yV] = "P"
            grille[x][y] = "°"
            return
        # déplacement simple
        grille[x][y] = '°'
        grille[x + 1][y] = 'P'
    elif direction == 'q':
        # déplacements spéciaux
        if grille[x][y - 1] == 'M':
            rencontre = True
            print("Vous avez vaincu le minotaure")
            time.sleep(1)
        elif grille[x][y - 1] == 'S' and rencontre == False:
            return
        elif grille[x][y - 1] == "O":
            grille[xV][yV] = "P"
            grille[x][y] = "°"
            return
        # déplacement simple
        grille[x][y] = '°'
        grille[x][y - 1] = 'P'
    elif direction == 'd':
        # déplacements spéciaux
        if grille[x][y + 1] == 'M':
            rencontre = True
            print("Vous avez vaincu le minotaure")
            time.sleep(1)
        elif grille[x][y + 1] == 'S' and rencontre == False:
            return
        elif grille[x][y + 1] == "O":
            grille[xV][yV] = "P"
            grille[x][y] = "°"
            return
        # déplacement simple
        grille[x][y] = '°'
        grille[x][y + 1] = 'P'
    legal(grille, direction)  # fin du jeu ?


def affichage(grille):
    """ affichage partiel de la grille selon les coordonnées du joueur. Cela permet de l'afficher au centre à chaque coup."""
    x, y = positionJoueur(grille)
    minX = max(0, x - 3)  # 0 si on est au bord
    maxX = min(nbrLi, x + 4)
    minY = max(0, y - 3)
    maxY = min(nbrCo, y + 4)

    for i in range(minX, maxX):
        for j in range(minY, maxY):
            print(grille[i][j], end=' ')
        print()


# -----------------------START------------------------------
Pseudo = input("Entrez votre pseudo : ")
ma_connexion = connexion(Pseudo)
while True:
    os.system('cls')
    affichage(grille)
    direction = input("Entrez la direction de déplacement (z/s/q/d) : ")
    score += 1
    deplacement(grille, direction)