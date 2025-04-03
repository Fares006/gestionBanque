# -*- coding: utf-8 -*-
#   import_donnees.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |-------Fonctions imports des fichiers-------|   #
#   |--------------------------------------------|   #
# --Imports-- #
import datetime
from cryptage_decryptage import CLE_CRYPTAGE, decryptage


# --Constantes-- #


# --Fonctions-- #
def import_idents(chemin_fichier: str, cle: int = CLE_CRYPTAGE) -> dict:
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
    dic_ident = dict()
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as idents:
        ligne = idents.readline()
        ligne = decryptage(ligne, cle=cle)
        while ligne != '':
            liste_intermediaire = ligne.strip('\n').split('*')
            dic_ident[liste_intermediaire[0]] = liste_intermediaire[1:]
            dic_ident[liste_intermediaire[0]][-1] = int(dic_ident[liste_intermediaire[0]][-1])
            ligne = idents.readline()
            ligne = decryptage(ligne, cle=cle)
    return dic_ident


def import_comptes(chemin_fichier: str, cle: int) -> list:
    """
    Importe le contenu relatif aux comptes du fichier id.txt et renvoie la liste des comptes.
    La liste contient directement les différents noms des comptes.

    Args:
        chemin_fichier (str): le chemin relatif du fichier id.txt
        cle (int): clé de cryptage du fichier

    Returns:
        list: la liste contenant les différents comptes de l'utilisateur
    """
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as fichier:
        liste_comptes = []
        ligne = fichier.readline()
        ligne = decryptage(ligne, cle)
        while ligne != '' and ligne[:3] == 'CPT':
            liste_intermediaire = ligne.strip('\n').split('*')
            liste_comptes.append(liste_intermediaire[1])
            ligne = fichier.readline()
            ligne = decryptage(ligne, cle)
    return liste_comptes


def import_operations(chemin_fichier: str, cle: int) -> list:
    """
    Importe le contenu relatif aux opérations du fichier id.txt et renvoie une liste de tuples qui contient :
      - Une date (datetime.date) (premier élément, lst_ope[i][0]),
      - Un libellé de l'opération (str) (deuxième élément, lst_ope[i][1]),
      - Le compte concerné (str) (troisième élément, lst_ope[i][2]),
      - Le montant de l'opération (float) (quatrième élément, lst_ope[i][3]),
      - Le mode de paiement (str) (cinquième élément, lst_ope[i][4]),
      - Un booléen indiquant si l'opération est effective (bool) (sixième élément, lst_ope[i][5]),
      - Le budget concerné (str) (septième élément, lst_ope[i][6]).

    Args:
        chemin_fichier (str): le chemin relatif du fichier id.txt
        cle (int): clé de cryptage du fichier

    Returns:
        list: la liste des tuples contenant les différentes informations concernant chaque opération
    """
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as fichier:
        liste_ope = []
        ligne = fichier.readline()
        ligne = decryptage(ligne, cle)
        while ligne != '':
            if ligne[:3] == 'OPE':
                liste_intermediaire = ligne.strip('\n').split('*')
                liste_intermediaire.pop(0)  # On se débarrasse de 'OPE'
                liste_intermediaire[0] = datetime.date(year=int(liste_intermediaire[0][6:]),
                                                       month=int(liste_intermediaire[0][3:5]),
                                                       day=int(liste_intermediaire[0][0:2]))
                liste_intermediaire[3] = float(liste_intermediaire[3])
                liste_intermediaire[5] = bool(liste_intermediaire[5])
                liste_ope.append(tuple(liste_intermediaire))
            ligne = fichier.readline()
            ligne = decryptage(ligne, cle)
    return liste_ope


def import_budgets(chemin_fichier: str, cle: int) -> list:
    """
    Importe le contenu relatif aux budgets du fichier id.txt et renvoie une liste de listes qui contient :
      - La catégorie de dépenses (str) (premier élément, lst_bud[0]),
      - Le montant alloué (float) (deuxième élément, lst_bud[1]),
      - Le compte associé (str) (troisième élément, lst_bud[2]).

    Args:
        chemin_fichier (str): le chemin relatif du fichier id.txt
        cle (int): clé de cryptage du fichier

    Returns:
        list: la liste des tuples contenant les différentes informations de chaque budget
    """
    with open(file=chemin_fichier, mode='r', encoding="utf-8") as fichier:
        liste_bud = []
        ligne = fichier.readline()
        ligne = decryptage(ligne, cle)
        while ligne != '':
            if ligne[:3] == 'BUD':
                liste_intermediaire = ligne.strip('\n').split('*')
                liste_intermediaire.pop(0)
                liste_intermediaire[1] = float(liste_intermediaire[1])
                liste_bud.append(liste_intermediaire)
            ligne = fichier.readline()
            ligne = decryptage(ligne, cle)
    return liste_bud


# --Programme principal--

