# -*- coding: utf-8 -*-
#   shared.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |-------Fonctions utilisées globalement------|   #
#   |--------------------------------------------|   #
# --Imports-- #
from cryptage_decryptage import cryptage
from import_donnees import import_idents
import datetime


# --Constantes-- #
dict_ident = import_idents(chemin_fichier='./ident.txt')


# --Fonctions-- #
def saisir_choix(valeurs_autorisees: set) -> int:
    """
    Invite l'utilisateur à saisir un entier appartenant à un ensemble de valeurs autorisées.

    La saisie est répétée tant que l'utilisateur n'entre pas un entier valide
    faisant partie de l'ensemble spécifié. Cette fonction garantit que le retour
    est toujours une valeur autorisée.

    Args:
        valeurs_autorisees (set): Ensemble d'entiers représentant les choix valides autorisés.

    Returns:
        int: L'entier saisi par l'utilisateur et validé comme faisant partie des valeurs autorisées.
    """
    while True:
        try:
            saisie = input("Votre choix : ")
            choix = int(saisie)
            if choix in valeurs_autorisees:
                return choix
            else:
                print("Veuillez saisir un nombre valide.")
        except ValueError:
            print("Veuillez saisir un nombre valide.")


def saisir_date() -> datetime.date:
    """
    Invite l'utilisateur à saisir une date au format jj/mm/aaaa,
    et renvoie cette date sous forme d'objet datetime.date.

    La saisie est répétée tant que le format n'est pas valide.

    Returns:
        datetime.date: La date correctement saisie et convertie.
    """ 
    while True:
        saisie = input("Date de l'opération (jj/mm/aaaa): ")
        try:
            date_op = datetime.datetime.strptime(saisie, "%d/%m/%Y").date()
            return date_op
        except ValueError:
            print("Format invalide. Veuillez entrer une date au format jj/mm/aaaa.")


def enregistrement_modif(lst_cpt: list, lst_ope: list, lst_bud: list, identifiant: int, cle_cryptage: int) -> None:
    """
    Enregistre les comptes, opérations et budgets de l'utilisateur dans son fichier personnel,
    après les avoir formatés et chiffrés avec sa clé de cryptage.

    Les données sont :
    - formatées ligne par ligne avec un préfixe (CPT, OPE, BUD),
    - concaténées dans un seul bloc de texte,
    - chiffrées avec la fonction cryptage,
    - puis écrites dans le fichier de l'utilisateur.

    Args:
        lst_cpt (list): Liste des comptes de l'utilisateur.
        lst_ope (list): Liste des opérations (tuples) de l'utilisateur.
        lst_bud (list): Liste des budgets (listes) de l'utilisateur.
        identifiant (int): Identifiant de l'utilisateur (utilisé pour nommer le fichier).
        cle_cryptage (int): Clé de cryptage utilisée pour sécuriser les données.

    Returns:
        None
    """
    lignes_cpt = ""
    lignes_ope = ""
    lignes_bud = ""
    for compte in lst_cpt:
        lignes_cpt += f"CPT*{compte}\n"
    for ope in lst_ope:
        lignes_ope += f"OPE*{ope[0].strftime("%d/%m/%Y")}*{ope[1]}*{ope[2]}*{ope[3]}*{ope[4]}*{ope[5]}*{ope[6]}\n"
    for bud in lst_bud:
        lignes_bud += f"BUD*{bud[0]}*{bud[1]}*{bud[2]}\n"

    texte = lignes_cpt + lignes_ope + lignes_bud
    contenu_fichier = cryptage(texte, cle_cryptage)

    with open(file=f'../users/{identifiant}.txt', mode='w+', encoding="utf-8") as fichier:
        fichier.write(contenu_fichier)
