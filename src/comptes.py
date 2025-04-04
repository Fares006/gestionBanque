# -*- coding: utf-8 -*-
#   comptes.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |----------Phase gestion de comptes----------|   #
#   |--------------------------------------------|   #
# --Imports-- #
import datetime
from copy import copy

from shared import saisir_choix, saisir_date


# --Constantes-- #

# --Fonctions-- #
def selection_compte(lst_cpt: list, courant: bool = True, exclude_self: bool = False, cpt_self: str = None) -> str:
    """
    Permet à l'utilisateur de sélectionner un compte parmi ceux disponibles.

    Par défaut, la fonction retourne automatiquement le premier compte de la liste (souvent "Compte A"),
    sauf si courant=False, auquel cas une interface console est affichée pour que l'utilisateur choisisse
    manuellement un compte dans la liste.

    Args:
        lst_cpt (list): Liste des comptes de l'utilisateur (ex. ["Compte A", "Compte B"]).
        courant (bool): Si True (par défaut), sélectionne automatiquement le premier compte. 
                        Si False, propose à l'utilisateur de choisir un compte manuellement.
        exclude_self (bool): Si l'opération demande à l'utilisateur de faire un virement par exemple,
                             on n'autorise pas la sélection du compte émetteur en tant que bénéficiaire.
        cpt_self (str): Le compte à ne pas inclure dans la liste des choix.

    Returns:
        str: Le nom du compte sélectionné par l'utilisateur.
    """
    choix = 0
    i = 0
    nb_comptes = len(lst_cpt)
    epuise = False
    if not courant:
        print("Faites le choix du compte : ")
        while i < nb_comptes and not epuise:
            if not exclude_self:
                print(f'{i + 1}. {lst_cpt[i]}')
                i += 1
            else:
                lst_cpt_no_self = copy(lst_cpt)
                lst_cpt_no_self.remove(cpt_self)
                try:
                    print(f'{i + 1}. {lst_cpt_no_self[i]}')
                    i += 1
                except IndexError:
                    epuise = True
        print("Choisissez le compte: ")
        choix = saisir_choix(
            valeurs_autorisees=set(range(1, nb_comptes + 1))) - 1  # On enlève le 1 ajouté à l'affichage
    compte_choisi = lst_cpt[choix] if not exclude_self else lst_cpt_no_self[choix]
    return compte_choisi


def calcul_solde(lst_ope: list, compte: str) -> float:
    """
    Calcule le solde actuel d’un compte donné à partir de la liste des opérations.

    Seules les opérations :
    - associées au compte spécifié
    - et marquées comme "passées" (état True)

    sont prises en compte dans le calcul du solde.

    Args:
        lst_ope (list): Liste des opérations sous forme de tuples
                        (date, libellé, compte, montant, mode_paiement, état, budget).
        compte (str): Nom du compte dont on souhaite calculer le solde.

    Returns:
        float: Solde total du compte (somme des montants des opérations passées).
    """
    solde = 0
    for ope in lst_ope:
        # ope[2] représente la case contenant le compte associé à une opération donnée.
        if ope[2] == compte and ope[5] is True:
            solde += ope[3]  # ope[3] correspond au montant (+/-) de l'opération.
    return solde


def ajout_compte(lst_cpt: list, nom: str) -> bool:
    """
    Ajoute un nouveau compte (ex : livret, épargne, etc.) à la liste des comptes de l'utilisateur,
    à condition qu'il n'existe pas déjà (vérification insensible à la casse).

    Si le compte est ajouté, il est automatiquement capitalisé (première lettre en majuscule).

    Args:
        lst_cpt (list): Liste existante des comptes de l'utilisateur.
        nom (str): Nom du nouveau compte à ajouter.

    Returns:
        bool: True si le compte a été ajouté avec succès, False s'il existait déjà.
    """
    lst_cpt_minuscule = [compte.casefold() for compte in lst_cpt]
    if nom.casefold() in lst_cpt_minuscule:
        print("Le compte existe déjà.")
        return False
    else:
        lst_cpt.append(nom.title())
        print(f"Compte {nom} ajouté avec succès.")
        return True


