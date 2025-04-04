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
    Importe et décrypte le contenu du fichier ident.txt contenant les informations utilisateurs.

    Chaque ligne du fichier crypté est d'abord décryptée à l'aide de la méthode de César, puis découpée.
    Les informations extraites sont :
        - identifiant (clé du dictionnaire)
        - mot de passe (str)
        - nom de l'utilisateur (str)
        - clé de cryptage associée à son fichier personnel (int)

    Args:
        chemin_fichier (str): Chemin relatif ou absolu vers le fichier ident.txt crypté.
        cle (int, optionnel): Clé de décryptage à appliquer (par défaut : CLE_CRYPTAGE).

    Returns:
        dict: Un dictionnaire contenant les identifiants comme clés (str),
              et une liste d'informations associées comme valeurs :
              [mot_de_passe (str), nom (str), cle_utilisateur (int)]
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
    Importe et décrypte les lignes correspondant aux comptes d’un utilisateur
    depuis son fichier personnel, et renvoie la liste des noms de comptes.

    Le fichier est lu ligne par ligne et chaque ligne est décryptée à l’aide de la clé fournie.
    Seules les lignes commençant par "CPT" sont traitées (convention pour les comptes).
    La lecture s'arrête dès qu'une ligne ne correspond plus à un compte.

    Args:
        chemin_fichier (str): Le chemin relatif ou absolu vers le fichier de l'utilisateur (ex: users/23456789.txt)
        cle (int): La clé de décryptage à utiliser (obtenue lors de l'identification)

    Returns:
        list: Liste des noms de comptes (str) associés à l'utilisateur.
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
    Importe et décrypte les opérations bancaires d’un utilisateur à partir de son fichier personnel.

    Seules les lignes commençant par "OPE" sont traitées. Chaque ligne est convertie en tuple contenant :
        - date (datetime.date) : Date de l'opération (au format jj/mm/aaaa)
        - libellé (str) : Description de l'opération
        - compte (str) : Nom du compte concerné
        - montant (float) : Montant de l'opération
        - mode de paiement (str) : Type de paiement (ex: CB, CHE, VIR)
        - état (bool) : Statut de l'opération (True si passée, False sinon)
        - budget (str) : Budget auquel l'opération est rattachée

    Args:
        chemin_fichier (str): Chemin relatif ou absolu vers le fichier utilisateur (ex: users/23456789.txt)
        cle (int): Clé de décryptage à utiliser pour lire le contenu du fichier.

    Returns:
        list: Liste de tuples représentant les opérations de l'utilisateur.
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
    Importe et décrypte les budgets d’un utilisateur à partir de son fichier personnel.

    Seules les lignes commençant par "BUD" sont prises en compte. Chaque ligne est convertie
    en une liste contenant les informations suivantes :
        - libellé du budget (str) : Catégorie de dépenses (ex: alimentation, loisirs)
        - montant alloué (float) : Plafond budgétaire mensuel autorisé
        - compte associé (str) : Nom du compte rattaché à ce budget

    Args:
        chemin_fichier (str): Chemin relatif ou absolu vers le fichier utilisateur (ex: users/23456789.txt)
        cle (int): Clé de décryptage à utiliser pour lire le contenu du fichier.

    Returns:
        list: Liste de listes représentant les budgets de l'utilisateur.
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

