# -*- coding: utf-8 -*-
#   |--------------------------------------------|   #
#   |--------Gestion de Budget (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |-----Cryptage des fichiers utilisateurs-----|   #
#   |--------------------------------------------|   #
# --Imports-- #
from cryptage_decryptage import cryptage, decryptage, CLE_CRYPTAGE
from import_donnees import import_idents


# --Constantes-- #

# --Fonctions-- #
def import_idents_clair(chemin_fichier: str) -> dict:
    """
    Importe le contenu d'un fichier d'identifiants non crypté (format texte clair)
    et retourne un dictionnaire associant chaque identifiant à ses informations.

    Chaque ligne du fichier doit être au format :
        identifiant*mot_de_passe*nom_utilisateur*cle_cryptage

    Args:
        chemin_fichier (str): Chemin relatif ou absolu vers le fichier ident_clair.txt

    Returns:
        dict: Un dictionnaire dont les clés sont les identifiants (str) et les valeurs des listes :
              [mot_de_passe (str), nom (str), cle_cryptage (int)]
    """
    # Ouverture du fichier et initialisation des variables nécessaires
    dic_ident_clair = dict()
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as idents:
        ligne = idents.readline()
        while ligne != '':
            liste_intermediaire = ligne.strip('\n').split('*')
            dic_ident_clair[liste_intermediaire[0]] = liste_intermediaire[1:]
            dic_ident_clair[liste_intermediaire[0]][-1] = int(dic_ident_clair[liste_intermediaire[0]][-1])
            ligne = idents.readline()
    return dic_ident_clair


def crypter_fichier(path: str, cle: int) -> None:
    """
    Crypte le contenu d'un fichier texte à l'aide du chiffrement de César, en écrasant le fichier original.

    Chaque caractère du fichier (sauf '\n' et '*', selon la fonction cryptage) est transformé
    en utilisant la clé fournie. Le fichier est ensuite réécrit avec son contenu crypté.

    Args:
        path (str): Le chemin absolu (ou relatif) vers le fichier à crypter.
        cle (int): La clé de cryptage (valeur entière de décalage).

    Returns:
        None
    """
    resultat = ''
    with open(file=path, mode='r', encoding='utf-8') as fichier:
        ligne = fichier.readline()
        while ligne != '':
            for char in ligne:
                resultat += cryptage(chaine=char, cle=cle)
            ligne = fichier.readline()

    with open(file=path, mode='w', encoding='utf-8') as fichier:
        fichier.write(resultat)


def decrypter_fichier(path: str, cle: int = 0) -> None:
    """
    Décrypte le contenu d’un fichier texte à l’aide du chiffrement de César,
    en écrasant le fichier original.

    Chaque caractère du fichier (sauf '\n' et '*', selon la fonction decryptage)
    est transformé en soustrayant la clé fournie. Le fichier est ensuite réécrit
    avec son contenu décrypté.

    Args:
        path (str): Chemin absolu (ou relatif) vers le fichier à décrypter.
        cle (int): Clé de décryptage (valeur entière du décalage inverse à appliquer). Par défaut : 0.

    Returns:
        None
    """
    resultat = ''
    with open(file=path, mode='r', encoding='utf-8') as fichier:
        ligne = fichier.readline()
        while ligne != '':
            for char in ligne:
                resultat += decryptage(chaine=char, cle=cle)
            ligne = fichier.readline()

    with open(file=path, mode='w', encoding='utf-8') as fichier:
        fichier.write(resultat)


# --Programme principal-- #
if __name__ == '__main__':
    #  ---Bloc de cryptage de tous les fichiers--- :
    # dict_ident_clair = import_idents_clair(chemin_fichier='./ident_clair.txt')
    # liste_ident = []
    # for id in dict_ident_clair.keys():
    #     liste_ident.append(id)
    # crypter_fichier(path='./ident.txt', cle=CLE_CRYPTAGE)
    # for id in liste_ident:
    #     crypter_fichier(path=f'../users/{id}.txt', cle=dict_ident_clair[id][-1])

    #   ---Bloc de décryptage de tous les fichiers---
    # dict_ident = import_idents(chemin_fichier='./ident.txt')
    # liste_ident = []
    # for id in dict_ident.keys():
    #     liste_ident.append(id)
    # decrypter_fichier(path='./ident.txt', cle=CLE_CRYPTAGE)
    # for id in liste_ident:
    #     decrypter_fichier(path=f'../users/{id}.txt', cle=dict_ident[id][-1])
    pass
