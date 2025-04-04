# -*- coding: utf-8 -*-
#   cryptage_decryptage.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |--------Fonctions crypter, décrypter--------|   #
#   |--------------------------------------------|   #
# --Imports-- #


# --Constantes-- #
CLE_CRYPTAGE = 23


# --Fonctions-- #

def cryptage(chaine: str, cle: int) -> str:
    """
    Crypte une chaîne de caractères à l'aide du chiffrement de César avec une clé donnée.

    Chaque caractère (sauf '\n' et '*') est décalé dans la table Unicode selon la clé fournie.
    Les caractères spéciaux '\n' (saut de ligne) et '*' sont conservés tels quels pour
    préserver la structure des fichiers.

    Args:
        chaine (str): Le texte brut à crypter.
        cle (int): La clé de cryptage (valeur entière du décalage à appliquer).

    Returns:
        str: La chaîne cryptée résultante.
    """
    crypte = ''
    for char in chaine:
        if char == '\n' or char == '*':
            crypte += char
        else:
            crypte += chr(ord(char) + cle)
    return crypte


def decryptage(chaine: str, cle: int) -> str:
    """
    Décrypte une chaîne de caractères à l'aide du chiffrement de César avec une clé donnée.

    Chaque caractère (sauf '\n' et '*') est décalé dans la table Unicode en soustrayant la clé fournie.
    Les caractères spéciaux '\n' (saut de ligne) et '*' sont conservés tels quels pour
    préserver la structure des fichiers cryptés.

    Args:
        chaine (str): Le texte crypté à décrypter.
        cle (int): La clé de décryptage (valeur entière du décalage inversé à appliquer).

    Returns:
        str: La chaîne décryptée résultante.
    """

    decrypte = ''
    for char in chaine:
        if char == '\n' or char == '*':
            decrypte += char
        else:
            decrypte += chr(ord(char) - cle)
    return decrypte
