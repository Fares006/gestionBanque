# -*- coding: utf-8 -*-
#   shared.py
#   |--------------------------------------------|   #
#   |--------Gestion de Banque (avec IHM)--------|   #
#   |--Groupe 2 (MOUSSA, ASSEMAT, JIN, ZAMOURI)--|   #
#   |Fonctions utilitaires (enregistrement, etc.)|   #
#   |--------------------------------------------|   #
# --Imports-- #
import hashlib
import os
import shutil

from constantes import IDX_OPE_DATE, IDX_OPE_LIB
from cryptage_decryptage import cryptage, decryptage


# --Constantes-- #


# --Fonctions-- #
def enregistrement_modif(
    lst_cpt: list,
    lst_ope: list,
    lst_bud: list,
    identifiant: int,
    cle_cryptage: int
) -> None:
    """
    Enregistre de façon sécurisée toutes les données de l'utilisateur dans un fichier chiffré,
    en créant une sauvegarde (.bak) et un fichier temporaire (.tmp) au préalable.

    Les lignes enregistrées suivent une convention :
        - CPT*<nom_du_compte>
        - OPE*<date>*<libellé>*<compte>*<montant>*<mode>*<état>*<budget>
        - BUD*<libellé>*<montant>*<compte>
        - HASH*<valeur_sha256> (ajouté automatiquement à la fin)

    Args:
        lst_cpt (list): Liste des comptes utilisateur.
        lst_ope (list): Liste des opérations utilisateur (tuples).
        lst_bud (list): Liste des budgets utilisateur (listes).
        identifiant (int): Identifiant numérique de l'utilisateur (sert à nommer le fichier).
        cle_cryptage (int): Clé utilisée pour chiffrer le fichier.

    Returns:
        None
    """
    # Définition des dossiers et chemins de fichiers
    dossier_users = "../users"
    dossier_temp = os.path.join(dossier_users, "temp")
    dossier_backup = os.path.join(dossier_users, "backup")

    # Création des dossiers si absents, ne génère pas d’erreur si déjà là
    os.makedirs(dossier_temp, exist_ok=True)
    os.makedirs(dossier_backup, exist_ok=True)

    # Chemins complets des fichiers à manipuler
    chemin_original = os.path.join(dossier_users, f"{identifiant}.txt")
    chemin_temporaire = os.path.join(dossier_temp, f"{identifiant}.tmp")
    chemin_backup = os.path.join(dossier_backup, f"{identifiant}.bak")

    try:
        lignes = []

        # Encodage des comptes
        for compte in lst_cpt:
            lignes.append(f"CPT*{compte}")

        # Encodage des opérations avec formatage de la date
        for operation in lst_ope:
            date_str = operation[IDX_OPE_DATE].strftime('%d/%m/%Y')

            # On convertit tous les champs de l'opération (sauf la date) en texte
            # afin de pouvoir les assembler proprement dans une ligne formatée
            champs_op = [date_str] + list(map(str, operation[IDX_OPE_LIB:]))

            # On construit une ligne texte de type 'OPE*date*libellé*...*budget'
            lignes.append("OPE*" + "*".join(champs_op))

        # Encodage des budgets
        for budget in lst_bud:
            # On transforme chaque budget en ligne texte formatée 'BUD*libellé*montant*compte'
            lignes.append("BUD*" + "*".join(map(str, budget)))

        # Regroupe toutes les lignes dans une chaîne unique
        contenu_en_clair = "\n".join(lignes)

        # Calcul du hash du contenu clair (empreinte numérique)
        hash_val = hashlib.sha256(contenu_en_clair.encode("utf-8")).hexdigest()

        # Ajoute la ligne de hash à la fin (convention : "HASH*<valeur>")
        contenu_complet = contenu_en_clair + f"\nHASH*{hash_val}"

        # Chiffrement du contenu complet (avec la ligne de hash)
        texte_chiffre = cryptage(contenu_complet, cle_cryptage)

        # Écriture dans un fichier temporaire
        with open(chemin_temporaire, "w", encoding="utf-8") as f:
            f.write(texte_chiffre)

        # Sauvegarde de l'ancien fichier si existant
        if os.path.exists(chemin_original):
            shutil.copy(chemin_original, chemin_backup)

        # Remplace le fichier utilisateur par le fichier temporaire (opération atomique)
        os.replace(chemin_temporaire, chemin_original)

    except Exception as e:
        print(f"Erreur lors de l'enregistrement sécurisé : {e}")

        # Nettoyage du fichier temporaire en cas d'erreur
        if os.path.exists(chemin_temporaire):
            os.remove(chemin_temporaire)


def verifier_integrite_fichier(chemin_fichier: str, cle: int) -> bool:
    """
    Vérifie l'intégrité d'un fichier utilisateur chiffré en comparant le hash stocké
    avec le hash recalculé sur le contenu brut (hors ligne 'HASH*').

    Args:
        chemin_fichier (str): Chemin du fichier à vérifier.
        cle (int): Clé de décryptage à utiliser.

    Returns:
        bool: True si le fichier est valide, False si modifié/corrompu.
    """
    try:
        # Lecture du fichier chiffré
        with open(chemin_fichier, mode='r', encoding='utf-8') as fichier:
            contenu_chiffre = fichier.read()

        # Déchiffrement complet du fichier
        contenu_clair = decryptage(contenu_chiffre, cle=cle).strip()

        # Séparation des lignes
        lignes = contenu_clair.split('\n')

        # Vérification de la présence de la ligne HASH
        if not lignes[-1].startswith("HASH*"):
            print("Ligne de hash manquante dans le fichier.")
            return False

        # Extraction du hash stocké
        hash_attendu = lignes[-1].split('*', 1)[1]

        # Recalcul du hash sur le contenu sans la ligne 'HASH*'
        contenu_sans_hash = '\n'.join(lignes[:-1])
        hash_recalcule = hashlib.sha256(contenu_sans_hash.encode("utf-8")).hexdigest()

        return hash_recalcule == hash_attendu

    except Exception as e:
        print(f"Erreur pendant la vérification d'intégrité : {e}")
        return False
