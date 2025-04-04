# -*- coding: utf-8 -*-
#   identification.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |------------Phase d'identification----------|   #
#   |--------------------------------------------|   #
# --Imports-- #
from shared import dict_ident

# --Constantes-- #


# --Fonctions-- #
def get_identifiant() -> str:
    """
    Demande à l'utilisateur de saisir un identifiant valide.

    L'utilisateur dispose de 5 tentatives maximum pour entrer un identifiant :
    - L'identifiant doit comporter exactement 8 caractères.
    - Il doit être présent dans le dictionnaire global dict_ident.

    Si un identifiant valide est saisi, il est retourné immédiatement.
    Sinon, une chaîne vide est renvoyée après épuisement des essais.

    Returns:
        str: L'identifiant saisi et validé, ou une chaîne vide en cas d'échec.
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
    Demande à l'utilisateur de saisir son mot de passe associé à l'identifiant donné.

    L'utilisateur dispose de 5 tentatives maximum pour entrer un mot de passe valide :
    - Le mot de passe doit comporter exactement 6 caractères.
    - Il doit correspondre à celui enregistré dans dict_ident pour l'identifiant fourni.

    Si le mot de passe est correct, il est retourné.
    En cas d'échec après 5 essais, une chaîne vide est renvoyée.

    Args:
        identifiant (str): L'identifiant utilisateur déjà validé (obtenu via get_identifiant).

    Returns:
        str: Le mot de passe saisi et validé, ou une chaîne vide en cas d'échec.
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
    Gère le processus de connexion d'un utilisateur à partir de son identifiant et de son mot de passe.

    La fonction appelle successivement :
    - get_identifiant() pour valider l'identifiant saisi.
    - get_mdp() pour valider le mot de passe associé à l'identifiant.

    L'utilisateur dispose de 5 tentatives pour chaque étape. En cas de réussite, la connexion est approuvée.

    Returns:
        tuple:
            - bool : True si l'identification est réussie, False sinon.
            - str : L'identifiant saisi (vide si l'utilisateur échoue à s'identifier).
    """
    identifiant = get_identifiant()
    if identifiant != '':
        mdp = get_mdp(identifiant)
        if mdp != '':
            return True, identifiant
    return False, identifiant


# --Programme principal--
