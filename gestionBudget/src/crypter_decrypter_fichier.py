#   |--------------------------------------------|   #
#   |--------Gestion de Budget (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |--------------------------------------------|   #
# --Imports-- #
from main import cryptage, decryptage, CLE_CRYPTAGE
# --Constantes-- #


# --Fonctions-- #
def crypter_fichier(path: str) -> None:
    """
    Procédure qui modifie un fichier pour le crypter

    Args:
        path: le chemin absolu du fichier
    """
    resultat = ''
    fichier = open(file=path, mode='r', encoding='utf-8')
    ligne = fichier.readline()
    while ligne != '':
        for char in ligne:
            resultat += cryptage(chaine=char, cle=CLE_CRYPTAGE)
        ligne = fichier.readline()
    fichier.close()
    fichier = open(file=path, mode='w', encoding='utf-8')
    fichier.write(resultat)
    fichier.close()


def decrypter_fichier(path: str) -> None:
    """
    Procédure qui modifie un fichier pour le décrypter

    Args:
        path: le chemin absolu du fichier
    """
    resultat = ''
    fichier = open(file=path, mode='r', encoding='utf-8')
    ligne = fichier.readline()
    while ligne != '':
        for char in ligne:
            resultat += decryptage(chaine=char, cle=CLE_CRYPTAGE)
        ligne = fichier.readline()
    fichier.close()
    fichier = open(file=path, mode='w', encoding='utf-8')
    fichier.write(resultat)
    fichier.close()


# --Programme principal-- #

