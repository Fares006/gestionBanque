# -*- coding: utf-8 -*-
#   import_donnees.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |-------Fonctions imports des fichiers-------|   #
#   |--------------------------------------------|   #
# --Imports-- #
import datetime

from constantes import CLE_CRYPTAGE
from cryptage_decryptage import decryptage
from utils import verifier_integrite_fichier


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
    # Initialise un dictionnaire vide qui contiendra les identifiants et leurs informations associées
    dic_ident = dict()

    # Ouverture du fichier contenant les identifiants cryptés en lecture (texte), avec encodage UTF-8
    with open(chemin_fichier, mode='r', encoding="utf-8") as idents:
        # Lecture ligne par ligne du fichier
        for ligne in idents:
            # Décryptage de la ligne à l'aide de la clé fournie, puis suppression des espaces et sauts de ligne
            ligne = decryptage(ligne, cle=cle).strip()

            # Découpage de la ligne en champs, à partir du séparateur '*'
            champs = ligne.split('*')

            # Vérifie que la structure minimale attendue est respectée (ex: 'Identifiant*MotDePasse*Prénom*Clé')
            if len(champs) != 4:
                continue    # Ligne ignorée si elle est mal formée

            identifiant, mdp, nom, cle_str = champs     # Attribution explicite des champs à des variables distinctes

            # Enregistrement dans le dictionnaire, avec conversion de la clé en entier
            dic_ident[identifiant] = [mdp, nom, int(cle_str)]

    # Retour du dictionnaire contenant l'ensemble des identifiants et de leurs données
    return dic_ident


def import_comptes(chemin_fichier: str, cle: int) -> list:
    """
    Importe et décrypte les lignes correspondant aux comptes d’un utilisateur
    depuis son fichier personnel, et renvoie la liste des noms de comptes.

    Le fichier est lu ligne par ligne, chaque ligne est décryptée à l’aide de la clé fournie.
    Seules les lignes commençant par "CPT" sont considérées comme valides (convention).
    La lecture s'interrompt dès qu'une ligne ne commence plus par "CPT".

    Args:
        chemin_fichier (str): Chemin vers le fichier personnel de l'utilisateur (ex: users/12345678.txt).
        cle (int): Clé de décryptage à utiliser pour chaque ligne.

    Returns:
        list: Liste des noms de comptes (str) associés à l'utilisateur.
    """
    # Vérification de l'intégrité du fichier avant traitement
    if not verifier_integrite_fichier(chemin_fichier, cle):
        print("Erreur : le fichier utilisateur semble altéré ou corrompu.")
        return []

    liste_comptes = []

    # Ouverture du fichier utilisateur en lecture (texte) avec encodage UTF-8
    with open(chemin_fichier, mode='r', encoding="utf-8") as fichier:
        # Lecture ligne par ligne du fichier
        for ligne in fichier:
            # Décryptage de la ligne à l'aide de la clé fournie, puis suppression des espaces et sauts de ligne
            ligne = decryptage(ligne, cle=cle).strip()

            # Vérifie que la ligne suit la convention d'un compte : commence par 'CPT'
            if not ligne.startswith('CPT'):
                break  # On arrête dès qu'on sort de la section comptes

            # Découpage de la ligne en champs, à partir du séparateur '*'
            champs = ligne.split('*')

            # Vérifie que la structure minimale attendue est respectée (ex: 'CPT*NomDuCompte')
            if len(champs) < 2:
                continue  # Ligne ignorée si elle est mal formée

            # Ajout du nom du compte à la liste (position 1)
            liste_comptes.append(champs[1])

    # Retour de la liste finale des comptes
    return liste_comptes


