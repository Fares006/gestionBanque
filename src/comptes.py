# -*- coding: utf-8 -*-
#   comptes.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |----------Phase gestion de comptes----------|   #
#   |--------------------------------------------|   #
# --Imports-- #
import datetime
from shared import saisir_choix, saisir_date


# --Constantes-- #

# --Fonctions-- #
def selection_compte(lst_cpt: list, courant: bool = True) -> str:
    """
    Interface qui permet de sélectionner un compte parmi ceux qui sont présents sur
    le compte bancaire d'un utilisateur, pour diverses utilisations.

    Args:
        lst_cpt (list): contient la liste des comptes de l'utilisateur
        courant (bool): valeur True par défaut qui indique que le compte par défaut est le compte courant (compte A)

    Returns:
        str: le nom du compte
    """
    choix = 0
    nb_comptes = len(lst_cpt)
    if not courant:
        print("Faites le choix du compte : ")
        for i in range(nb_comptes):
            print(f'{i + 1}. {lst_cpt[i]}')
        print("Choisissez le compte: ")
        choix = saisir_choix(valeurs_autorisees=set(range(1, nb_comptes+1))) - 1  # On enlève le 1 ajouté à l'affichage
    compte_choisi = lst_cpt[choix]
    return compte_choisi


def calcul_solde(lst_ope: list, compte: str) -> float:
    """
    Calcule le solde d'un utilisateur grâce à la liste des opérations associées au compte.

    Args:
        lst_ope (list): liste des opérations
        compte (str): le nom du compte

    Returns:
        float: le montant présent sur le compte
    """
    solde = 0
    for ope in lst_ope:
        # ope[2] représente la case contenant le compte associé à une opération donnée.
        if ope[2] == compte:
            solde += ope[3]  # ope[3] correspond au montant (+/-) de l'opération.
    return solde


def ajout_compte(lst_cpt: list, nom: str) -> bool:
    """
    Ajoute un compte de type livret d'épargne, etc. à la liste des comptes de l'utilisateur prise en paramètre.

    Args:
        lst_cpt (list): liste des comptes de l'utilisateur.
        nom (str): le nom du nouveau compte.

    Returns:
        bool: booléen qui indique si oui ou non le compte a été ajouté
    """
    lst_cpt_minuscule = [compte.casefold() for compte in lst_cpt]
    if nom.casefold() in lst_cpt_minuscule:
        print("Le compte existe déjà.")
        return False
    else:
        lst_cpt.append(nom.capitalize())
        print(f"Compte {nom} ajouté avec succès.")
        return True


def creation_operation(lst_cpt: list, lst_bud: list) -> tuple:
    """
    Crée le tuple d'une opération suite à l'entrée de l'utilisateur.

    Args:
        lst_cpt (list): liste des comptes de l'utilisateur.
        lst_bud (list): liste des budgets de l'utilisateur.

    Returns:
        tuple: l'opération sous forme de tuple
    """
    from budgets import selection_budget

    date_op = saisir_date()
    libelle = input("Libellé de l'opération : ")
    compte = selection_compte(lst_cpt, courant=False)

    saisie_montant = input("Montant en € (-montant si négatif) : ")
    saisie_montant_valide = False
    while not saisie_montant_valide:
        try:
            montant = float(saisie_montant)
            saisie_montant_valide = True
        except ValueError:
            print("Veuillez entrer un montant en € correct.")
            saisie_montant = input("Montant en € (-montant si négatif) : ")

    mode_paiement = input("Mode de paiement (CB, VIR, CHE, ...) : ")

    saisie_etat = input("L'opération est elle passée ? (O/N) : ").upper()
    while saisie_etat not in ['O', 'N']:
        saisie_etat = input("L'opération est elle passée ? (O/N) : ").upper()
    match saisie_etat:
        case 'O':
            etat = True
        case 'N':
            etat = False

    # On choisit seulement le nom / libellé du budget ici,
    # car nous n'utilisons que son nom dans l'enregistrement de l'opération
    budget = selection_budget(lst_bud)[0]

    operation = date_op, libelle, compte, montant, mode_paiement, etat, budget
    return operation


def ajout_operation(lst_ope: list, operation: tuple) -> None:
    """
    Ajoute une opération (tuple) à la liste des opérations de l'utilisateur, prise en paramètre.

    Args:
        lst_ope (list): la liste des opérations à laquelle on vient ajouter la nouvelle opération.
        operation (tuple): le tuple contenant les informations relatives à une opération (date, libellé, etc.)

    Returns:
        None
    """
    lst_ope.append(operation)


