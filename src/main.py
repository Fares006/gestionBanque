#   |--------------------------------------------|   #
#   |--------Gestion de Budget (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |--------------------------------------------|   #
# --Imports-- #

# --Constantes-- #
CLE_CRYPTAGE = 23


# --Fonctions-- #
def import_idents(chemin_fichier: str, cle: int = CLE_CRYPTAGE) -> dict:
    """
    Importe le contenu du fichier ident.txt et renvoie une liste qui contient :
    l'identifiant, le mot de passe, le nom et la clé de cryptage du fichier de l'utilisateur.

    Args:
        chemin_fichier: le chemin absolu du fichier ident.txt
        cle: clé de cryptage du fichier (en dur)

    Returns:
        le dictionnaire des identifiants (et informations associées dans une liste)
    """
    # Ouverture du fichier et initialisation des variables nécessaires
    idents = open(file=chemin_fichier, mode='r', encoding="utf-8")
    dict_ident = dict()
    ligne = idents.readline()
    ligne = decryptage(ligne)
    while ligne != '':
        num_champ = 0   # Numéro des champs, 0: identifiant, 1: mdp, 2: username, 3: clé de cryptage
        champ = ''
        for char in ligne:
            if char == '*' or char == '\n':
                if num_champ == 0:
                    identifiant = champ
                    dict_ident[identifiant] = []
                elif num_champ == 3:
                    dict_ident[identifiant].append(int(champ))
                else:
                    dict_ident[identifiant].append(champ)
                champ = ''
                num_champ += 1
            else:
                champ += char
        ligne = idents.readline()
        ligne = decryptage(ligne)

    idents.close()
    return dict_ident


def import_comptes(chemin_fichier: str, cle: int = CLE_CRYPTAGE) -> list:
    """
    Importe le contenu relatif aux comptes du fichier id.txt et renvoie la liste des comptes.

    Args:
        chemin_fichier: le chemin absolu du fichier id.txt
        cle: clé de cryptage du fichier (en dur)

    Returns:
        la liste contenant les différents comptes de l'utilisateur
    """
    fichier = open(file=chemin_fichier, mode='r', encoding="utf-8")
    liste_comptes = []
    ligne = fichier.readline()
    ligne = decryptage(ligne)
    while ligne != '':
        if ligne[0] != 'C':
            break   # On se permet un break ici, car les lignes de compte sont en premier.
        else:
            num_champ = 0
            champ = ''
            for char in ligne:
                if char == '*' or char == '\n':
                    if num_champ == 1:
                        liste_comptes.append(champ)
                    champ = ''
                    num_champ += 1
                else:
                    champ += char
        ligne = fichier.readline()
        ligne = decryptage(ligne)
    fichier.close()
    return liste_comptes


def import_operations(chemin_fichier: str, cle: int = CLE_CRYPTAGE) -> list:
    """
    Importe le contenu relatif aux opérations du fichier id.txt et renvoie une liste de tuples qui contient :
      - Une date (str),
      - Un libellé de l'opération (str),
      - Le compte concerné (str),
      - Le montant de l'opération (float),
      - Le mode de paiement (str),
      - Un booléen indiquant si l'opération est effective (bool),
      - Le budget concerné (str).

    Args:
        chemin_fichier: le chemin absolu du fichier id.txt
        cle: clé de cryptage du fichier (en dur)

    Returns:
        la liste des tuples contenant les différentes informations concernant chaque opération
    """
    fichier = open(file=chemin_fichier, mode='r', encoding="utf-8")
    liste_ope = []
    ligne = fichier.readline()
    ligne = decryptage(ligne)
    num_op = 0
    while ligne != '':
        if ligne[0] != 'O':
            ligne = fichier.readline()
            ligne = decryptage(ligne)
        else:
            num_champ = 0
            champ = ''
            for char in ligne:
                if char == '*' or char == '\n':
                    if num_champ == 4:
                        liste_ope[num_op] += (float(champ),)
                    elif num_champ == 6:
                        liste_ope[num_op] += (bool(champ),)
                    elif num_champ == 1:
                        liste_ope.append((champ,))
                    elif num_champ == 0:
                        pass
                    else:
                        liste_ope[num_op] += (champ,)
                    champ = ''
                    num_champ += 1
                else:
                    champ += char
            ligne = fichier.readline()
            ligne = decryptage(ligne)
            num_op += 1
    fichier.close()
    return liste_ope


