# -*- coding: utf-8 -*-
#   |--------------------------------------------|   #
#   |--------Gestion de Budget (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |-----Cryptage des fichiers utilisateurs-----|   #
#   |--------------------------------------------|   #
# --Imports-- #
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
    Crypte le contenu d'un fichier texte à l'aide du chiffrement de César.
    Le fichier est modifié directement (en l'écrasant).

    Args:
        path (str): Chemin vers le fichier à crypter.
        cle (int): Clé de décalage.
    """
    with open(path, 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()

    contenu_crypte = cryptage(contenu, cle)

    with open(path, 'w', encoding='utf-8') as fichier:
        fichier.write(contenu_crypte)



def decrypter_fichier(path: str, cle: int) -> None:
    """
    Décrypte le contenu d’un fichier texte à l’aide du chiffrement de César.
    Le fichier est modifié directement (en l’écrasant).

    Args:
        path (str): Chemin vers le fichier à décrypter.
        cle (int): Clé de décalage inverse à appliquer.
    """
    with open(path, 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()

    contenu_decrypte = decryptage(contenu, cle)

    with open(path, 'w', encoding='utf-8') as fichier:
        fichier.write(contenu_decrypte)


# --Programme principal-- #
if __name__ == '__main__':
    from constantes import CLE_CRYPTAGE
    from cryptage_decryptage import cryptage, decryptage
    from import_donnees import import_idents  # pour les identifiants cryptés

    choix = input("Souhaitez-vous crypter ou décrypter ? (C/D) : ").strip().upper()

    if choix == 'C':
        print("Cryptage en cours...")
        dict_ident_clair = import_idents_clair('./ident_clair.txt')
        liste_ident = list(dict_ident_clair.keys())

        crypter_fichier('./ident.txt', cle=CLE_CRYPTAGE)
        for ident in liste_ident:
            cle_perso = dict_ident_clair[ident][-1]
            crypter_fichier(f'../users/{ident}.txt', cle=cle_perso)

        print("Tous les fichiers ont été cryptés avec succès.")

    elif choix == 'D':
        print("Décryptage en cours...")
        dict_ident = import_idents('./ident.txt')
        liste_ident = list(dict_ident.keys())

        decrypter_fichier('./ident.txt', cle=CLE_CRYPTAGE)
        for ident in liste_ident:
            cle_perso = dict_ident[ident][-1]
            decrypter_fichier(f'../users/{ident}.txt', cle=cle_perso)

        print("Tous les fichiers ont été décryptés avec succès.")

    else:
        print("Choix invalide. Veuillez entrer 'C' pour crypter ou 'D' pour décrypter.")

