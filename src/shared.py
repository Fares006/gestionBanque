# -*- coding: utf-8 -*-
#   shared.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |-------Fonctions utilisées globalement------|   #
#   |--------------------------------------------|   #
# --Imports-- #
import datetime
from import_donnees import import_idents

# --Constantes-- #
# --Variables-- #
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
            # Demande de saisie à l'utilisateur
            saisie = input("Votre choix : ")
            choix = int(saisie)

            # Vérifie que la valeur saisie est bien dans l'ensemble autorisé
            if choix in valeurs_autorisees:
                return choix
            else:
                print(f"Valeur non autorisée. Veuillez choisir parmi : {sorted(valeurs_autorisees)}")
        except ValueError:
            # Gestion d'une saisie non convertible en entier
            print("Entrée invalide. Veuillez saisir un nombre entier.")


def saisir_date(day: bool = True, month: bool = True, year: bool = True) -> datetime.date:
    """
    Invite l'utilisateur à saisir une date au format attendu selon les composantes activées.

    Le format de saisie s'ajuste selon les paramètres :
    - day=True, month=True, year=True   → jj/mm/aaaa
    - day=False, month=True, year=True  → mm/aaaa
    - day=False, month=False, year=True → aaaa

    La saisie est répétée jusqu'à ce qu'une date valide soit fournie.

    Args:
        day (bool): Si True, demande le jour.
        month (bool): Si True, demande le mois.
        year (bool): Si True, demande l'année.

    Returns:
        datetime.date: L'objet date correspondant à la saisie.
                       Les valeurs manquantes sont fixées par défaut à :
                       - 1 pour le jour
                       - janvier pour le mois
    """
    # Construction du format d'affichage et de parsing selon les paramètres
    if day and month and year:
        prompt = "Date (jj/mm/aaaa) : "
        fmt = "%d/%m/%Y"
    elif not day and month and year:
        prompt = "Date (mm/aaaa) : "
        fmt = "%m/%Y"
    elif not day and not month and year:
        prompt = "Année (aaaa) : "
        fmt = "%Y"
    else:
        raise ValueError("Configuration de saisie invalide : year doit être True.")

    while True:
        saisie = input(prompt)
        try:
            date_obj = datetime.datetime.strptime(saisie, fmt)

            # On complète la date avec les valeurs par défaut si nécessaire
            return datetime.date(
                year=date_obj.year,
                month=date_obj.month if month else 1,
                day=date_obj.day if day else 1
            )
        except ValueError:
            print(f"Format invalide. Veuillez entrer une date au format {prompt.strip(': ')}.")



def saisie_oui_non(prompt: str) -> bool:
    reponse = ""
    while reponse.upper() not in ['O', 'N']:
        reponse = input(prompt).strip()
        if reponse.upper() not in ['O', 'N']:
            print("Veuillez répondre par 'O' pour Oui ou 'N' pour Non.")
    return reponse.upper() == 'O'



