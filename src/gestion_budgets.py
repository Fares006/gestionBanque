# -*- coding: utf-8 -*-
#   gestion_budgets.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |-----------Phase gestion de budgets---------|   #
#   |--------------------------------------------|   #
# --Imports-- #
import datetime
import calendar
import locale

from import_donnees import import_comptes, import_operations, import_budgets
from shared import enregistrement_modif, dict_ident
from budgets import *

try:
    locale.setlocale(locale.LC_TIME, 'French_France.1252')
except locale.Error:
    pass


# --Constantes-- #

# --Fonctions-- #
def afficher_menu_g_budgets() -> None:
    """
    Affiche en console le menu des actions disponibles dans la gestion des budgets.

    Le menu propose à l'utilisateur les options suivantes :
        0. Revenir en arrière
        1. Afficher les budgets existants
        2. Ajouter un nouveau budget
        3. Modifier un budget existant
        4. Afficher la différence entre les dépenses et le budget

    Returns:
        None
    """
    print("\nDe quelle fonctionnalité avez-vous besoin ?")
    print("0. Revenir en arrière\n"
          "1. Afficher les budgets\n"
          "2. Ajouter un budget\n"
          "3. Modifier un budget\n"
          "4. Afficher différence dépenses/budget\n")


def gestion_budgets(identifiant: int) -> None:
    """
    Gère toutes les interactions liées à la gestion des budgets de l'utilisateur connecté.

    Cette fonction propose un menu interactif permettant à l'utilisateur de :
    - Visualiser ses budgets existants
    - Ajouter un nouveau budget lié à un compte
    - Modifier un budget existant (libellé, montant, compte)
    - Consulter un rapport mensuel des dépenses pour un budget donné

    Chaque action est répétable via des boucles interactives.
    Toutes les modifications sont automatiquement sauvegardées dans le fichier utilisateur (avec chiffrement).

    Args:
        identifiant (int): Identifiant de l'utilisateur connecté (utilisé pour accéder à ses données personnelles).

    Returns:
        None
    """
    cle_cryptage = dict_ident[identifiant][-1]
    lst_cpt = import_comptes(chemin_fichier=f'../users/{identifiant}.txt', cle=cle_cryptage)
    lst_ope = import_operations(chemin_fichier=f'../users/{identifiant}.txt', cle=cle_cryptage)
    lst_bud = import_budgets(chemin_fichier=f'../users/{identifiant}.txt', cle=cle_cryptage)
    nom = dict_ident[identifiant][1]

    afficher_menu_g_budgets()
    choix = saisir_choix(valeurs_autorisees={0, 1, 2, 3, 4})

    while choix != 0:
        # Boucle de navigation principale (choix utilisateur)
        match choix:
            case 1:  # Afficher les budgets
                print(f"|-----Affichage des budgets de {nom} -----|")
                print("\n".join(
                    f"- {budget[0]} : {budget[1]}€ associé au compte : {budget[2]}" for budget in lst_bud))
            case 2:  # Ajouter un budget
                boucle = 'O'
                while boucle.upper() != 'N':
                    print("|-----Ajout d'un budget-----|")
                    budget = creation_budget(lst_cpt, lst_bud)
                    ajout_budget(lst_bud, budget)

                    boucle = ""
                    while boucle.upper() not in ['O', 'N']:
                        boucle = input("Souhaitez-vous ajouter un autre budget ? (O/N) : ")
                        if boucle.upper() not in ['O', 'N']:
                            print("Veuillez répondre par 'O' pour Oui ou 'N' pour Non.")
            case 3:  # Modifier un budget
                boucle = 'O'
                while boucle.upper() != 'N':
                    print("|-----Modification d'un budget-----|")
                    modifier_budget(lst_bud, lst_cpt)

                    boucle = ""
                    while boucle.upper() not in ['O', 'N']:
                        boucle = input("Souhaitez-vous modifier un autre budget ? (O/N) : ")
                        if boucle.upper() not in ['O', 'N']:
                            print("Veuillez répondre par 'O' pour Oui ou 'N' pour Non.")
            case 4:  # Rapport dépense budget
                boucle = 'O'
                while boucle.upper() != 'N':
                    print("|-----Rapport dépenses / budget-----|")
                    budget = selection_budget(lst_bud)

                    saisie_valide = False
                    while not saisie_valide:
                        saisie = input("Entrez le mois et l'année (mm/yyyy) : ")
                        try:
                            date_obj = datetime.datetime.strptime(saisie, "%m/%Y")
                            mois = date_obj.month
                            annee = date_obj.year
                            saisie_valide = True
                        except ValueError:
                            print("Format invalide. Veuillez entrer une date au format mm/yyyy.")

                    rapport = rapport_bud_depenses(budget, lst_ope, mois, annee)
                    print(f"Pour le budget {budget[0]} au mois de {calendar.month_name[mois].capitalize()} {annee}, "
                          f"vous avez utilisé {(rapport * 100):.2f} % de votre budget.\n"
                          f"Dépense / budget :\n {rapport * budget[1]:.2f}€ / {budget[1]}€")

                    boucle = ""
                    while boucle.upper() not in ['O', 'N']:
                        boucle = input("Souhaitez-vous consulter un autre rapport ? (O/N) : ")
                        if boucle.upper() not in ['O', 'N']:
                            print("Veuillez répondre par 'O' pour Oui ou 'N' pour Non.")

        enregistrement_modif(lst_cpt, lst_ope, lst_bud, identifiant, cle_cryptage)
        afficher_menu_g_budgets()
        choix = saisir_choix(valeurs_autorisees={0, 1, 2, 3, 4})