def creation_operation(lst_cpt: list, lst_bud: list) -> tuple:
    """
    Crée une opération bancaire à partir des saisies utilisateur, 
    et la retourne sous forme de tuple structuré.

    Les informations demandées sont :
        - date de l'opération (via saisir_date)
        - libellé de l'opération
        - compte concerné (choisi dans la liste lst_cpt)
        - montant (float, positif ou négatif)
        - mode de paiement (CB, CHE, VIR, etc.)
        - état de l'opération (passée ou non)
        - budget associé (sélectionné dans lst_bud)

    Args:
        lst_cpt (list): Liste des comptes disponibles pour l'utilisateur.
        lst_bud (list): Liste des budgets définis par l'utilisateur.

    Returns:
        tuple: Un tuple contenant toutes les informations de l'opération sous la forme :
            (date, libellé, compte, montant, mode_paiement, état, budget)
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
    Ajoute une opération bancaire à la liste des opérations existantes de l'utilisateur.

    L'opération est représentée par un tuple structuré contenant :
        (date, libellé, compte, montant, mode_paiement, état, budget)

    Args:
        lst_ope (list): Liste actuelle des opérations de l'utilisateur.
        operation (tuple): Tuple représentant une opération à ajouter à la liste.

    Returns:
        None
    """
    lst_ope.append(operation)


def creer_virement(lst_cpt: list, dict_soldes: dict, is_nouveau_compte: bool = False,
                   nouveau_compte: str = None) -> tuple:
    """
    Interface utilisateur permettant de créer un virement entre deux comptes.

    La fonction vérifie que :
    - Le compte émetteur dispose d’un solde suffisant
    - Le compte bénéficiaire est différent du compte émetteur
    - Le montant saisi est valide et disponible
    - Qu'il s'agit d'une opération de transfert du solde initial d'un nouveau compte
        - Auquel cas, elle demande à l'utilisateur depuis quel compte se fera l'opération

    Elle retourne un tuple contenant les informations nécessaires pour effectuer le virement via ajout_virement().

    Args:
        lst_cpt (list): Liste des comptes de l'utilisateur.
        dict_soldes (dict): Dictionnaire des soldes de chaque compte de l'utilisateur.
        is_nouveau_compte (bool) : Si True, alors on ne demande pas à l'utilisateur le compte bénéficiaire,
                                   il sera automatiquement nouveau_compte
        nouveau_compte (str) : Le nom du nouveau compte qu'aura créé l'utilisateur

    Returns:
        tuple: Le virement sous forme (compte_emetteur, compte_beneficiaire, montant)
    """
    print("Sélectionnez le compte émetteur : ")
    compte_emetteur = selection_compte(lst_cpt, courant=False, exclude_self=True, cpt_self=nouveau_compte) \
        if is_nouveau_compte else selection_compte(lst_cpt, courant=False)
    solde_emetteur = dict_soldes[compte_emetteur]
    # Vérifie que le solde du compte émetteur permet un virement
    while solde_emetteur <= 0:
        print(f"Le solde de ce compte ({solde_emetteur:.2f} €) ne permet pas de faire un virement. "
              f"Veuillez choisir un autre compte émetteur.")
        compte_emetteur = selection_compte(lst_cpt, courant=False)
        solde_emetteur = dict_soldes[compte_emetteur]

    if not is_nouveau_compte:
        print("Sélectionnez le compte bénéficiaire : ")
        compte_benef = selection_compte(lst_cpt, courant=False)
        # Vérifie que les comptes source et destination sont différents
        while compte_emetteur == compte_benef:
            print("Le compte émetteur doit être différent du compte bénéficiaire.")
            compte_benef = selection_compte(lst_cpt, courant=False)
    else:
        compte_benef = nouveau_compte

    saisie_montant_valide = False
    while not saisie_montant_valide:  # Redemande un montant tant que celui-ci est invalide ou supérieur au solde
        saisie_montant = input(f"Saisissez le montant du virement à effectuer "
                               f"(solde : {solde_emetteur:.2f} €) : ")
        try:
            montant = float(saisie_montant)
            if montant > 0:
                saisie_montant_valide = True
        except ValueError:
            print("Veuillez entrer un montant en € correct.")

    while montant > dict_soldes[compte_emetteur]:
        print(f"Il n'y a pas assez de provisions sur ce compte pour effectuer ce virement. "
              f"({montant:.2f} € > {dict_soldes[compte_emetteur]:.2f} €)")
        saisie_montant_valide = False
        while not saisie_montant_valide:
            saisie_montant = input(f"Saisissez le montant du virement à effectuer "
                                   f"(solde : {solde_emetteur:.2f} €) : ")
            try:
                montant = float(saisie_montant)
                if montant > 0:
                    saisie_montant_valide = True
            except ValueError:
                print("Veuillez entrer un montant en € correct.")

    virement = compte_emetteur, compte_benef, montant
    return virement


