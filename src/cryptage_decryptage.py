# -*- coding: utf-8 -*-
#   cryptage_decryptage.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |--------Fonctions crypter, décrypter--------|   #
#   |--------------------------------------------|   #
# --Imports-- #
# --Constantes-- #
caracteres_preserves = {'\n', '*'}


# --Fonctions-- #
def cryptage(chaine: str, cle: int) -> str:
    """
    Chiffre une chaîne de caractères avec un décalage de César (décalage Unicode simple).

    Les caractères '\n' (saut de ligne) et '*' sont conservés pour éviter de briser
    la structure de fichiers multi-lignes ou à séparateurs. Ne gère que des caractères
    standards (ASCII/Unicode simples).

    Args:
        chaine (str): Texte à chiffrer.
        cle (int): Décalage à appliquer (valeur entière).

    Returns:
        str: Texte chiffré avec décalage Unicode.
    """
    crypte = ''
    for char in chaine:
        if char in caracteres_preserves:
            crypte += char
        else:
            crypte += chr((ord(char) + cle) % 1114112)      # valeur max Unicode
    return crypte


def decryptage(chaine: str, cle: int) -> str:
    """
    Décrypte une chaîne chiffrée à l'aide du chiffrement de César avec une clé donnée.

    Les caractères '\n' (saut de ligne) et '*' sont conservés pour ne pas altérer
    la structure des fichiers cryptés.

    Args:
        chaine (str): Texte chiffré à décrypter.
        cle (int): Décalage (entier) à soustraire.

    Returns:
        str: Texte d'origine, reconstruit depuis la chaîne chiffrée.
    """
    decrypte = ''
    for char in chaine:
        if char in caracteres_preserves:
            decrypte += char
        else:
            decrypte += chr((ord(char) - cle) % 1114112)    # valeur max Unicode
    return decrypte

