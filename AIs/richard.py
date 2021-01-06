import math

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

chemin_plus_petit = []
g_max_iterations = 1


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global chemin_plus_petit
    chemin_plus_petit = chemin_plus_court(astar(mazeMap, playerLocation, piecesOfCheese))


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    global chemin_plus_petit

    while chemin_plus_petit:
        return move(playerLocation)
    chemin_plus_petit = chemin_plus_court(astar(mazeMap, playerLocation, piecesOfCheese))


def move(playerLocation):
    global chemin_plus_petit

    dest_x = chemin_plus_petit[0][0]
    dest_y = chemin_plus_petit[0][1]
    play_x = playerLocation[0]
    play_y = playerLocation[1]

    del chemin_plus_petit[0]

    if play_x < dest_x and play_y == dest_y:
        return MOVE_RIGHT
    if play_x > dest_x and play_y == dest_y:
        return MOVE_LEFT
    if play_y < dest_y and play_x == dest_x:
        return MOVE_UP
    if play_y > dest_y and play_x == dest_x:
        return MOVE_DOWN


def chemin_plus_court(chemins):
    global chemin_plus_petit

    plus_petit = math.inf
    chem_plus_petit = []

    for i in range(0, len(chemins)):
        if chemins[i][0] < plus_petit:
            plus_petit = chemins[i][0]
            chem_plus_petit = chemins[i][1:]

    return chem_plus_petit


class Noeud:
    def __init__(self, position, valeur, parent):
        self.x, self.y = position
        self.valeur = valeur
        self.parent = parent
        self.voisins = []

        self.g = 0
        self.h = 0
        self.f = 0

    def ajouter_voisins(self, mazeMap):
        for cle, val in mazeMap[(self.x, self.y)].items():
            self.voisins.append(Noeud(cle, val, self))


def return_chemin(pos_actuelle):
    chemin = []
    cout = 0
    pos = pos_actuelle

    while pos is not None:
        chemin.append((pos.x, pos.y))
        cout += pos.f
        pos = pos.parent
    chemin.append(cout)
    return chemin[::-1]


def astar(mazeMap, playerLocation, piecesOfCheese):
    global g_max_iterations
    tout_les_chemins = []

    for fromage in piecesOfCheese:
        start = Noeud(playerLocation, 0, None)
        end = Noeud(fromage, 0, None)

        liste_ouverte = []
        liste_ferme = []

        liste_ouverte.append(start)

        outer_iterations = 0

        while liste_ouverte:
            outer_iterations += 1

            pos_actu = liste_ouverte[0]
            index_pos_actu = 0

            #1ère itération : on a une liste de len 1 avec le start dedans
            #2ème itération : on a une liste de len x avec le start et ses voisins

            for noeud in range(len(liste_ouverte)): #1ère itération ca rentre pas dans le if donc rien ne change
                                                    #2ème itération ca rentre dans la boucle et un des voisins devrait avoir un f plus petit
                if liste_ouverte[noeud].f < pos_actu.f:
                    pos_actu = liste_ouverte[noeud]    #2ème itération on a trouvé une nouvelle position actuelle
                    index_pos_actu = noeud

            if outer_iterations > g_max_iterations:
                break

            liste_ouverte.pop(index_pos_actu)   #on à parcouru le noeud donc on l'enlève la liste à visiter
            liste_ferme.append(pos_actu)        #on l'ajoute à la liste déjà visité

            pos_actu.ajouter_voisins(mazeMap) #on cherche les voisins de la position

            if pos_actu.x == end.x and pos_actu.y == end.y:
                #return "On a trouvé la fin"
                tout_les_chemins.append(return_chemin(pos_actu))

            voisins = pos_actu.voisins

            for vois in voisins: #on va parcourir la liste des voisins
                if vois in liste_ouverte: #si le voisin n'es pas déjà dans la liste ouverte
                    continue
                vois.g = vois.valeur + pos_actu.g
                vois.h = (((vois.x - end.x) ** 2) + ((vois.y - end.y) ** 2))

                vois.f = vois.g + vois.h

                if vois in liste_ferme: #et qu'il n'est pas dan la liste ferme
                    continue

                liste_ouverte.append(vois)

    if len(tout_les_chemins) == 0:
        g_max_iterations *= 2
    return tout_les_chemins