def ajout_virement(virement: tuple, lst_ope: list, dict_soldes: dict) -> None:
    """
    Effectue un virement entre deux comptes en mettant à jour :
    - la liste des opérations (ajout débit/crédit)
    - le dictionnaire des soldes (mise à jour des montants)

    Deux opérations sont créées :
        - Une pour le compte émetteur (montant négatif)
        - Une pour le compte bénéficiaire (montant positif)

    Args:
        virement (tuple): Tuple contenant (compte_emetteur (str), compte_beneficiaire (str), montant (float))
        lst_ope (list): Liste des opérations de l'utilisateur à mettre à jour.
        dict_soldes (dict): Dictionnaire des soldes des comptes de l'utilisateur.

    Returns:
        None
    """
    # Crée une opération de débit pour le compte émetteur
    ope_emetteur = (datetime.date.today(),
                    f"Virement - émetteur",
                    virement[0],  # Compte émetteur
                    -virement[2],  # Montant, négatif
                    "VIR",
                    True,
                    "...")
    # Crée une opération de crédit pour le compte bénéficiaire
    ope_benef = (datetime.date.today(),
                 f"Virement - bénéficiaire",
                 virement[1],  # Compte émetteur
                 virement[2],  # Montant, négatif
                 "VIR",
                 True,
                 "...")

    ajout_operation(lst_ope, operation=ope_emetteur)
    ajout_operation(lst_ope, operation=ope_benef)

    # Met à jour les soldes des deux comptes
    dict_soldes[virement[0]] -= virement[2]
    dict_soldes[virement[1]] = dict_soldes.get(virement[1], 0) + dict_soldes.get(virement[1], virement[2])


def calcul_dict_soldes(lst_cpt, lst_ope) -> dict:
    """
    Calcule le solde de chaque compte de l'utilisateur et retourne un dictionnaire associant
    chaque compte à son solde.

    La fonction initialise le solde de chaque compte à 0, puis parcourt la liste des opérations
    pour additionner (ou soustraire) le montant de chaque opération au compte correspondant.
    On suppose que chaque opération est représentée par un tuple dont :
        - l'indice 2 correspond au nom du compte,
        - l'indice 3 correspond au montant de l'opération (positif ou négatif).

    Args:
        lst_cpt (list): Liste des comptes de l'utilisateur.
        lst_ope (list): Liste des opérations de l'utilisateur.

    Returns:
        dict: Un dictionnaire où chaque clé est le nom d'un compte et chaque valeur est son solde (float).
    """

    dict_soldes = dict(zip(lst_cpt, [0 for _ in lst_cpt]))
    for ope in lst_ope:
        dict_soldes[ope[2]] = dict_soldes.get(ope[2], 0) + ope[3]
    return dict_soldes


def afficher_operations(lst_ope: list, compte: str, filtre_date: bool = False) -> None:
    """
    Affiche les opérations associées à un compte spécifique, avec ou sans filtrage par date.

    Si filtre_date est True, l'utilisateur est invité à saisir une période (date de début et date de fin).
    Seules les opérations comprises dans cette plage seront affichées.
    Si filtre_date est False, toutes les opérations du compte spécifié sont affichées sans restriction.

    Args:
        lst_ope (list): Liste des opérations de l'utilisateur.
        compte (str): Nom du compte dont on souhaite afficher les opérations.
        filtre_date (bool, optional): Si True, filtre les opérations par date. Sinon, affiche toutes les opérations.

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
            if plancher <= limite:
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
    Formate une opération bancaire sous forme de chaîne lisible pour affichage.

    Cette fonction transforme les données d'une opération stockée sous forme de tuple
    en une chaîne structurée contenant tous les champs pertinents.

    Args:
        operation (tuple): Une opération représentée par :
            - date (datetime.date) : Date de l'opération
            - libellé (str) : Description de l'opération
            - compte (str) : Nom du compte concerné
            - montant (float) : Montant (positif ou négatif)
            - mode de paiement (str) : CB, VIR, CHE, etc.
            - état (bool) : True si l'opération est passée, False sinon
            - budget (str) : Libellé du budget associé

    Returns:
        str: Chaîne formatée et lisible représentant l'opération.
    """
    etat_str = "Passée" if operation[5] else "En attente"
    affichage = (f"| Date : {operation[0].strftime('%d/%m/%Y')} - "
                 f"Libellé : {operation[1]} - "
                 f"Compte : {operation[2]} - "
                 f"Montant : {operation[3]:.2f} € - "
                 f"Mode de paiement : {operation[4]} - "
                 f"État : {etat_str} - "
                 f"Budget : {operation[6]} |")
    return affichage

# --Programme principal--
