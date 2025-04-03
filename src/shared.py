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
    Demande à l'utilisateur de saisir un entier parmi un ensemble de valeurs autorisées.

    La fonction continue de demander une saisie tant que l'utilisateur n'entre pas
    un entier valide appartenant à l'ensemble spécifié.

    Args:
        valeurs_autorisees (set): Un ensemble d'entiers représentant les choix valides.

    Returns:
        int: Le choix validé de l'utilisateur parmi les valeurs autorisées.
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
    Demande à l'utilisateur de saisir une date au format jj/mm/aaaa
    et la retourne sous forme d'objet datetime.date.

    Returns:
        datetime.date: La date saisie par l'utilisateur.
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
    Enregistre les modifications effectuées au fichier de l'utilisateur

    Args:
        lst_cpt (list): liste des comptes de l'utilisateur.
        lst_ope (list): liste des opérations de l'utilisateur.
        lst_bud (list): liste des budgets de l'utilisateur.
        identifiant (str): identifiant de l'utilisateur.
        cle_cryptage (int): clé de cryptage unique à l'utilisateur.

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
