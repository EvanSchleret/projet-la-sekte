import math

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

chemin_a_faire = []

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    """
    Fonction permettant de faire des calcules avant que la partie commence.
    :param mazeMap: dict -> un dictionnaire de dictionnaire représentant la map
    :param mazeWidth: int -> la largeur de la map
    :param mazeHeight: int -> la hauteur de la map
    :param playerLocation: tuple -> la position x et y du joueur
    :param opponentLocation: tuple -> la position x et y de l'opposant
    :param piecesOfCheese: list -> une liste de tuple qui représente la position des fromages sur la carte
    :param timeAllowed: int -> temps alouer pour faire un mouvement
    :return:
    """
    global chemin_a_faire

    chemin_a_faire = chemin_plus_court(astar(mazeMap, playerLocation, piecesOfCheese))
    return

def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    """
    Fonction permetant de retourner le mouvement du rat ou python
    :param mazeMap: dict -> un dictionnaire de dictionnaire représentant la map
    :param mazeWidth: int -> la largeur de la map
    :param mazeHeight: int -> la hauteur de la map
    :param playerLocation: tuple -> la position x et y du joueur
    :param opponentLocation: tuple -> la position x et y de l'opposant
    :param playerScore: int -> nombre de fromage qu'on a mangé
    :param opponentScore: int -> nombre de fromage que l'opposant a mangé
    :param piecesOfCheese: list -> une liste de tuple qui représente la position des fromages sur la carte
    :param timeAllowed: int -> temps alouer pour faire un mouvement
    :return: str -> le movement que l'on veut effectuer (UP, DOWN, RIGHT, LEFT)
    """
    global chemin_a_faire

    if chemin_a_faire:
        return move(playerLocation, piecesOfCheese)
    else:
        chemin_a_faire = chemin_plus_court(astar(mazeMap, playerLocation, piecesOfCheese))
        return move(playerLocation, piecesOfCheese)


def move(playerLocation: tuple, piecesOfCheese):
    """
    Fonction qui permet de faire bouger la souris en retournant un mouvement
    :param playerLocation: tuple -> la position actuelle du joueur
    :param piecesOfCheese: list -> la liste de tout les fromages
    :return: str -> le mouvement à effectuer
    """
    global chemin_a_faire

    dest_x, dest_y = chemin_a_faire[0] #la position x et y de destination correspond à la première position du chemin à faire
    play_x, play_y = playerLocation #la position x et y du joueur
    dernier = chemin_a_faire[-1]

    chemin_a_faire.pop(0) #on enlève ensuite la première position du chemin à faire car on va le parcourir

    #on compare les positions x et y du joueur et de la destination pour savoir quel mouvement faire

    if dernier in piecesOfCheese: #on fait une petite condition au milieu des mouvements pour savoir si le fromage est toujours la ou non
        #car si le fromage est pas la ca ne sert a rien d'y aller et du coup on vide chemin_a_faire comme ca on pourra recalculer un nouveau chemin
        #ca permet de changer de direction si un adversaire mange un fromage avant qu'on y arrive
        if play_x < dest_x:
            return MOVE_RIGHT
        if play_x > dest_x:
            return MOVE_LEFT
        if play_y < dest_y:
            return MOVE_UP
        if play_y > dest_y:
            return MOVE_DOWN
    else:
         chemin_a_faire = []


def chemin_plus_court(chemins: dict):
    """
    Fonction qui permet de trouver le chemin le plus court dans un dictionaire de chemins possible
    :param chemins: dict -> un dictionnaire contenant tout les chemins possible pour aller vers un fromage. La clé est
    le point d'arrivé (donc le fromage qu'on va prendre) et la valeur est une liste avec toutes les positions pour acceder
    au fromage.
    :return: list -> le chemin le plus petit. On rend la liste avec [2:] pour que les 2 premières positions de la liste ne
    soient pas dans le return. La première étant le cout du chemin et la seconde étant la position de départ qui ne sont donc
    pas nécessaire.
    """
    global chemin_a_faire

    plus_petit = math.inf #on initialise plus_petit à math.inf pour donner un chiffre impossible à atteindre et être sur que ca sera forcement plus petit
    chem_plus_petit = []

    for val in chemins.values():#pour chaque valeur dans la liste des chemins (donc pour chaque liste de chemins)
        if val[0] < plus_petit:#on test la valeur 0 (qui représente le cout du chemin) avec plus petit
            plus_petit = val[0]#on reasigne plus petit à la valeur 0 du chemin si et le chem_plus_petit au chemin
            chem_plus_petit = val

    return chem_plus_petit[2:]#puis on retourne le chemin le plus petit sans les 2 premières positions

