# GestionBudget

## Description du projet
GestionBudget est un projet universitaire de gestion de comptes bancaires et de budgets. L'application est développée en **Python** et utilise **Tkinter** pour la partie graphique (prévue en fin de projet). Ce projet académique a pour but d'offrir une interface permettant aux utilisateurs de gérer leurs comptes et budgets de manière intuitive.

## Objectif du projet
Ce projet a été réalisé dans le cadre des cours de **M. Jérôme Delobelle** et **M. Bruno Bouzy** à l'**Université Paris Cité**.

## Fonctionnalités principales
### 1. Phase d’identification
- L'utilisateur s'identifie avec un **numéro d'identifiant** (8 chiffres) et un **mot de passe** (6 chiffres).
- Un **clavier virtuel** est utilisé pour la saisie du mot de passe, avec une disposition aléatoire des chiffres.
- Les identifiants sont stockés dans un fichier sécurisé (`ident.txt`), chiffré avec le **chiffrement de César**.

### 2. Gestion des comptes
- Visualisation des comptes bancaires et de leur solde.
- Ajout d'opérations bancaires (Carte Bancaire, Chèque, Virement).
- Gestion des virements entre comptes.
- Stockage des opérations dans des fichiers utilisateurs chiffrés.

### 3. Gestion des budgets
- Création et gestion de budgets mensuels.
- Association des opérations bancaires à des budgets spécifiques.
- Affichage des dépenses par budget sous forme de **tableau**.

### 4. Autres fonctionnalités
- Calculatrice intégrée.
- Simulateur d’emprunt immobilier.

## Prérequis
- **Python 3.12**
- **Bibliothèques** : `tkinter` (pour une future interface graphique)

## Installation
1. Installer [Python 3.12](https://www.python.org/downloads/).
2. Cloner le dépôt :  
   ```sh
   git clone https://github.com/votre-utilisateur/gestionBudget.git
   cd gestionBudget
   ```

## Utilisation
### Mode Ligne de Commande (CLI)
1. Exécuter le fichier principal :
   ```sh
   python main.py
   ```

## Structure du projet
```
gestionBudget/
 |-- main.py                   # Fichier principal du programme
 |-- README.md                 # Documentation du projet
 |-- gestionBudget.iml         # Fichier de configuration du projet
 |-- misc.xml                  # Fichier de configuration supplémentaire
 |-- modules.xml               # Fichier de configuration des modules
 |-- vcs.xml                   # Fichier de configuration du contrôle de version
 |-- .gitignore                # Fichier pour ignorer des fichiers dans Git
 |-- idea/                     # Dossier de configuration d'IDEA
     |-- inspectionProfiles/   
 |-- src/                      # Code source
     |-- crypter_decrypter_fichier.py  # Script pour crypter et décrypter des fichiers
     |-- ident.txt             # Fichier d'identification (crypté)
 |-- users/                    # Dossiers contenant les comptes et budgets des utilisateurs (cryptés)
     |-- 19283746.txt          # Fichier utilisateur
     |-- 23456789.txt          # Fichier utilisateur
     |-- 34567890.txt          # Fichier utilisateur
     |-- 56789012.txt          # Fichier utilisateur
     |-- 87654321.txt          # Fichier utilisateur
```

## Évolutions prévues
- Ajout progressif des fonctionnalités en mode CLI.
- Finalisation de l'interface graphique avec **Tkinter** en fin de projet.
- Amélioration de la sécurité du stockage des données.
- Ajout de la visualisation graphique des budgets.
- Documentation plus détaillée et exemples d'utilisation.

## Licence
Projet réalisé à des fins académiques. Toute utilisation externe doit être validée par l'Université Paris Cité.

---
📌 *Projet universitaire – Université Paris Cité*
