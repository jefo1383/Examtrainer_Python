# 🐍 Python Exam Trainer

Un simulateur d'examen local (style "Examshell") pour s'entraîner aux algorithmes Python.
Ce projet génère un **examen blanc complet** en tirant au sort des exercices parmi une vaste base de données, testant votre code avec une validation automatique stricte.

## 📋 Description

Ce programme (`trainer.py`) agit comme un correcteur automatique intelligent.
À son lancement, il propose un menu pour choisir votre **parcours de difficulté** (Basic, Medium, Challenging). Pour chaque niveau du parcours choisi, il sélectionne un exercice au hasard. Vous devez écrire la solution dans un fichier dédié (`solution.py`). Le correcteur lance ensuite une batterie de **10 tests unitaires rigoureux** (cas limites, grands nombres, types incorrects, cas complexes...) pour valider votre code.

## 🚀 Fonctionnalités

* **Menu de Difficulté** : 4 parcours disponibles (Basic, Medium, Challenging, In-depth).
* **Mode Examen Aléatoire** : Un exercice tiré au sort à chaque passage de niveau.
* **Commandes Interactives** :
    * `next` : Générer un autre exercice du même niveau.
    * `up` : Forcer le passage au niveau supérieur (Skip).
    * `exit` : Quitter le programme proprement.
* **Correction Instantanée** : Affichage clair des différences (Entrée vs Attendu vs Reçu).
* **Gestion des sorties et arguments multiples** : Supporte `return`, la capture de `print` (stdout), et le déballage automatique d'arguments complexes (tuples, matrices, dictionnaires).
* **Rechargement Dynamique** : Pas besoin de relancer le programme, il relit votre fichier `solution.py` à chaque essai.

## 🛠️ Installation & Prérequis

Aucune installation complexe requise. Projet "Vanilla Python".

* **Requis** : Python 3.x

~~~bash
python3 --version
~~~

## 🎮 Comment l'utiliser

1. Assurez-vous d'avoir `trainer.py` et `solution.py` dans le même dossier.
2. Lancez le simulateur :

~~~bash
python3 trainer.py
~~~

3. Le terminal affiche le **menu principal**. Sélectionnez votre parcours (ex: `1` pour Basic).
4. Le premier exercice du niveau s'affiche.
5. Ouvrez `solution.py`, écrivez votre fonction en respectant scrupuleusement le **prototype**.
6. Revenez dans le terminal. Vous avez 4 choix :
    * Appuyer sur **Entrée** pour lancer la correction de votre code.
    * Taper **`next`** pour changer d'exercice (si celui-ci ne vous inspire pas).
    * Taper **`up`** pour sauter l'exercice et passer directement au niveau suivant.
    * Taper **`exit`** pour arrêter l'examen.
7. Si c'est ✅ **VALIDÉ**, vous passez automatiquement au niveau suivant !

## 📚 Liste des Exercices (Base de données)

Le programme choisit actuellement parmi **25 exercices** répartis par difficulté :

### 🟢 Parcours : Python Basic
Conçu pour réviser la syntaxe fondamentale, les boucles et les tris simples.
* **String Sculptor** : Manipulation de string (alternance Maj/Min).
* **FizzBuzz** : Boucles, conditions et modulo.
* **Convert Base** : Algorithme de conversion (Bases 2 à 36).
* **Bracket Validator** : Validation de parenthèses (Stack logique avec caractères parasites).
* **Matrix Reverse / Transpose / Sort Rev** : Opérations et transformations sur matrices 2D.
* **Is Palindrome / Rot 13** : Analyse et chiffrement de chaînes.
* **Shadow Merge / Twist Shake** : Fusion et rotation de listes.
* **Cryptic Sort / Custom Sort** : Tris multi-critères avancés.

### 🟡 Parcours : Python Medium
Conçu pour introduire les algorithmes classiques et la manipulation de structures imbriquées.
* **Palindrome Partitioning** : Découpage optimal de chaînes.
* **Is Rotation** : Vérification de décalage circulaire de tableaux.
* **Max Sliding Window** : Analyse de sous-tableaux par fenêtre glissante.
* **Merge Sorted List / List Intersection** : Algorithmique ensembliste avec préservation d'ordre.
* **Constellation Mapper** : Génération de grilles 2D par coordonnées.
* **Packages Dependencies** : Ordonnancement conditionnel et résolution de graphes acycliques (DAG).

### 🔴 Parcours : Python Challenging
Conçu pour repousser les limites avec des algorithmes d'optimisation (Graphes, DP, Gloutons).
* **Run-Length Encoding (RLE)** : Compression de données.
* **Max Intervals** : Ordonnancement glouton d'intervalles (*Interval Scheduling*).
* **Detect Cycle** : Parcours en profondeur (DFS 3-états) dans des graphes orientés.
* **Find Shortest Path** : Parcours en largeur (BFS) dans des grilles labyrinthiques.
* **Maximal Square** : Programmation Dynamique (DP) sur cartes 2D.

### 🟣 Parcours : Python In-Depth
*En cours de construction...*

## ⚠️ Règles de l'examen

1. N'utilisez **pas de modules externes** (pas de `pip install`). L'import autorisé dépend du sujet.
2. Respectez strictement les **prototypes** fournis (noms de fonctions, arguments, et typages attendus).
3. Gérez les **cas limites** (listes vides, entrées hors bornes, etc.). Le correcteur ne pardonne pas !

## 📂 Structure du projet

~~~text
.
├── trainer.py      # Le moteur d'examen (ne pas modifier)
├── solution.py     # Votre fichier de travail (à modifier)
└── README.md       # Documentation
~~~

---
*Bonne chance pour l'examen !* 🧠