class Noeud:
    def __init__(self, position: tuple, valeur: int, parent):
        """
        Fonction constructeur de la classe noeud
        :param position: tuple -> position x et y du noeud
        :param valeur: int -> valeur qui représente le cout du noeud
        :param parent: noeud -> noeud parent a celui-ci
        """
        self.position = self.x, self.y = position #initialisation de self.position et self.x, self.y comme ca on peut soit utiliser position si on veut le x et le y
        #ou bien simplement utiliser x ou y
        self.valeur = valeur
        self.parent = parent

        self.g = 0 #represente la distance au point de départ
        self.h = 0 #représente la distance au point d'arrivé
        self.f = 0 #represente le cout total du noeud (donc g + h)


def return_chemin(pos_actuelle: Noeud):
    """
    Fonction qui retourne le chemin à partire du noeud d'arrivé
    :param pos_actuelle: noeud -> le dernier noeud du chemin (donc l'arrivé)
    :return: list -> chemin à parcourir pour arrivé au fromage
    """
    chemin = []
    cout = 0

    while pos_actuelle is not None: #on boucle sur pos et tant que c'est pas égal à None on continue
        chemin.append(pos_actuelle.position) #on ajoute la position de pos au chemin et on reasigne pos pour qu'il soit égale a sont parent
        cout += pos_actuelle.f
        pos_actuelle = pos_actuelle.parent

    chemin.append(cout) #on ajoute à la fin cout qui représente le cout totale du chemin

    return chemin[::-1] #on retourne la liste inversé


def astar(mazeMap, playerLocation, piecesOfCheese):
    """
    Algorithme qui va calculer le chemin le plus rapide pour chaque fromage
    :param mazeMap: dict -> graph de la map jouable
    :param playerLocation: tuple -> position du joueur
    :param piecesOfCheese: list -> list des positions des fromages
    :return: list -> liste de tout les chemins possible
    """
    tout_les_chemins = {}

    #on boucle sur tout les fromages restant sur la map et on calcule pour chacun de ces fromages le chemin le plus rapide pour y acceder
    for fromage in piecesOfCheese:
        start = Noeud(playerLocation, 0, None) #on crée les noeud start et end qui représente le point de départ et le point d'arrivé
        end = Noeud(fromage, 0, None)

        liste_ouverte = {} #la liste ouverte représente les noeud qu'on doit encore potentiellement visiter
        liste_ferme = {} #la liste fermé représente les noeud qu'on a déjà visité

        liste_ouverte[start.position] = start #vu que liste ouverte est un dico on lui ajoute le noeud de départ avec comme clé sa position

        nb_max_iterations = (len(mazeMap) // 2) ** 10 #on défini le nombre max d'itération avec la taille de la map
        compteur_iterations = 0 #le compteur d'itération sert au cas ou le chemin prendrait trop de temps à chercher pour pas boucler pendant trop longtemps


        while liste_ouverte: #on boucle sur les noeud de la liste ouverte
            compteur_iterations += 1

            if compteur_iterations > nb_max_iterations: #si le nombre d'itérations est plus grande que le nombre max d'itération, on arrete de chercher le chemin et on break
                break

            pos_actu = list(liste_ouverte.values())[0] #prendre la première position de la liste ouverte

            for valeur in liste_ouverte.values(): #boucle sur les valeur de la liste (donc les noeud) et on compare les f pour savoir quel serait le noeud suivant idéale
                if valeur.f < pos_actu.f:
                    pos_actu = valeur

            liste_ouverte.pop(pos_actu.position) #on retire le nouveau noeud idéale de la liste ouverte car on va le visiter et on l'ajoute à la liste fermé
            liste_ferme[pos_actu.position] = pos_actu

            if pos_actu.position == end.position: #si on a atteint le fromage rechercher (donc end) on return ajoute le chemin pour acceder à celui-ci dans le dico tout_les_chemins
                #on lui donne comme clé la position final (donc la même que end) et on break pour passer au fromage suivant
                tout_les_chemins[pos_actu.position] = return_chemin(pos_actu)
                break

            for cle, val in mazeMap[pos_actu.position].items(): #on va chercher dans la mazemap le dico qui correspond a la position actuelle
                #on va ensuite boucler sur ses voisins et si les voisins ne sont ni dans la liste ouverte, ni dans la liste fermé on les instancie en noeud et on les
                #ajoute a la liste ouverte
                if cle not in liste_ouverte:
                    if cle not in liste_ferme:
                        vois = Noeud(cle, val, pos_actu)

                        vois.g = vois.valeur + pos_actu.g
                        vois.h = (vois.x - end.x) + (vois.y - end.y)
                        vois.f = vois.g + vois.h

                        liste_ouverte[cle] = vois

    return tout_les_chemins #une fois que l'on a trouvé un chemin pour chaque fromage on retourne la liste de tout les chemins
