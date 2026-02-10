# 🐍 Python Exam Trainer

Un simulateur d'examen local (style "Examshell" ou "Moulinette") pour s'entraîner aux algorithmes Python.
Ce projet génère un **examen blanc complet** en tirant au sort des exercices parmi une base de données, testant votre code avec une validation automatique stricte.

## 📋 Description

Ce programme (`trainer.py`) agit comme un correcteur automatique intelligent.
Il simule un examen en 4 niveaux. Pour chaque niveau, il sélectionne un exercice au hasard. Vous devez écrire la solution dans un fichier dédié (`solution.py`). Le correcteur lance ensuite une batterie de **10 tests unitaires** (cas limites, grands nombres, types incorrects...) pour valider votre code.

## 🚀 Fonctionnalités

* **Mode Examen Aléatoire** : Un exercice tiré au sort par niveau (1 → 2 → 3 → 4).
* **Commandes Interactives** :
    * `next` : Générer un autre exercice du même niveau.
    * `exit` : Quitter le programme proprement.
* **Correction Instantanée** : Affichage clair des différences (Entrée vs Attendu vs Reçu).
* **Gestion des sorties** : Supporte `return` et `print` (capture stdout).
* **Rechargement Dynamique** : Pas besoin de relancer le programme, il relit votre fichier `solution.py` à chaque essai.

## 🛠️ Installation & Prérequis

Aucune installation complexe requise. Projet "Vanilla Python".

* **Requis** : Python 3.x

```bash
python3 --version

```

## 🎮 Comment l'utiliser

1. Assurez-vous d'avoir `trainer.py` et `solution.py` dans le même dossier.
2. Lancez le simulateur :
```bash
python3 trainer.py

```


3. Le terminal affiche un exercice tiré au sort pour le **Niveau 1**.
4. Ouvrez `solution.py`, écrivez votre fonction en respectant le prototype.
5. Revenez dans le terminal. Vous avez 3 choix :
* Appuyer sur **Entrée** pour corriger votre code.
* Taper **`next`** pour changer d'exercice (si celui-ci ne vous inspire pas).
* Taper **`exit`** pour arrêter.


6. Si c'est ✅ **VALIDÉ**, vous passez automatiquement au niveau suivant !

## 📚 Liste des Exercices (Base de données)

Le programme choisit parmi ces 12 exercices :

### Niveau 1 (Bases & Logique)

* **Case Letter** : Manipulation de string (alternance Maj/Min).
* **FizzBuzz** : Boucles, conditions et modulo.
* **Convert Base** : Algorithme de conversion de bases (Binaire, Hexa -> Décimal et inverse).
* **Bracket Validator** : Algorithme de validation de parenthèses (Stack/Pile logique).

### Niveau 2 (Listes & Matrices)

* **Matrix Reverse** : Inversion verticale de matrice (colonnes).
* **Is Palindrome** : Vérification de palindrome (nettoyage de string).
* **Sort Rev Matrix** : Tri décroissant des lignes d'une matrice.

### Niveau 3 (Algorithmique Intermédiaire)

* **Swap Chunk** : Rotation de liste et manipulation d'index.
* **Rot 13** : Chiffrement par décalage ASCII.
* **Transpose Matrix** : Transformation lignes <-> colonnes (Zip).

### Niveau 4 (Tris Avancés)

* **Crispy Sort** : Tri multi-critères (Longueur > Voyelles > Alpha).
* **Custom Sort** : Tri conditionnel (Longueur > Alpha > Priorité Majuscule).

## ⚠️ Règles de l'examen

1. N'utilisez **pas de modules externes** (pas de `pip install`).
2. Respectez strictement les **prototypes** fournis (noms de fonctions et arguments).
3. Gérez les cas limites (listes vides, arguments invalides).

## 📂 Structure du projet

```text
.
├── trainer.py      # Le moteur d'examen (ne pas modifier)
├── solution.py     # Votre fichier de travail (à modifier)
└── README.md       # Documentation

```

---

*Bonne chance pour l'examen !* 🧠
