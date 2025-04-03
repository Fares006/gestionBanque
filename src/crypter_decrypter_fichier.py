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
    Importe le contenu du fichier ident.txt et renvoie une liste qui contient :
    l'identifiant, le mot de passe, le nom et la clé de cryptage du fichier de l'utilisateur.

    Args:
        chemin_fichier (str): le chemin relatif du fichier ident.txt
        cle (int): clé de cryptage du fichier (en dur)

    Returns:
        dict: le dictionnaire des identifiants (et informations associées dans une liste)
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
    Procédure qui modifie un fichier pour le crypter

    Args:
        path: le chemin absolu du fichier
        cle: clé de cryptage
    """
    resultat = ''
    fichier = open(file=path, mode='r', encoding='utf-8')
    ligne = fichier.readline()
    while ligne != '':
        for char in ligne:
            resultat += cryptage(chaine=char, cle=cle)
        ligne = fichier.readline()
    fichier.close()
    fichier = open(file=path, mode='w', encoding='utf-8')
    fichier.write(resultat)
    fichier.close()


def decrypter_fichier(path: str, cle: int = 0) -> None:
    """
    Procédure qui modifie un fichier pour le décrypter

    Args:
        path: le chemin absolu du fichier
        cle: clé de cryptage
    """
    resultat = ''
    fichier = open(file=path, mode='r', encoding='utf-8')
    ligne = fichier.readline()
    while ligne != '':
        for char in ligne:
            resultat += decryptage(chaine=char, cle=cle)
        ligne = fichier.readline()
    fichier.close()
    fichier = open(file=path, mode='w', encoding='utf-8')
    fichier.write(resultat)
    fichier.close()


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