def creer_virement(lst_cpt: list, dict_soldes: dict) -> tuple:
    """
    Interface pour créer le virement, sous forme de tuple, afin de l'exécuter à l'aide de ajout_virement()

    Args:
        lst_cpt (list): liste des comptes de l'utilisateur.
        dict_soldes (dict): dictionnaire des soldes de chaque compte de l'utilisateur.

    Returns:
        tuple: le virement prêt à être exécuté.
    """
    print("Sélectionnez le compte émetteur : ")
    compte_emetteur = selection_compte(lst_cpt, courant=False)
    solde_emetteur = dict_soldes[compte_emetteur]
    while solde_emetteur <= 0:
        print(f"Le solde de ce compte ({solde_emetteur:.2f} €) ne permet pas de faire un virement. "
              f"Veuillez choisir un autre compte émetteur.")
        compte_emetteur = selection_compte(lst_cpt, courant=False)
        solde_emetteur = dict_soldes[compte_emetteur]

    print("Sélectionnez le compte bénéficiaire : ")
    compte_benef = selection_compte(lst_cpt, courant=False)
    while compte_emetteur == compte_benef:
        print("Le compte émetteur doit être différent du compte bénéficiaire.")
        compte_benef = selection_compte(lst_cpt, courant=False)

    saisie_montant = input(f"Saisissez le montant du virement à effectuer "
                           f"(solde : {solde_emetteur:.2f} €) : ")
    saisie_montant_valide = False
    while not saisie_montant_valide:
        try:
            montant = float(saisie_montant)
            if montant > 0:
                saisie_montant_valide = True
        except ValueError:
            print("Veuillez entrer un montant en € correct.")
            saisie_montant = input("Montant en € : ")

    while montant > dict_soldes[compte_emetteur]:
        print(f"Il n'y a pas assez de provisions sur ce compte pour effectuer ce virement. "
              f"({montant:.2f} € > {dict_soldes[compte_emetteur]:.2f} €)")
        saisie_montant = input(f"Saisissez le montant du virement à effectuer "
                               f"(solde : {solde_emetteur:.2f} €) : ")
        saisie_montant_valide = False
        while not saisie_montant_valide:
            try:
                montant = float(saisie_montant)
                if montant > 0:
                    saisie_montant_valide = True
            except ValueError:
                print("Veuillez entrer un montant en € correct.")
                saisie_montant = input("Montant en € : ")

    virement = compte_emetteur, compte_benef, montant
    return virement


def ajout_virement(virement: tuple, lst_ope: list, dict_soldes: dict) -> None:
    """
    Effectue les modifications nécessaires aux structures pour l'exécution d'un virement d'un compte à un autre.

    Args:
        virement (tuple): tuple qui contient compte_emetteur, compte_benef, montant
        lst_ope (list): liste des opérations de l'utilisateur
        dict_soldes (dict): dictionnaire avec les soldes de chaque compte de l'utilisateur.

    Returns:
        None
    """
    ope_emetteur = (datetime.date.today(),
                    f"Virement - émetteur",
                    virement[0],  # Compte émetteur
                    -virement[2],  # Montant, négatif
                    "VIR",
                    True,
                    "...")
    ope_benef = (datetime.date.today(),
                 f"Virement - bénéficiaire",
                 virement[1],  # Compte émetteur
                 virement[2],  # Montant, négatif
                 "VIR",
                 True,
                 "...")

    ajout_operation(lst_ope, operation=ope_emetteur)
    ajout_operation(lst_ope, operation=ope_benef)

    dict_soldes[virement[0]] -= virement[2]
    dict_soldes[virement[1]] += virement[2]


def calcul_dict_soldes(lst_cpt, lst_ope) -> dict:
    """
    Crée un dictionnaire contenant, pour chaque compte, son solde associé

    Args:
        lst_cpt (list): liste des comptes de l'utilisateur.
        lst_ope (list): liste des opérations de l'utilisateur.

    Returns:
        dict: le dictionnaire {compte1 : solde1, ...}
    """
    dict_soldes = dict(zip(lst_cpt, [0 for _ in lst_cpt]))
    for ope in lst_ope:
        dict_soldes[ope[2]] = dict_soldes.get(ope[2], 0) + ope[3]
    return dict_soldes


def afficher_operations(lst_ope: list, compte: str, filtre_date: bool = False) -> None:
    """
    Affiche les opérations de l'utilisateur, en fonction d'un compte et, si précisé, filtré selon une période.

    Args:
        lst_ope: liste des opérations de l'utilisateur
        compte: le nom du compte
        filtre_date: boolén pour savoir si l'on doit filtrer (filtre_date == True) par la date ou non

    Returns:
        None
    """
    if filtre_date:
        print("Veuillez saisir la date de début pour filtrer.")
        plancher = saisir_date()
        print("Veuillez saisir la date limite pour filtrer.")
        limite = saisir_date()
        date_valide = False
        while not date_valide:
            if plancher < limite:
                date_valide = True
            else:
                print("La date limite doit être inférieure ou égale à celle du début.")
                limite = saisir_date()
        for operation in lst_ope:
            if operation[2] == compte and plancher <= operation[0] <= limite:
                print(formatter_operation(operation))
    else:
        for operation in lst_ope:
            if operation[2] == compte:
                print(formatter_operation(operation))


def formatter_operation(operation: tuple) -> str:
    """
    Formate une opération bancaire sous forme de chaîne lisible pour l'affichage.

    Args:
        operation (tuple): Une opération représentée par un tuple contenant :
            - date (datetime.date)
            - libellé (str)
            - compte (str)
            - montant (float)
            - mode de paiement (str)
            - état de validation (bool)
            - budget associé (str)

    Returns:
        str: Une chaîne formatée décrivant l'opération de manière claire.
    """
    etat_str = "Passée" if operation[5] else "En attente"
    affichage = (f"| Date : {operation[0].strftime("%d/%m/%Y")} - "
                 f"Libellé : {operation[1]} - "
                 f"Compte : {operation[2]} - "
                 f"Montant : {operation[3]:.2f} € - "
                 f"Mode de paiement : {operation[4]} - "
                 f"Etat : {etat_str} - "
                 f"Budget : {operation[6]} |")
    return affichage

# --Programme principal--
