#   |--------------------------------------------|   #
#   |--------Gestion de Budget (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |--------------------------------------------|   #

# --Imports-- #
from src.main import import_idents, cryptage, decryptage, CLE_CRYPTAGE
# --Constantes-- #
dict_ident = import_idents(chemin_fichier='./ident.txt')

# --Fonctions-- #
def crypter_fichier(path: str, cle: int) -> None:
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
    liste_ident = []
    for id in dict_ident.keys():
        liste_ident.append(id)

    #   Bloc de cryptage de tous les fichiers :
    # crypter_fichier(path='./ident.txt', cle=CLE_CRYPTAGE)
    # for id in liste_ident:
    #     crypter_fichier(path=f'../users/{id}.txt', cle=dict_ident[id][-1])

    #   Bloc de décryptage de tous les fichiers :
    # decrypter_fichier(path='./ident.txt', cle=CLE_CRYPTAGE)
    # for id in liste_ident:
    #     decrypter_fichier(path=f'../users/{id}.txt', cle=dict_ident[id][-1])
    pass