def import_budgets(chemin_fichier: str, cle: int = CLE_CRYPTAGE) -> list:
    """
    Importe le contenu relatif aux budgets du fichier id.txt et renvoie une liste de listes qui contient :
      - La catégorie de dépenses (str),
      - Le montant alloué (float),
      - Le compte associé (str).

    Args:
        chemin_fichier: le chemin absolu du fichier id.txt
        cle: clé de cryptage du fichier (en dur)

    Returns:
        la liste des tuples contenant les différentes informations de chaque budget
    """
    fichier = open(file=chemin_fichier, mode='r', encoding="utf-8")
    liste_bud = []
    ligne = fichier.readline()
    ligne = decryptage(ligne)
    num_bud = 0
    while ligne != '':
        if ligne[0] != 'B':
            ligne = fichier.readline()
            ligne = decryptage(ligne)
        else:
            num_champ = 0
            champ = ''
            for char in ligne:
                if char == '*' or char == '\n':
                    if num_champ == 2:
                        liste_bud[num_bud].append(float(champ))
                    elif num_champ == 1:
                        liste_bud.append([champ])
                    elif num_champ == 0:
                        pass
                    else:
                        liste_bud[num_bud].append(champ)
                    champ = ''
                    num_champ += 1
                else:
                    champ += char
            ligne = fichier.readline()
            ligne = decryptage(ligne)
            num_bud += 1
    fichier.close()
    return liste_bud


def cryptage(chaine: str, cle: int = CLE_CRYPTAGE) -> str:
    """
    Fonction, avec 2 options en paramètres, qui renvoie une chaîne de caractères cryptée
    avec la méthode César, selon la clé fournie.

    Args:
        chaine: texte à crypter
        cle: clé qui sera utilisée pour le cryptage

    Returns:
        la chaine cryptée
    """
    crypte = ''
    for char in chaine:
        if char == '\n' or char == '*':
            crypte += char
        else:
            crypte += chr(ord(char) + cle)
    return crypte


def decryptage(chaine: str, cle: int = CLE_CRYPTAGE) -> str:
    """
    Fonction, avec 2 options en paramètres, qui renvoie une chaîne de caractères décryptée
    avec la méthode César, selon la clé fournie.

    Args:
        chaine: texte à décrypter
        cle: clé qui sera utilisée pour le décryptage

    Returns:
        str: la chaine décryptée
    """
    decrypte = ''
    for char in chaine:
        if char == '\n' or char == '*':
            decrypte += char
        else:
            decrypte += chr(ord(char) - cle)
    return decrypte


def login(db: dict) -> bool:
    """
    Permet à l'utilisateur de saisir ses identifiants de connexion et renvoie un booléen.

    Args:
        db: Le fichier ident.txt qui joue le role de base de données

    Returns:
        True si l'identifiant et le mot de passe sont corrects, False sinon
    """
    nb_essais = 0
    trouve = False
    while not trouve:
        identifiant = input('Veuillez saisir votre identifiant : ')
        if identifiant not in db.keys():
            print('Identifiant introuvable.')
        else:
            trouve = True

    while nb_essais < 5:
        mdp = input('Veuillez saisir votre mot de passe : ')
        if mdp != db[identifiant][0]:
            nb_essais += 1
            print(f"Mot de passe incorrect. Vous avez {5 - nb_essais} essais restants.")
        else:
            return True

    return False


def identification():
    """
    Fonction qui gère le comportement du logiciel, en fonction des entrées de l'utilisateur.

    Returns:

    """
    pass
# --Programme principal-- #


test_ident = import_idents(chemin_fichier='C:/Users/MSI/PycharmProjects/gestionBudget/src/ident.txt')
print(test_ident)

test_cpt = import_comptes(chemin_fichier='C:/Users/MSI/PycharmProjects/gestionBudget/users/19283746.txt')
print(test_cpt)

test_op = import_operations(chemin_fichier='C:/Users/MSI/PycharmProjects/gestionBudget/users/19283746.txt')
print(test_op)

test_bud = import_budgets(chemin_fichier='C:/Users/MSI/PycharmProjects/gestionBudget/users/19283746.txt')
print(test_bud)

print(login(db=test_ident))
