# -*- coding: utf-8 -*-
#   gestion_budgets.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |-----------Phase gestion de budgets---------|   #
#   |--------------------------------------------|   #
# --Imports-- #
import calendar
import locale

from budgets import *
from import_donnees import import_comptes, import_operations, import_budgets
from shared import dict_ident, saisie_oui_non, saisir_date
from utils import enregistrement_modif

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

    choix = -1
    while choix != 0:
        # Boucle de navigation principale (choix utilisateur)
        afficher_menu_g_budgets()
        choix = saisir_choix(valeurs_autorisees={0, 1, 2, 3, 4})
        match choix:
            case 1:  # Afficher les budgets
                print(f"|-----Affichage des budgets de {nom} -----|")
                print("\n".join(
                    f"- {budget[0]} : {budget[1]}€ associé au compte : {budget[2]}" for budget in lst_bud))
            case 2:  # Ajouter un budget
                afficher = True
                while afficher or saisie_oui_non("Souhaitez-vous ajouter un autre budget ? (O/N) : "):
                    afficher = False
                    print("|-----Ajout d'un budget-----|")
                    budget = creation_budget(lst_cpt, lst_bud)
                    ajout_budget(lst_bud, budget)
            case 3:  # Modifier un budget
                afficher = True
                while afficher or saisie_oui_non("Souhaitez-vous modifier un autre budget ? (O/N) : "):
                    afficher = False
                    print("|-----Modification d'un budget-----|")
                    modifier_budget(lst_bud, lst_cpt)
            case 4:  # Rapport dépense budget
                afficher = True
                while afficher or saisie_oui_non("Souhaitez-vous consulter un autre rapport ? (O/N) : "):
                    afficher = False
                    print("|-----Rapport dépenses / budget-----|")
                    budget = selection_budget(lst_bud)
                    mois_annee = saisir_date(day=False)
                    rapport = rapport_bud_depenses(budget, lst_ope, mois_annee)
                    print(f"Pour le budget {budget[0]} au mois de "
                          f"{calendar.month_name[mois_annee.month].capitalize()} {mois_annee.year}, "
                          f"vous avez utilisé {(rapport * 100):.2f} % de votre budget.\n"
                          f"Dépense / budget :\n {rapport * budget[1]:.2f}€ / {budget[1]}€")

        enregistrement_modif(lst_cpt, lst_ope, lst_bud, identifiant, cle_cryptage)
        print("Données enregistrées dans la base de données avec succès.")