def import_operations(chemin_fichier: str, cle: int) -> list:
    """
    Importe et décrypte les opérations bancaires d’un utilisateur à partir de son fichier personnel.

    Le fichier est lu ligne par ligne, chaque ligne est décryptée à l’aide de la clé fournie.
    Seules les lignes commençant par "OPE" sont considérées comme des opérations valides.

    Chaque ligne est ensuite convertie en tuple contenant :
        - date (datetime.date) : Date de l'opération (format jj/mm/aaaa)
        - libellé (str) : Description de l'opération
        - compte (str) : Nom du compte concerné
        - montant (float) : Montant de l'opération
        - mode de paiement (str) : Type de paiement (ex: CB, CHE, VIR)
        - état (bool) : Statut de l'opération (True si passée, False sinon)
        - budget (str) : Nom du budget associé

    Args:
        chemin_fichier (str): Chemin vers le fichier personnel de l'utilisateur (ex: users/12345678.txt).
        cle (int): Clé de décryptage à utiliser pour chaque ligne.

    Returns:
        list: Liste de tuples représentant les opérations de l'utilisateur.
    """
    # Vérification de l'intégrité du fichier avant traitement
    if not verifier_integrite_fichier(chemin_fichier, cle):
        print("Erreur : le fichier utilisateur semble altéré ou corrompu.")
        return []

    from constantes import (
        IDX_OPE_DATE,
        IDX_OPE_MONTANT,
        IDX_OPE_ETAT
    )

    liste_ope = []

    # Ouverture du fichier utilisateur en lecture (texte) avec encodage UTF-8
    with open(chemin_fichier, mode='r', encoding="utf-8") as fichier:
        # Lecture ligne par ligne du fichier
        for ligne in fichier:
            # Décryptage de la ligne à l'aide de la clé fournie, puis suppression des espaces et sauts de ligne
            ligne = decryptage(ligne, cle=cle).strip()

            # Vérifie que la ligne suit la convention d'une opération : commence par 'OPE'
            if not ligne.startswith('OPE'):
                continue  # On ignore les lignes hors section opérations

            # Découpage de la ligne en champs, à partir du séparateur '*'
            champs = ligne.split('*')

            # Vérifie que la structure minimale attendue est respectée :
            # (OPE*date*libellé*compte*montant*mode*état*budget)
            if len(champs) != 8:
                continue  # Ligne ignorée si elle est mal formée

            # Suppression du préfixe 'OPE'
            champs.pop(0)

            # Conversion du champ date (au format jj/mm/aaaa) en objet datetime.date
            champs[IDX_OPE_DATE] = datetime.date(
                year=int(champs[IDX_OPE_DATE][6:]),
                month=int(champs[IDX_OPE_DATE][3:5]),
                day=int(champs[IDX_OPE_DATE][0:2])
            )

            # Conversion du montant en float
            champs[IDX_OPE_MONTANT] = float(champs[IDX_OPE_MONTANT])

            # Conversion de l'état en booléen (à partir d'une chaîne "True" ou "False")
            champs[IDX_OPE_ETAT] = champs[IDX_OPE_ETAT] == 'True'

            # Ajout de l'opération sous forme de tuple dans la liste
            liste_ope.append(tuple(champs))

    # Retour de la liste finale des opérations bancaires
    return liste_ope


def import_budgets(chemin_fichier: str, cle: int) -> list:
    """
    Importe et décrypte les budgets d’un utilisateur à partir de son fichier personnel.

    Le fichier est lu ligne par ligne, chaque ligne est décryptée à l’aide de la clé fournie.
    Seules les lignes commençant par "BUD" sont considérées comme valides (convention).

    Chaque ligne est ensuite convertie en liste contenant :
        - libellé (str) : Nom de la catégorie budgétaire
        - montant (float) : Plafond mensuel autorisé
        - compte associé (str) : Compte bancaire rattaché à ce budget

    Args:
        chemin_fichier (str): Chemin vers le fichier personnel de l'utilisateur (ex: users/12345678.txt).
        cle (int): Clé de décryptage à utiliser pour chaque ligne.

    Returns:
        list: Liste de listes représentant les budgets de l'utilisateur.
    """
    # Vérification de l'intégrité du fichier avant traitement
    if not verifier_integrite_fichier(chemin_fichier, cle):
        print("Erreur : le fichier utilisateur semble altéré ou corrompu.")
        return []

    from constantes import (
        IDX_BUD_MONTANT
    )

    liste_bud = []

    # Ouverture du fichier utilisateur en lecture (texte) avec encodage UTF-8
    with open(chemin_fichier, mode='r', encoding="utf-8") as fichier:
        # Lecture ligne par ligne du fichier
        for ligne in fichier:
            # Décryptage de la ligne à l'aide de la clé fournie, puis suppression des espaces et sauts de ligne
            ligne = decryptage(ligne, cle=cle).strip()

            # Vérifie que la ligne suit la convention d'un budget : commence par 'BUD'
            if not ligne.startswith('BUD'):
                continue  # On ignore les lignes hors section budgets

            # Découpage de la ligne en champs, à partir du séparateur '*'
            champs = ligne.split('*')

            # Vérifie que la structure minimale attendue est respectée (BUD*nom*montant*compte)
            if len(champs) != 4:
                continue  # Ligne ignorée si elle est mal formée

            # Suppression du préfixe 'BUD'
            champs.pop(0)

            # Conversion du montant en float
            champs[IDX_BUD_MONTANT] = float(champs[IDX_BUD_MONTANT])

            # Ajout du budget sous forme de liste dans la liste principale
            liste_bud.append(champs)

    # Retour de la liste finale des budgets
    return liste_bud
