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
from constantes import (
    IDX_OPE_DATE,
    IDX_OPE_LIB,
    IDX_OPE_CPT,
    IDX_OPE_MONTANT,
    IDX_OPE_MODE,
    IDX_OPE_ETAT,
    IDX_OPE_BUD,
    IDX_BUD_NOM
)


# --Constantes-- #

# --Fonctions-- #
def selection_compte(lst_cpt: list, courant: bool = True, exclude_self: bool = False, cpt_self: str = None) -> str:
    """
    Permet à l'utilisateur de sélectionner un compte parmi ceux disponibles.

    - Si courant=True (par défaut) : retourne automatiquement le premier compte (souvent "Compte A").
    - Si courant=False : propose une sélection manuelle à l'utilisateur via la console.
    - Si exclude_self=True : retire un compte donné (cpt_self) de la liste pour éviter qu'il soit sélectionné.
      Ce cas est utile pour un virement où le compte bénéficiaire doit être différent de l’émetteur.

    Args:
        lst_cpt (list): Liste des comptes de l'utilisateur (ex. ["Compte A", "Compte B"]).
        courant (bool): Si True, sélectionne automatiquement le premier compte.
        exclude_self (bool): Si True, exclut cpt_self de la liste proposée.
        cpt_self (str): Compte à exclure de la sélection (utile avec exclude_self=True).

    Returns:
        str: Le nom du compte sélectionné.
    """
    if courant:
        return lst_cpt[0]  # Sélection automatique par défaut (compte "courant")

    # Prépare la liste affichée (avec ou sans exclusion de cpt_self )
    lst_affichee = copy(lst_cpt)
    if exclude_self and cpt_self in lst_affichee:
        lst_affichee.remove(cpt_self)

    # Affichage des options à l'utilisateur
    print("Faites le choix du compte :")
    for i, compte in enumerate(lst_affichee):
        print(f"{i + 1}. {compte}")

    # Saisie utilisateur (on enlève 1 pour transformer l'index humain en index Python)
    choix = saisir_choix(valeurs_autorisees=set(range(1, len(lst_affichee) + 1))) - 1

    return lst_affichee[choix]


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
        # ope[IDX_OPE_CPT] représente la case contenant le compte associé à une opération donnée.
        # On vérifie l'état de l'opération avec ope[IDX_OPE_ETAT], si elle est passé, on la prend en compte
        if ope[IDX_OPE_CPT] == compte and ope[IDX_OPE_ETAT]:
            solde += ope[IDX_OPE_MONTANT]  # ope[IDX_OPE_MONTANT] correspond au montant (+/-) de l'opération.
    return solde


def ajout_compte(lst_cpt: list, nom: str) -> bool:
    """
    Ajoute un nouveau compte (ex : livret, épargne, etc.) à la liste des comptes de l'utilisateur,
    à condition qu'il n'existe pas déjà (vérification insensible à la casse).

    Si le compte est ajouté, il est automatiquement capitalisé (première lettre en majuscule de chaque mot).

    Utilise un ensemble (set) pour optimiser la recherche d'existence (O(1)).

    Args:
        lst_cpt (list): Liste existante des comptes de l'utilisateur.
        nom (str): Nom du nouveau compte à ajouter.

    Returns:
        bool: True si le compte a été ajouté avec succès, False s'il existait déjà.
    """
    nom = nom.strip()   # Supprime les espaces inutiles en début et fin

    # Création d'un ensemble avec les noms en minuscules (via casefold) pour comparaison rapide
    comptes_set = {c.casefold() for c in lst_cpt}

    # Vérifie si le compte existe déjà (insensible à la casse)
    if nom.casefold() in comptes_set:
        print("Le compte existe déjà.")
        return False
    else:
        # Ajoute le compte en le capitalisant (ex : "livret a" → "Livret A")
        lst_cpt.append(nom.title())
        print(f"Compte {nom.title()} ajouté avec succès.")
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
    libelle = input("Libellé de l'opération : ").strip().capitalize()
    compte = selection_compte(lst_cpt, courant=False)

    saisie_montant_valide = False
    while not saisie_montant_valide:
        saisie_montant = input("Montant en € (-montant si négatif) : ")
        try:
            montant = float(saisie_montant)
            if montant != 0:
                saisie_montant_valide = True
            else:
                print("Veuillez saisir un montant non nul.")
        except ValueError:
            print("Veuillez entrer un montant en € correct.")

    mode_paiement = input("Mode de paiement (CB, VIR, CHE, ...) : ").strip().upper()

    saisie_etat_valide = False
    while not saisie_etat_valide:
        saisie_etat = input("L'opération est elle passée ? (O/N) : ").upper()
        if saisie_etat not in ['O', 'N']:
            print("Saisissez 'O' ou 'N'.")
        else:
            saisie_etat_valide = True
            etat = saisie_etat == 'O'

    # On choisit seulement le nom / libellé du budget ici,
    # car nous n'utilisons que son nom dans l'enregistrement de l'opération
    budget = selection_budget(lst_bud)[IDX_BUD_NOM]

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
    assert isinstance(operation, tuple) and len(operation) == 7, "L'opération doit être un tuple de 7 éléments"
    lst_ope.append(operation)


