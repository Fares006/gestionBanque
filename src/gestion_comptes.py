# -*- coding: utf-8 -*-
#   gestion_comptes.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |-----------Phase gestion de comptes---------|   #
#   |--------------------------------------------|   #
# --Imports-- #
from import_donnees import *
from comptes import *
from shared import saisir_choix, enregistrement_modif, dict_ident


# --Constantes-- #

# --Fonctions-- #
def afficher_menu_g_comptes() -> None:
    """
    Affiche le menu pour la gestion des comptes.

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

    Cette fonction permet à l'utilisateur authentifié de :
    - Consulter le solde de ses comptes
    - Ajouter un nouveau compte avec un solde initial
    - Afficher les opérations liées à un compte, avec ou sans filtre par date
    - Ajouter une nouvelle opération bancaire
    - Effectuer un virement entre deux comptes

    Chaque action peut être répétée plusieurs fois grâce à un système de boucles interactives.
    Les modifications effectuées sont automatiquement enregistrées dans le fichier utilisateur après chaque action.

    Args:
        identifiant (int): L'identifiant de l'utilisateur connecté, utilisé pour accéder à ses données chiffrées.

    Returns:
        None
    """
    cle_cryptage = dict_ident[identifiant][-1]
    lst_cpt = import_comptes(chemin_fichier=f'../users/{identifiant}.txt', cle=cle_cryptage)
    lst_ope = import_operations(chemin_fichier=f'../users/{identifiant}.txt', cle=cle_cryptage)
    lst_bud = import_budgets(chemin_fichier=f'../users/{identifiant}.txt', cle=cle_cryptage)
    dict_soldes = calcul_dict_soldes(lst_cpt, lst_ope)

    afficher_menu_g_comptes()
    choix = saisir_choix(valeurs_autorisees={0, 1, 2, 3, 4, 5})

    while choix != 0:
        match choix:
            case 1:  # Solde
                boucle = 'O'
                while boucle.upper() != 'N':
                    choix_compte = selection_compte(lst_cpt, courant=False)
                    solde = dict_soldes[choix_compte]
                    print(f"\n|-----Solde d'un compte-----|\n"
                          f"| Vous avez {solde:.2f} € sur votre compte \"{choix_compte}\" |")

                    boucle = ""
                    while boucle.upper() not in ['O', 'N']:
                        boucle = input("Souhaitez-vous consulter le solde d'un autre compte ? (O/N) : ")
                        if boucle.upper() not in ['O', 'N']:
                            print("Veuillez répondre par 'O' pour Oui ou 'N' pour Non.")
            case 2:  # Ajout compte
                boucle = 'O'
                while boucle.upper() != 'N':
                    print("|-----Ajout de compte-----|")
                    nouveau_compte = input("Quel est le nom du nouveau compte ? : ")
                    succes_ajout = ajout_compte(lst_cpt, nouveau_compte)
                    if succes_ajout:
                        solde_initial = float(input("Quel est le solde initial de ce nouveau compte ? : "))
                        dict_soldes[nouveau_compte] = solde_initial
                        ajout_operation(lst_ope, operation=(datetime.date.today(),
                                                            f"Ouverture du compte {nouveau_compte}",
                                                            nouveau_compte,
                                                            solde_initial,
                                                            "Application",
                                                            True,
                                                            "..."))
                    boucle = ""
                    while boucle.upper() not in ['O', 'N']:
                        boucle = input("Souhaitez-vous ajouter un autre compte ? (O/N) : ")
                        if boucle.upper() not in ['O', 'N']:
                            print("Veuillez répondre par 'O' pour Oui ou 'N' pour Non.")
            case 3:  # Afficher les opérations d'un compte
                boucle = 'O'
                while boucle.upper() != 'N':
                    print("|-----Affichage des opérations d'un compte-----|")
                    compte = selection_compte(lst_cpt, courant=False)
                    choix_filtrer_date = ""
                    while choix_filtrer_date.upper() not in {'O', 'N'}:
                        choix_filtrer_date = input("Voulez-vous filtrer les opérations entre deux dates ? (O/N) : ")
                        if choix_filtrer_date.upper() not in {'O', 'N'}:
                            print("Veuillez répondre par 'O' pour Oui ou 'N' pour Non.")
                    afficher_operations(lst_ope, compte, filtre_date=(choix_filtrer_date.upper() == 'O'))

                    boucle = ""
                    while boucle.upper() not in ['O', 'N']:
                        boucle = input("Souhaitez-vous consulter un autre compte ? (O/N) : ")
                        if boucle.upper() not in ['O', 'N']:
                            print("Veuillez répondre par 'O' pour Oui ou 'N' pour Non.")
            case 4:  # Ajouter une opération
                boucle = 'O'
                while boucle.upper() != 'N':
                    print("|-----Ajout d'opération-----|")
                    operation = creation_operation(lst_cpt, lst_bud)
                    ajout_operation(lst_ope, operation)
                    affichage_ope = formatter_operation(operation)
                    print(f"Opération :\n{affichage_ope}\najoutée avec succès.")

                    boucle = ""
                    while boucle.upper() not in ['O', 'N']:
                        boucle = input("Souhaitez-vous ajouter une autre opération ? (O/N) : ")
                        if boucle.upper() not in ['O', 'N']:
                            print("Veuillez répondre par 'O' pour Oui ou 'N' pour Non.")
            case 5:  # Effectuer un virement entre comptes
                boucle = 'O'
                while boucle.upper() != 'N':
                    print("|-----Virement compte A -> compte B-----|")
                    nouveau_virement = creer_virement(lst_cpt, dict_soldes)
                    ajout_virement(nouveau_virement, lst_ope, dict_soldes)

                    boucle = ""
                    while boucle.upper() not in ['O', 'N']:
                        boucle = input("Souhaitez-vous effectuer un autre virement ? (O/N) : ")
                        if boucle.upper() not in ['O', 'N']:
                            print("Veuillez répondre par 'O' pour Oui ou 'N' pour Non.")

        lst_ope = sorted(lst_ope, key=lambda ope: ope[0])  # Trie la liste des opérations par rapport à leur date
        enregistrement_modif(lst_cpt, lst_ope, lst_bud, identifiant, cle_cryptage)

        afficher_menu_g_comptes()
        choix = saisir_choix(valeurs_autorisees={0, 1, 2, 3, 4, 5})

