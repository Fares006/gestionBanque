# -*- coding: utf-8 -*-
#   identification.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |------------Phase d'identification----------|   #
#   |--------------------------------------------|   #
# --Imports-- #
from import_donnees import import_idents
from shared import dict_ident

# --Constantes-- #


# --Fonctions-- #
def get_identifiant() -> str:
    """
    Permet à l'utilisateur de saisir son identifiant.

    Args:

    Returns:
        str: renvoie l'identifiant de l'utilisateur validé
    """
    identifiant_trouve = False
    nb_essais = 0
    while nb_essais < 5 and not identifiant_trouve:
        identifiant = input('Veuillez saisir votre identifiant : ')
        if len(identifiant) != 8:
            print('L\'identifiant doit faire 8 caractères.')
        elif identifiant not in dict_ident.keys():
            nb_essais += 1
            print(f"Identifiant introuvable. Vous avez {5 - nb_essais} essais restants.")
        else:
            return identifiant
    return ''


def get_mdp(identifiant: str) -> str:
    """
    Permet à l'utilisateur de saisir son mot de passe.

    Args:
        identifiant (str): l'id de l'utilisateur validé (acquis par la fonction get_identifiant())

    Returns:
        str: renvoie le mot de passe de l'utilisateur validé
    """
    connecte = False
    nb_essais = 0
    while nb_essais < 5 and not connecte:
        mdp = input('Veuillez saisir votre mot de passe : ')
        if len(mdp) != 6:
            print('Le mot de passe doit faire 6 caractères.')
        elif mdp != dict_ident[identifiant][0]:
            nb_essais += 1
            print(f"Mot de passe incorrect. Vous avez {5 - nb_essais} essais restants.")
        else:
            return mdp
    return ''


def identification() -> tuple:
    """
    Permet la connexion d'un utilisateur en utilisant le couple identifiant mot de passe.

    Args:

    Returns:
        tuple: composé de l'approbation ou non de la connexion ainsi que l'identifiant saisi.
    """
    identifiant = get_identifiant()
    if identifiant != '':
        mdp = get_mdp(identifiant)
        if mdp != '':
            return True, identifiant
    return False, identifiant


# --Programme principal--
if __name__ == "__main__":
    dict_ident = import_idents(chemin_fichier='./ident.txt')