def creer_virement(lst_cpt: list, dict_soldes: dict,
                   is_nouveau_compte: bool = False,
                   nouveau_compte: str = None) -> tuple:
    """
    Interface utilisateur en ligne de commande permettant de créer un virement entre deux comptes de l'utilisateur.

    Cette fonction permet à l'utilisateur de :
    - Choisir un compte émetteur (parmi ceux disponibles)
    - Choisir un compte bénéficiaire (sauf dans le cas où le virement est destiné à un nouveau compte)
    - Saisir un montant de virement
    - Vérifier la validité de la transaction (solde suffisant, comptes différents, montant valide)

    Elle est également utilisée pour initialiser un virement vers un nouveau compte, lors de sa création,
    auquel cas le compte bénéficiaire est automatiquement renseigné.

    Args:
        lst_cpt (list): Liste des noms de comptes disponibles de l'utilisateur.
        dict_soldes (dict): Dictionnaire associant chaque nom de compte à son solde actuel.
        is_nouveau_compte (bool): Indique s'il s'agit d'un virement vers un nouveau compte (dans ce cas,
                                  le compte bénéficiaire est imposé et correspond à nouveau_compte).
        nouveau_compte (str): Nom du compte récemment créé (utilisé uniquement si is_nouveau_compte est True).

    Returns:
        tuple: Tuple contenant les informations du virement sous la forme
               (compte_emetteur, compte_beneficiaire, montant).
    """

    print("Sélectionnez le compte émetteur : ")

    # Si on initialise un nouveau compte, on ne veut pas que l'utilisateur puisse le sélectionner comme émetteur
    compte_emetteur = selection_compte(lst_cpt, courant=False, exclude_self=True, cpt_self=nouveau_compte) \
        if is_nouveau_compte else selection_compte(lst_cpt, courant=False)

    solde_emetteur = dict_soldes[compte_emetteur]

    # Tant que le solde du compte émetteur est nul ou négatif, on redemande un autre compte
    while solde_emetteur <= 0:
        print(f"Le solde de ce compte ({solde_emetteur:.2f} €) ne permet pas de faire un virement. "
              f"Veuillez choisir un autre compte émetteur.")
        compte_emetteur = selection_compte(lst_cpt, courant=False)
        solde_emetteur = dict_soldes[compte_emetteur]

    # Sélection du compte bénéficiaire uniquement si ce n'est pas un virement vers un nouveau compte
    if not is_nouveau_compte:
        print("Sélectionnez le compte bénéficiaire : ")
        compte_benef = selection_compte(lst_cpt, courant=False)

        # Le compte bénéficiaire doit être différent du compte émetteur
        while compte_emetteur == compte_benef:
            print("Le compte émetteur doit être différent du compte bénéficiaire.")
            compte_benef = selection_compte(lst_cpt, courant=False)
    else:
        compte_benef = nouveau_compte  # Virement d'initialisation du nouveau compte

    saisie_montant_valide = False

    # Demande à l'utilisateur de saisir un montant valide (> 0)
    while not saisie_montant_valide:
        saisie_montant = input(f"Saisissez le montant du virement à effectuer "
                               f"(solde : {solde_emetteur:.2f} €) : ")
        try:
            montant = float(saisie_montant)
            if montant > 0:
                saisie_montant_valide = True
        except ValueError:
            print("Veuillez entrer un montant en € correct.")

    # Vérifie que le montant ne dépasse pas le solde du compte émetteur
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

    # Retourne les données du virement sous forme de tuple
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
                    -virement[2],  # Montant du débit (négatif)
                    "VIR",
                    True,
                    "...")
    # Crée une opération de crédit pour le compte bénéficiaire
    ope_benef = (datetime.date.today(),
                 f"Virement - bénéficiaire",
                 virement[1],  # Compte émetteur
                 virement[2],  # Montant du crédit (positif)
                 "VIR",
                 True,
                 "...")

    ajout_operation(lst_ope, operation=ope_emetteur)
    ajout_operation(lst_ope, operation=ope_benef)

    # Met à jour les soldes des deux comptes
    dict_soldes[virement[0]] -= virement[2]
    dict_soldes[virement[1]] = dict_soldes.get(virement[1], 0) + virement[2]


