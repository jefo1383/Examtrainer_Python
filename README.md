# 🐍 Python Exam Trainer

Un simulateur d'examen local (style "Examshell" ou "Moulinette") pour s'entraîner aux algorithmes Python.
Ce projet permet de tester son code en conditions réelles avec une validation automatique stricte.

## 📋 Description

Ce programme (`trainer.py`) agit comme un correcteur automatique. Il propose une série d'exercices classés par niveaux de difficulté. Pour chaque exercice, vous devez écrire la solution dans un fichier dédié (`solution.py`). Le correcteur lance ensuite une batterie de **10 tests unitaires** (incluant des cas limites, des listes vides, des grands nombres, etc.) pour valider ou rejeter votre code.

## 🚀 Fonctionnalités

* **4 Niveaux de difficulté** progressive.
* **Correction instantanée** avec affichage des erreurs (Entrée vs Attendu vs Reçu).
* **Gestion des types de sortie** : Supporte les fonctions qui `return` une valeur et celles qui `print` dans la console (capture de flux stdout).
* **Tests robustes** : 10 tests par exercice pour couvrir les "Edge Cases" (cas particuliers).
* **Rechargement dynamique** : Pas besoin de relancer le programme, il relit votre fichier à chaque tentative.

## 🛠️ Installation & Prérequis

Aucune installation complexe n'est requise. Le projet utilise uniquement la librairie standard de Python.

* **Requis** : Python 3.x

```bash
# Vérifier votre version de python
python3 --version

```

## 🎮 Comment l'utiliser

1. Assurez-vous d'avoir les fichiers `trainer.py` et `solution.py` (créez ce dernier s'il n'existe pas) dans le même dossier.
2. Lancez le simulateur :

```bash
python3 trainer.py

```

3. Le terminal affichera le nom de l'exercice et la consigne.
4. Ouvrez `solution.py` dans votre éditeur de code favori (VS Code, Vim, etc.).
5. Écrivez votre fonction en respectant scrupuleusement le prototype demandé.
6. Sauvegardez votre fichier `solution.py`.
7. Retournez dans le terminal et appuyez sur **Entrée**.
8. Si c'est ✅ **VALIDÉ**, vous passez au suivant. Sinon, corrigez et réessayez !

## 📚 Liste des Exercices

### Niveau 1 (Manipulation de base)

* **Case Letter** : Manipulation de Strings, alternance Maj/Min, gestion des index.
* **FizzBuzz** : Logique conditionnelle, modulo, affichage (print).

### Niveau 2 (Listes & Matrices)

* **Matrix Reverse** : Manipulation de listes imbriquées (2D), slicing.

### Niveau 3 (Algorithmique Mathématique)

* **Swap Chunck** : Rotation de liste, gestion des index négatifs, modulo sur index.

### Niveau 4 (Avancé)

* **Convert Base** : Conversion de bases numériques (Binaire, Hexa, etc.) vers Base 10 et inversement.
* **Crispy Sort** : Tri complexe multi-critères (longueur, alphabet, voyelles) avec `sorted` et `lambda`.

## ⚠️ Règles de l'examen

Pour simuler les vraies conditions d'examen :

1. N'utilisez **pas de modules externes** (pas de `pip install`).
2. N'utilisez pas de fonctions qui facilitent trop la tâche si l'exercice demande de recréer la logique (ex: `hex()` ou `bin()` pour l'exo Convert Base sont souvent interdits).
3. Gérez les cas limites et cas particuliers.

## 📂 Structure du projet

```text
.
├── trainer.py      # Le moteur de test (ne pas modifier pendant l'exam)
├── solution.py     # Votre fichier de travail (à modifier)
└── README.md       # Documentation

```

---

*Bon entraînement !* 🧠
