# -*- coding: utf-8 -*-
#   gestion_comptes.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |-----------Phase gestion de comptes---------|   #
#   |--------------------------------------------|   #
# --Imports-- #
from comptes import *
from import_donnees import *
from shared import saisir_choix, saisie_oui_non, dict_ident
from utils import enregistrement_modif

# --Constantes-- #


# --Fonctions-- #
def afficher_menu_g_comptes() -> None:
    """
    Affiche en console le menu des actions disponibles dans la gestion des comptes.
    Cette fonction est appelée à chaque fin de boucle pour réafficher les options.

    Le menu propose à l'utilisateur les options suivantes :
        0. Revenir en arrière
        1. Afficher le solde d'un compte
        2. Ajouter un nouveau compte
        3. Afficher les opérations d'un compte
        4. Ajouter une nouvelle opération
        5. Effectuer un virement entre comptes

    Returns:
        None
    """

    print("\nDe quelle fonctionnalité avez-vous besoin ?")
    print("0. Revenir en arrière\n"
          "1. Afficher le solde du compte\n"
          "2. Ajouter un compte\n"
          "3. Afficher les opérations d'un compte\n"
          "4. Ajouter une opération\n"
          "5. Faire un virement\n")


def gestion_comptes(identifiant: int) -> None:
    """
    Gère toutes les interactions liées à la gestion des comptes bancaires d'un utilisateur.

    Cette fonction propose un menu permettant à l'utilisateur authentifié de :
    - Consulter le solde de ses comptes
    - Ajouter un nouveau compte avec un solde initial
    - Afficher les opérations associées à un compte (avec ou sans filtre par date)
    - Ajouter une nouvelle opération
    - Effectuer un virement entre deux comptes

    Chaque fonctionnalité est réutilisable grâce à une boucle interactive.
    Toutes les modifications sont automatiquement enregistrées dans le fichier utilisateur
    (avec chiffrement) après chaque action.

    Args:
        identifiant (int): Identifiant de l'utilisateur connecté (utilisé pour accéder à ses données chiffrées).

    Returns:
        None
    """
    cle_cryptage = dict_ident[identifiant][-1]
    lst_cpt = import_comptes(chemin_fichier=f'../users/{identifiant}.txt', cle=cle_cryptage)
    lst_ope = import_operations(chemin_fichier=f'../users/{identifiant}.txt', cle=cle_cryptage)
    lst_bud = import_budgets(chemin_fichier=f'../users/{identifiant}.txt', cle=cle_cryptage)
    dict_soldes = calcul_dict_soldes(lst_cpt, lst_ope)

    choix = -1
    while choix != 0:
        # Boucle de navigation principale (choix utilisateur)
        afficher_menu_g_comptes()
        choix = saisir_choix(valeurs_autorisees={0, 1, 2, 3, 4, 5})

        match choix:
            case 1:  # Solde
                afficher = True
                while afficher or saisie_oui_non("Souhaitez-vous consulter le solde d’un autre compte ? (O/N) : "):
                    afficher = False
                    choix_compte = selection_compte(lst_cpt, courant=False)
                    solde = dict_soldes[choix_compte]
                    print(f"\n|-----Solde d'un compte-----|\n"
                          f"| Vous avez {solde:.2f} € sur votre compte \"{choix_compte}\" |")

            case 2:  # Ajout compte
                afficher = True
                while afficher or saisie_oui_non("Souhaitez-vous ajouter un autre compte ? (O/N) : "):
                    afficher = False
                    print("|-----Ajout de compte-----|")
                    nouveau_compte = input("Quel est le nom du nouveau compte ? : ")
                    succes_ajout = ajout_compte(lst_cpt, nouveau_compte.title())
                    if succes_ajout and saisie_oui_non("Souhaitez-vous charger le solde initial ? (O/N) : "):
                        virement_solde_init = creer_virement(lst_cpt, dict_soldes, is_nouveau_compte=True,
                                                             nouveau_compte=nouveau_compte.title())
                        ajout_virement(virement_solde_init, lst_ope, dict_soldes)

            case 3:  # Afficher les opérations d'un compte
                afficher = True
                while afficher or saisie_oui_non("Souhaitez-vous consulter un autre compte ? (O/N) : "):
                    afficher = False
                    print("|-----Affichage des opérations d'un compte-----|")
                    compte = selection_compte(lst_cpt, courant=False)
                    filtrer = saisie_oui_non("Voulez-vous filtrer les opérations entre deux dates ? (O/N) : ")
                    afficher_operations(lst_ope, compte, filtre_date=filtrer)

            case 4:  # Ajouter une opération
                afficher = True
                while afficher or saisie_oui_non("Souhaitez-vous ajouter une autre opération ? (O/N) : "):
                    afficher = False
                    print("|-----Ajout d'opération-----|")
                    operation = creation_operation(lst_cpt, lst_bud)
                    ajout_operation(lst_ope, operation)
                    print(f"Opération :\n{formatter_operation(operation)}\najoutée avec succès.")

            case 5:  # Effectuer un virement entre comptes
                afficher = True
                while afficher or saisie_oui_non("Souhaitez-vous effectuer un autre virement ? (O/N) : "):
                    afficher = False
                    print("|-----Virement compte A -> compte B-----|")
                    nouveau_virement = creer_virement(lst_cpt, dict_soldes)
                    ajout_virement(nouveau_virement, lst_ope, dict_soldes)

        lst_ope = sorted(lst_ope, key=lambda ope: ope[0])  # Trie chronologiquement les opérations avant enregistrement
        enregistrement_modif(lst_cpt, lst_ope, lst_bud, identifiant, cle_cryptage)
        print("Données enregistrées dans la base de données avec succès.")