def calcul_dict_soldes(lst_cpt, lst_ope) -> dict:
    """
    Calcule le solde de chaque compte de l'utilisateur à partir de la liste des opérations,
    et retourne un dictionnaire associant chaque compte à son solde.

    Pour chaque compte, le solde est initialisé à 0. Ensuite, chaque opération de la liste
    est traitée pour mettre à jour le solde du compte concerné, en ajoutant ou soustrayant
    le montant de l’opération.

    Convention utilisée pour les opérations (tuple) :
        - ope[2] : nom du compte concerné
        - ope[3] : montant de l’opération (positif ou négatif)

    Args:
        lst_cpt (list): Liste des noms des comptes de l'utilisateur.
        lst_ope (list): Liste des opérations, où chaque opération est un tuple contenant
                        au moins les éléments aux indices 2 (compte) et 3 (montant).

    Returns:
        dict: Dictionnaire avec comme clés les noms de comptes et comme valeurs leurs soldes respectifs.
    """
    # Initialise le dictionnaire avec un solde de 0 pour chaque compte de la liste
    dict_soldes = dict(zip(lst_cpt, [0 for _ in lst_cpt]))

    # Parcourt toutes les opérations pour mettre à jour le solde des comptes concernés
    for ope in lst_ope:
        # Ajout (ou soustraction) du montant de l'opération au solde du compte concerné
        # Utilisation get(..., 0) pour éviter une erreur si une opération concerne un compte non listé initialement
        dict_soldes[ope[2]] = dict_soldes.get(ope[2], 0) + ope[3]

    # Retourne le dictionnaire final contenant les soldes à jour
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
        # Demande et validation directe des dates (boucle jusqu'à plage valide)
        while True:
            print("Veuillez saisir la date de début pour filtrer.")
            plancher = saisir_date()
            print("Veuillez saisir la date limite pour filtrer.")
            limite = saisir_date()
            if plancher <= limite:
                break
            print("La date limite doit être supérieure ou égale à la date de début.")

    trouve = False
    for operation in lst_ope:
        if operation[IDX_OPE_CPT] == compte:
            # L'opérateur 'or' utilise un court-circuit : si not filtre_date est True,
            # Python n'évalue pas la suite (plancher <= operation[0] <= limite),
            # ce qui évite une erreur si plancher ou limite ne sont pas définis.
            if not filtre_date or (plancher <= operation[IDX_OPE_DATE] <= limite):
                print(formatter_operation(operation))
                trouve = True

    if not trouve:
        print("Aucune opération trouvée pour ce compte et/ou à cette date.")


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
    etat_str = "Passée" if operation[IDX_OPE_ETAT] else "En attente"
    affichage = (f"| Date : {operation[IDX_OPE_DATE].strftime('%d/%m/%Y')} - "
                 f"Libellé : {operation[IDX_OPE_LIB]} - "
                 f"Compte : {operation[IDX_OPE_CPT]} - "
                 f"Montant : {operation[IDX_OPE_MONTANT]:.2f} € - "
                 f"Mode de paiement : {operation[IDX_OPE_MODE]} - "
                 f"État : {etat_str} - "
                 f"Budget : {operation[IDX_OPE_BUD]} |")
    return affichage

# --Programme principal--
