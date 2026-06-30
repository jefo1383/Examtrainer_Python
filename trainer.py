import sys
import time
import importlib.util
import os
import io
import re
import random
from contextlib import redirect_stdout

# --- COULEURS ---
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CYAN}{'='*50}")
    print("      EXAM TRAINER - 42 - PYTHON")
    print(f"{'='*50}{RESET}\n")

def charger_solution():
    if not os.path.exists("solution.py"):
        print(f"{RED}Erreur : 'solution.py' introuvable.{RESET}")
        return None
    
    if "solution" in sys.modules:
        del sys.modules["solution"]
        
    spec = importlib.util.spec_from_file_location("solution", "solution.py")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"{RED}Erreur de syntaxe dans 'solution.py' :{RESET}")
        print(e)
        return None

def get_function_name(prototype):
    match = re.search(r"def\s+(\w+)", prototype)
    if match:
        return match.group(1)
    return None

def run_tests(exercice):
    """
    Exécute les tests pour un exercice donné.
    Retourne : 
      True  -> Exercice réussi
      False -> Exercice raté
      "next" -> L'utilisateur veut changer d'exercice
      "exit" -> L'utilisateur veut quitter
      "up" -> L'utilisateur veut passer au niveau superieur
    """
    func_name = get_function_name(exercice['prototype'])
    if not func_name:
        print(f"{RED}Erreur config: Prototype invalide pour {exercice['nom']}{RESET}")
        return False

    # Affichage du sujet
    print_header()
    print(f"{BOLD}Exercice : {exercice['nom']} (Niveau {exercice['niveau']}){RESET}\n")
    print(f"Prototype : {YELLOW}{exercice['prototype']}{RESET}\n")
    print(f"Consigne : {exercice['sujet']}\n")
    print(f"Exemples :\n{CYAN}{exercice['exemples']}{RESET}\n")
    
    # Gestion des commandes utilisateur
    print(f"{YELLOW}Modifie 'solution.py' et appuie sur Entrée.")
    user_input = input(f"Commandes : 'next' (changer), 'up' (niv. suivant), 'exit' (quitter)... {RESET}")
    
    cmd = user_input.strip().lower()
    if cmd == "exit": return "exit"
    if cmd == "next": return "next"
    if cmd == "up": return "up"

    print("Correction...", end="", flush=True)
    time.sleep(0.5)
    print("\n") 
    
    module = charger_solution()
    if not module: return False

    if not hasattr(module, func_name):
        print(f"\n{RED}❌ Fonction '{func_name}' introuvable.{RESET}")
        print(f"   Vérifiez le prototype : {exercice['prototype']}")
        return False
    
    user_func = getattr(module, func_name)
    
    for i, (args, expected) in enumerate(exercice['tests']):
        try:
            if exercice.get('capture_print'):
                f = io.StringIO()
                with redirect_stdout(f):
                    user_func(args)
                result = f.getvalue().strip()
                expected = expected.strip()
            else:
                # Si args est un tuple, on décompresse les arguments (pour les fonctions à arguments multiples)
                if isinstance(args, tuple) and type(args).__name__ == 'tuple': 
                    result = user_func(*args)
                else: 
                    result = user_func(args)
                
            if result != expected:
                print(f"\n{RED}❌ TEST {i+1} ÉCHOUÉ{RESET}")
                print(f"   Entrée   : {args}")
                print(f"   Attendu  : {repr(expected)}")
                print(f"   Reçu     : {repr(result)}")
                return False
            else:
                print(f"{GREEN}TEST {i+1} ---------- 🔥{RESET}")

        except Exception as e:
            print(f"\n{RED}❌ ERREUR TEST {i+1} (Planté): {e}{RESET}")
            print(f"   Entrée   : {args}")
            print(f"   Attendu  : {repr(expected)}")
            return False

    print(f"\n{GREEN}✅ EXERCICE VALIDÉ !{RESET}\n")
    time.sleep(1)
    return True


# --- LISTE COMPLETE DES EXERCICES ---

EXERCICES = [
    # ==========================================
    # === CATEGORIE : PYTHON BASIC (Niv 1-4) ===
    # ==========================================
    {
        'nom': 'String_sculptor',
        'categorie': 'basic', 'niveau': 1,
        'prototype': 'def string_sculptor(text: str) -> str:',
        'sujet': 'Écrivez une fonction qui transforme la chaîne de caractères donnée en alternant la casse.\n'
                 'Le premier caractère doit être en minuscule, le second en majuscule, et ainsi de suite.\n'
                 'Les caractères non-alphabétiques doivent rester inchangés et ne comptent pas dans le positionnement.\n'
                 'Type de retour attendu : str',
        'exemples': '1. input = "Hello world"\n   output = "hElLo WoRlD"\n\n'
                    '2. input = "we123lcome"\n   output = "wE123lCoMe"\n\n'
                    '3. input = "Python 3.8"\n   output = "pYtHoN 3.8"',
        'capture_print': False,
        'tests': [
            ("Hello world", "hElLo WoRlD"),
            ("we123lcome", "wE123lCoMe"),
            ("Python! 3.10", "pYtHoN! 3.10"),
            ("", ""), ("123456", "123456"), ("A", "a"), ("a b c", "a B c"),
            ("   ", "   "), ("zZzZ", "zZzZ"), ("A!B@C#", "a!B@c#")
        ]
    },
    {
        'nom': 'FizzBuzz',
        'categorie': 'basic', 'niveau': 1,
        'prototype': 'def fizzbuzz(n: int) -> None:',
        'sujet': 'Écrivez une fonction qui affiche les nombres de 1 à n inclus, suivis d\'un saut de ligne.\n'
                 'Pour les multiples de 3, affichez "fizz". Pour 5, "buzz". Pour 3 et 5, "fizzbuzz".\n'
                 'Type de retour attendu : None (Affichage sur la sortie standard)',
        'exemples': '1. n = 3\n   1\n   2\n   fizz\n\n'
                    '2. n = 5\n   1\n   2\n   fizz\n   4\n   buzz\n',
        'capture_print': True,
        'tests': [
            (3, "1\n2\nfizz"),
            (5, "1\n2\nfizz\n4\nbuzz"),
            (15, "1\n2\nfizz\n4\nbuzz\nfizz\n7\n8\nfizz\nbuzz\n11\nfizz\n13\n14\nfizzbuzz"),
            (1, "1"), (0, ""), (2, "1\n2"), (6, "1\n2\nfizz\n4\nbuzz\nfizz"),
            (10, "1\n2\nfizz\n4\nbuzz\nfizz\n7\n8\nfizz\nbuzz"), (-5, ""),
            (20, "1\n2\nfizz\n4\nbuzz\nfizz\n7\n8\nfizz\nbuzz\n11\nfizz\n13\n14\nfizzbuzz\n16\n17\nfizz\n19\nbuzz")
        ]
    },
    {
        'nom': 'Convert Base',
        'categorie': 'basic', 'niveau': 1, 
        'prototype': 'def convert_base(n: str, base_from: int, base_to: int) -> str:',
        'sujet': 'Convertit une chaîne représentant un nombre d\'une base vers une autre base cible (2 à 36).\n'
                 'Si les paramètres sont invalides, échouez silencieusement en renvoyant None.',
        'exemples': '1. input = ("10", 10, 2)  -> "1010"\n'
                    '2. input = ("FF", 16, 10) -> "255"\n'
                    '3. input = ("10", 1, 10)  -> None',
        'capture_print': False,
        'tests': [
            (("10", 10, 2), "1010"), (("1A", 16, 10), "26"), (("1010", 2, 16), "A"),
            (("42", 10, 16), "2A"), (("0", 10, 2), "0"), (("10", 1, 10), None),
            (("10", 10, 37), None), (("FF", 16, 2), "11111111"), (("Z", 36, 10), "35"),
            (("7", 8, 2), "111")
        ]
    },
    {
        'nom': 'Bracket Validator',
        'categorie': 'basic', 'niveau': 1,
        'prototype': 'def bracket_validator(s: str) -> bool:',
        'sujet': 'Vérifie la validité d\'une expression contenant parenthèses, crochets et accolades.\n'
                 'Tous les autres caractères (lettres, chiffres, ponctuation) doivent être ignorés.\n'
                 'Type de retour attendu : bool',
        'exemples': '1. input = "{a[b]c}"\n   output = True\n\n'
                    '2. input = "(a[b)c]"\n   output = False\n\n'
                    '3. input = "texte sans crochets"\n   output = True',
        'capture_print': False,
        'tests': [
            ("{a[123]!}", True), 
            ("x(y[z)a]b", False), 
            ("({[a(b)c]})", True), 
            ("1(2(3", False),
            ("fin)", False), 
            ("", True), # Chaîne vide : cas limite toujours important
            (" ( ( a ( b ( c ) ) ) ) ", True), # Espaces et imbrications
            ("[1]{2}(3)", True), 
            ("a[b[c!@", False), 
            ("{![@(#)]*}", True)
        ]
    },
    {
        'nom': 'Matrix Reverse',
        'categorie': 'basic', 'niveau': 2,
        'prototype': 'def matrix_reverse(matrix: list[list[int]]) -> list[list[int]]:',
        'sujet': 'Inverse l\'ordre des éléments au sein de chaque ligne d\'une matrice.\n'
                 'Type de retour attendu : list[list[int]]',
        'exemples': '1. input = [[1, 2], [3, 4]] -> [[2, 1], [4, 3]]\n'
                    '2. input = [[1, 2, 3]] -> [[3, 2, 1]]',
        'capture_print': False,
        'tests': [
            ([[1, 2, 3], [4, 5, 6]], [[3, 2, 1], [6, 5, 4]]), ([], []),
            ([[], []], [[], []]), ([[1, 2], [], [10]], [[2, 1], [], [10]]),
            ([[100, 2000]], [[2000, 100]]), ([[1]], [[1]]),
            ([[1, 2, 3, 4, 5]], [[5, 4, 3, 2, 1]]), ([[0, 0, 1]], [[1, 0, 0]]),
            ([[-1, -2]], [[-2, -1]]), ([[1, 2], [1]], [[2, 1], [1]])
        ]
    },
    {
        'nom': 'Shadow merge',
        'categorie': 'basic', 'niveau': 2,
        'prototype': 'def shadow_merge(list1: list[int], list2: list[int]) -> list[int]:',
        'sujet': 'Fusionne deux listes triées en une troisième liste triée.\nType de retour attendu : list[int]',
        'exemples': '1. input = [1, 3], [2, 4] -> [1, 2, 3, 4]\n2. input = [], [1] -> [1]',
        'capture_print': False,
        'tests': [
            (([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6]), (([1, 2, 3], []), [1, 2, 3]),
            (([], []), []), (([], [4, 5, 6]), [4, 5, 6]), (([1, 2], [3, 4, 5, 6]), [1, 2, 3, 4, 5, 6]),
            (([1, 5, 5], [2, 5, 6]), [1, 2, 5, 5, 5, 6]), (([-5, 0, 2], [-3, 1]), [-5, -3, 0, 1, 2]),
            (([1, 2, 3], [10, 11]), [1, 2, 3, 10, 11]), (([20, 30], [1, 2, 3]), [1, 2, 3, 20, 30]),
            (([10], [5]), [5, 10])
        ]
    },
    {
        'nom': 'Is Palindrome',
        'categorie': 'basic', 'niveau': 2,
        'prototype': 'def is_palindrome(s: str) -> bool:',
        'sujet': 'Détermine si une chaîne est un palindrome (insensible à la casse, ignore les espaces).\n',
        'exemples': '1. "Kayak" -> True\n2. "Elu par cette crapule" -> True\n3. "Bonjour" -> False',
        'capture_print': False,
        'tests': [
            ("Kayak", True), ("test", False), ("A man a plan a canal Panama", True),
            ("Elu par cette crapule", True), ("", True), ("a", True), ("ab", False),
            ("Noon", True), ("Was it a car or a cat I saw", True), ("Python", False)
        ]
    },
    {
        'nom': 'Sort Rev Matrix',
        'categorie': 'basic', 'niveau': 2,
        'prototype': 'def sort_rev_matrix(matrix: list[list[int]]) -> list[list[int]]:',
        'sujet': 'Trie indépendamment chaque ligne d\'une matrice par ordre décroissant.\n',
        'exemples': '1. [[1, 5, 2], [8, 3]] -> [[5, 2, 1], [8, 3]]\n',
        'capture_print': False,
        'tests': [
            ([[1, 5, 2], [8, 3]], [[5, 2, 1], [8, 3]]), ([[1, 2, 3]], [[3, 2, 1]]),
            ([[-5, -1, -10]], [[-1, -5, -10]]), ([], []), ([[10, 2, 30], [5, 5, 5]], [[30, 10, 2], [5, 5, 5]]),
            ([[1]], [[1]]), ([[1, 3], [2, 4]], [[3, 1], [4, 2]]), ([[0], [0, 1]], [[0], [1, 0]]),
            ([[100, 1, 50]], [[100, 50, 1]]), ([[-1, -2, -3]], [[-1, -2, -3]])
        ]
    },
    {
        'nom': 'Twist shake',
        'categorie': 'basic', 'niveau': 3,
        'prototype': 'def twist_shake(arr: list[int], k: int) -> list[int]:',
        'sujet': 'Déplacez les k derniers éléments de la liste vers le début de celle-ci.\n',
        'exemples': '1. input = [0, 1, 2, 3, 4], k=2 -> [3, 4, 0, 1, 2]\n',
        'capture_print': False,
        'tests': [
            (([0, 1, 2, 3, 4, 5], 2), [4, 5, 0, 1, 2, 3]), (([1, 2, 3, 4], 10), [3, 4, 1, 2]),
            (([], 5), []), (([1, 2, 3], 3), [1, 2, 3]), (([1, 2, 3, 4, 5], 7), [4, 5, 1, 2, 3]),
            (([1, 2, 3], 0), [1, 2, 3]), (([1], 10), [1]), (([1, 2], 1), [2, 1]),
            (([10, 20, 30], 2), [20, 30, 10]), (([-10, -20, -30], 1), [-30, -10, -20])
        ]
    },
    {
        'nom': 'Rot 13',
        'categorie': 'basic', 'niveau': 3,
        'prototype': 'def rot13(txt: str) -> str:',
        'sujet': 'Algorithme de chiffrement par substitution ROT13.\n',
        'exemples': '1. "abc" -> "nop"\n2. "Hello" -> "Uryyb"',
        'capture_print': False,
        'tests': [
            ("abc", "nop"), ("nop", "abc"), ("Hello World!", "Uryyb Jbeyq!"),
            ("Python 3.10", "Clguba 3.10"), ("", ""), ("1234567890", "1234567890"),
            ("M", "Z"), ("N", "A"), ("z", "m"), ("a", "n")
        ]
    },
    {
        'nom': 'Transpose Matrix',
        'categorie': 'basic', 'niveau': 3,
        'prototype': 'def transpose_matrix(matrix: list[list[int]]) -> list[list[int]]:',
        'sujet': 'Calculez et retournez la transposée de la matrice.\n',
        'exemples': '1. [[1, 2], [3, 4]] -> [[1, 3], [2, 4]]\n',
        'capture_print': False,
        'tests': [
            ([[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]]), ([[1, 2], [3, 4]], [[1, 3], [2, 4]]),
            ([[1], [2], [3]], [[1, 2, 3]]), ([], []), ([[1]], [[1]]),
            ([[1, 2, 3]], [[1], [2], [3]]), ([[1, 2], [3, 4], [5, 6]], [[1, 3, 5], [2, 4, 6]]),
            ([[0, 0], [1, 1]], [[0, 1], [0, 1]]), ([[10, 20], [30, 40]], [[10, 30], [20, 40]]),
            ([[-1]], [[-1]])
        ]
    },
    {
        'nom': 'Cryptic Sort',
        'categorie': 'basic', 'niveau': 4,
        'prototype': 'def cryptic_sort(strings: list[str]) -> list[str]:',
        'sujet': 'Triez une liste de chaînes : 1. Longueur, 2. Ordre alphabétique, 3. Nombre de voyelles.\n',
        'exemples': '1. ["ccc", "bb", "a"] -> ["a", "bb", "ccc"]\n',
        'capture_print': False,
        'tests': [
            (["ccc", "bb", "a"], ["a", "bb", "ccc"]), (["chat", "char"], ["char", "chat"]),
            (["banane", "pomme", "kiwi", "sac", "arc", "a", ""], ["", "a", "arc", "sac", "kiwi", "pomme", "banane"]),
            ([], []), (["aa", "bz"], ["aa", "bz"]), (["Zebra", "apple", "Banana"], ["apple", "Zebra", "Banana"]),
            (["b", "a"], ["a", "b"]), (["E", "b"], ["b", "E"]),
            (["@#$!BB*&^%", "@#$!aa*&^%", "@#$!bb*&^%", "@#$!AA*&^%"], ["@#$!aa*&^%", "@#$!AA*&^%", "@#$!BB*&^%", "@#$!bb*&^%"]),
            (["aaaa", "bb"], ["bb", "aaaa"])
        ]
    },
    {
        'nom': 'Custom Sort',
        'categorie': 'basic', 'niveau': 4,
        'prototype': 'def custom_sort(words: list[str]) -> list[str]:',
        'sujet': 'Trie : 1. Longueur, 2. Alphabétique, 3. Majuscule prioritaire en cas d\'égalité.\n',
        'exemples': '1. ["b", "A", "a", "B"] -> ["A", "a", "B", "b"]\n',
        'capture_print': False,
        'tests': [
            (["b", "A", "a", "B"], ["A", "a", "B", "b"]), (["aa", "Ab", "ac"], ["aa", "Ab", "ac"]),
            (["Zoo", "abeille"], ["Zoo", "abeille"]), (["", "a"], ["", "a"]),
            (["c", "C"], ["C", "c"]), (["beta", "Alpha"], ["beta", "Alpha"]),
            (["A", "B", "C"], ["A", "B", "C"]), (["a", "b", "c"], ["a", "b", "c"]),
            (["Z", "z", "a"], ["a", "Z", "z"]), (["Test", "test"], ["Test", "test"])
        ]
    },

    # ==================================
    # === CATEGORIE : PYTHON MEDIUM  ===
    # ==================================
    {
        'nom': 'Palindrome partitioning',
        'categorie': 'medium', 'niveau': 2,
        'prototype': 'def palindrome_partitioning(s: str) -> int:',
        'sujet': 'Calculez le nombre minimum de coupes nécessaires pour partitionner\n'
                 'une chaîne de caractères de sorte que chaque sous-chaîne soit un palindrome.\n'
                 'Une lettre seule est considérée comme un palindrome.\n'
                 'Type de retour attendu : int',
        'exemples': '1. input = "aab"\n   output = 1\n\n'
                    '2. input = "racecar"\n   output = 0\n\n'
                    '3. input = "ab"\n   output = 1',
        'capture_print': False,
        'tests': [
            ("aab", 1), ("racecar", 0), ("ab", 1), ("banana", 1),
            ("abcde", 4), ("aaaa", 0), ("aabbc", 2), ("abacbc", 1),
            ("x madamy", 3), ("", 0)
        ]
    },
    {
        'nom': 'Is Rotation',
        'categorie': 'medium', 'niveau': 1,
        'prototype': 'def is_rotation(arr1: list[int], arr2: list[int]) -> bool:',
        'sujet': 'Déterminez si la liste arr2 est une rotation valide de la liste arr1.\n'
                 'Une rotation implique de décaler les éléments vers la gauche ou la droite,\n'
                 'et les éléments qui sortent d\'un côté réapparaissent de l\'autre.\n'
                 'Type de retour attendu : bool',
        'exemples': '1. input = [1, 2, 3, 4, 5], [5, 1, 2, 3, 4]\n'
                    '   output = True\n\n'
                    '2. input = [1, 2, 3, 4, 5], [2, 3, 4, 5, 6]\n'
                    '   output = False\n\n'
                    '3. input = [], []\n'
                    '   output = True',
        'capture_print': False,
        'tests': [
            (([1, 2, 3, 4, 5], [5, 1, 2, 3, 4]), True),
            (([1, 2, 3, 4, 5], [2, 3, 4, 5, 1]), True),
            (([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]), True),
            (([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]), False),
            (([], []), True),
            (([1, 2], [1, 2, 3]), False), # Tailles différentes (Edge case)
            (([1, 1, 2, 1], [1, 2, 1, 1]), True), # Avec des doublons
            (([1, 2, 3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 1, 2, 3]), True),
            (([1, 2, 3, 4], [4, 3, 2, 1]), False), # Liste inversée, pas tournante
            (([7, 7, 7, 7, 7], [7, 7, 7, 7, 7]), True) # Nombres identiques
        ]
    },
    {
        'nom': 'Max Sliding Window',
        'categorie': 'medium', 'niveau': 1,
        'prototype': 'def max_sliding_window(nums: list[int], k: int) -> list[int]:',
        'sujet': 'Étant donné un tableau d\'entiers `nums` et une fenêtre glissante de taille `k`,\n'
                 'qui se déplace de l\'extrême gauche vers l\'extrême droite d\'une position à la fois.\n'
                 'Vous ne pouvez voir que les `k` nombres dans la fenêtre à chaque étape.\n'
                 'Retournez un tableau contenant le chiffre maximum de chaque fenêtre.\n'
                 'Type de retour attendu : list[int]',
        'exemples': '1. input = [1, 3, -1, -3, 5, 3, 6, 7], k = 3\n'
                    '   output = [3, 3, 5, 5, 6, 7]\n\n'
                    '2. input = [1], k = 1\n'
                    '   output = [1]\n\n'
                    '3. input = [4, -2], k = 2\n'
                    '   output = [4]',
        'capture_print': False,
        'tests': [
            (([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7]),
            (([1], 1), [1]),
            (([1, -1], 1), [1, -1]),
            (([9, 11], 2), [11]),
            (([4, -2], 2), [4]),
            (([1, 2, 3, 4, 5], 5), [5]), # k équivalent à la taille de la liste (Edge case)
            (([5, 4, 3, 2, 1], 2), [5, 4, 3, 2]), # Tableau strictement décroissant
            (([1, 2, 3, 4, 5], 2), [2, 3, 4, 5]), # Tableau strictement croissant
            (([], 0), []), # Tableau vide (Edge case)
            (([8, 3, -1, -3, 5, 3, 6, 7, 9, 2, 4, 1, 5], 4), [8, 5, 5, 5, 6, 7, 9, 9, 9, 5]) # Cas complexe plus long
        ]
    },
    {
        'nom': 'Merge Sorted List',
        'categorie': 'medium', 'niveau': 3,
        'prototype': 'def merge_sorted_list(lists: list[list[int]]) -> list[int]:',
        'sujet': 'Fusionnez plusieurs listes d\'entiers en une seule liste finale triée par ordre croissant.\n'
                 'Type de retour attendu : list[int]',
        'exemples': '1. input = [[1, 4, 5], [1, 3, 4], [2, 6]]\n'
                    '   output = [1, 1, 2, 3, 4, 4, 5, 6]\n\n'
                    '2. input = []\n'
                    '   output = []\n\n'
                    '3. input = [[], [1]]\n'
                    '   output = [1]',
        'capture_print': False,
        'tests': [
            ([[1, 4, 5], [1, 3, 4], [2, 6]], [1, 1, 2, 3, 4, 4, 5, 6]),
            ([], []),
            ([[], [], []], []),
            ([[1, 2, 3]], [1, 2, 3]),
            ([[-5, 0], [-2, 3], [1]], [-5, -2, 0, 1, 3]),
            ([[10, 20], [5, 15], [1, 2]], [1, 2, 5, 10, 15, 20]),
            ([[1, 1, 1], [1, 1]], [1, 1, 1, 1, 1]),
            ([[], [5], []], [5]),
            ([[100]], [100]),
            ([[1, 10, 20], [2, 9, 21], [3, 8, 22], [4, 7, 23], [5, 6, 24]], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 21, 22, 23, 24]) # Cas complexe
        ]
    },
    {
        'nom': 'List Intersection Ordered',
        'categorie': 'medium', 'niveau': 2,
        'prototype': 'def list_intersection_finder_ordered(lists: list[list[int]]) -> list[int]:',
        'sujet': 'Trouvez l\'intersection de plusieurs listes d\'entiers.\n'
                 'Le résultat doit conserver l\'ordre d\'apparition des éléments de la première liste.\n'
                 'Si un élément apparaît plusieurs fois dans la première liste et fait partie de l\'intersection,\n'
                 'ses occurrences doivent être conservées.\n'
                 'Type de retour attendu : list[int]',
        'exemples': '1. input = [[1, 2, 3, 4], [2, 4, 6], [2, 4, 8]]\n'
                    '   output = [2, 4]\n\n'
                    '2. input = [[1, 1, 2], [1, 2], [1, 2, 3]]\n'
                    '   output = [1, 1, 2]\n\n'
                    '3. input = [[1, 2], [3, 4]]\n'
                    '   output = []',
        'capture_print': False,
        'tests': [
            ([[1, 2, 3, 4], [2, 4, 6], [2, 4, 8]], [2, 4]),
            ([[1, 1, 2], [1, 2], [1, 2, 3]], [1, 1, 2]),
            ([[1, 2], [3, 4]], []),
            ([], []),
            ([[1, 2, 3]], [1, 2, 3]),
            ([[5, 4, 3, 2, 1], [1, 2, 3], [3, 1, 5]], [3, 1]),
            ([[10, 20, 30], [], [10, 20]], []),
            ([[0, 0, 0], [0]], [0, 0, 0]),
            ([[-1, -2, -3], [-3, -2, -1], [-2, -1]], [-1, -2]),
            ([[5, 9, 2, 9, 1, 4], [9, 5, 2, 4, 7], [2, 9, 4, 5, 8], [9, 9, 9, 5, 2, 4]], [5, 9, 2, 9, 4]) # Cas complexe
        ]
    },
    {
        'nom': 'Constellation Mapper',
        'categorie': 'medium', 'niveau': 1,
        'prototype': 'def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:',
        'sujet': 'Générez une grille carrée de taille `size` x `size` sous forme de liste de chaînes.\n'
                 'Les espaces vides sont représentés par des points `.` et les étoiles par des `*`.\n'
                 'Les étoiles sont fournies sous la forme de tuples de coordonnées (ligne, colonne).\n'
                 'Type de retour attendu : list[str]',
        'exemples': '1. stars = [(0, 0), (1, 1)], size = 2\n'
                    '   output = ["*.", ".*"]\n\n'
                    '2. stars = [(0, 2)], size = 3\n'
                    '   output = ["..*", "...", "..."]\n\n'
                    '3. stars = [], size = 1\n'
                    '   output = ["."]',
        'capture_print': False,
        'tests': [
            (([(0, 0), (1, 1)], 2), ["*.", ".*"]),
            (([(0, 2)], 3), ["..*", "...", "..."]),
            (([], 1), ["."]),
            (([(0, 0), (0, 1), (0, 2)], 3), ["***", "...", "..."]),
            (([(2, 2)], 3), ["...", "...", "..*"]),
            (([(0, 0), (1, 3), (2, 2), (4, 4)], 5), ["*....", "...*.", "..*..", ".....", "....*"]),
            (([], 0), []),
            (([(1, 1), (1, 1)], 3), ["...", ".*.", "..."]), # Étoiles superposées
            (([(i, i) for i in range(4)], 4), ["*...", ".*..", "..*.", "...*"]),
            (([(0,9), (1,8), (2,7), (3,6), (4,5), (5,4), (6,3), (7,2), (8,1), (9,0)], 10), 
             [".........*", "........*.", ".......*..", "......*...", ".....*....", "....*.....", "...*......", "..*.......", ".*........", "*........."]) # Diagonale inverse complexe
        ]
    },
    {
        'nom': 'Packages Dependencies',
        'categorie': 'medium', 'niveau': 3,
        'prototype': 'def packages_dependencies(packages: list[tuple[str, list[str]]]) -> list[str]:',
        'sujet': 'Déterminez l\'ordre d\'installation de paquets pour respecter leurs dépendances.\n'
                 'Vous recevez une liste de tuples : (nom_du_paquet, [dependances_requises]).\n'
                 'Un paquet ne peut être installé que si toutes ses dépendances sont déjà installées.\n'
                 'S\'il y a un cycle ou des dépendances introuvables, ignorez les paquets impossibles à résoudre.\n'
                 'En cas d\'égalité (plusieurs paquets prêts en même temps), respectez l\'ordre d\'apparition initial des paquets dans la liste.\n'
                 'Type de retour attendu : list[str]',
        'exemples': '1. input = [("A", []), ("B", ["A"])]\n'
                    '   output = ["A", "B"]\n\n'
                    '2. input = [("A", ["B"]), ("B", ["C"]), ("C", [])]\n'
                    '   output = ["C", "B", "A"]\n\n'
                    '3. input = [("A", ["B"]), ("B", ["A"])]\n'
                    '   output = []',
        'capture_print': False,
        'tests': [
            ([("A", []), ("B", ["A"])], ["A", "B"]),
            ([("A", ["B"]), ("B", ["C"]), ("C", [])], ["C", "B", "A"]),
            ([("A", ["B"]), ("B", ["A"])], []), # Cycle complet
            ([], []),
            ([("A", ["C"]), ("B", ["C"]), ("C", [])], ["C", "A", "B"]),
            ([("X", ["Y", "Z"]), ("Y", ["Z"]), ("Z", [])], ["Z", "Y", "X"]),
            ([("A", ["D"]), ("B", ["D"]), ("C", ["D"])], []), # Dépendance "D" manquante
            ([("A", []), ("B", []), ("C", [])], ["A", "B", "C"]),
            ([("Flask", ["Werkzeug", "Jinja2"]), ("Werkzeug", []), ("Jinja2", ["MarkupSafe"]), ("MarkupSafe", [])], 
             ["Werkzeug", "MarkupSafe", "Jinja2", "Flask"]),
            # Cas complexe avec arbre asymétrique et résolution multi-passes
            ([("App", ["Auth", "DB", "UI"]), ("UI", ["React"]), ("Auth", ["DB", "Crypto"]), ("DB", ["FS"]), ("Crypto", []), ("React", []), ("FS", [])], 
             ["Crypto", "React", "FS", "UI", "DB", "Auth", "App"])
        ]
    }

    # =======================================
    # === CATEGORIE : PYTHON CHALLENGING  ===
    # =======================================
    {
        'nom': 'Run-Length Encoding',
        'categorie': 'challenging', 'niveau': 1,
        'prototype': 'def run_length_encoding(s: str) -> str:',
        'sujet': 'Réalisez la compression par encodage de longueur de plage (RLE) de la chaîne.\n'
                 'Remplacez chaque séquence de caractères identiques consécutifs par le nombre '
                 'd\'occurrences suivi du caractère lui-même.\n'
                 'Si la chaîne d\'entrée est vide, retournez une chaîne vide.',
        'exemples': '1. input = "aabbc"\n   output = "2a2b1c"\n\n'
                    '2. input = "a"\n   output = "1a"\n\n'
                    '3. input = ""\n   output = ""',
        'capture_print': False,
        'tests': [
            ("aabbc", "2a2b1c"),
            ("", ""),
            ("a", "1a"),
            ("abc", "1a1b1c"),
            ("AAAAA", "5A"),
            ("aAaA", "1a1A1a1A"),
            ("11223", "212213"),
            ("  ", "2 "),
            ("!!!!!!!!!!", "10!"),
            ("aaabbbbcccddeeeefff", "3a4b3c2d4e3f") # Cas complexe
        ]
    },
    {
        'nom': 'Max Intervals',
        'categorie': 'challenging', 'niveau': 2,
        'prototype': 'def max_intervals(intervals: list[tuple[int, int]]) -> int:',
        'sujet': 'Déterminez le cardinal maximal d\'un sous-ensemble d\'intervalles mutuellement compatibles.\n'
                 'Chaque intervalle est un tuple (début, fin). Si deux intervalles se touchent '
                 'à la frontière (ex: fin à 5 et début à 5), ils sont compatibles.\n'
                 'Type de retour attendu : int',
        'exemples': '1. input = [(1, 3), (2, 4), (3, 5)]\n   output = 2\n\n'
                    '2. input = []\n   output = 0\n\n'
                    '3. input = [(1, 2)]\n   output = 1',
        'capture_print': False,
        'tests': [
            ([(1, 3), (2, 4), (3, 5)], 2),
            ([], 0),
            ([(1, 2)], 1),
            ([(1, 2), (2, 3), (3, 4)], 3), # Intervalles collés
            ([(1, 5), (2, 3), (3, 4)], 2),
            ([(1, 10), (2, 6), (7, 11), (3, 4), (5, 6), (7, 8)], 4),
            ([(0, 1), (0, 1), (0, 1)], 1), # Duplicatas complets
            ([(10, 20), (1, 10)], 2),      # Désordonnés
            ([(5, 10), (1, 5), (10, 15)], 3),
            ([(0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (8, 10), (9, 11)], 5) # Complexe
        ]
    },
    {
        'nom': 'Detect Cycle',
        'categorie': 'challenging', 'niveau': 2,
        'prototype': 'def detect_cycle(graph: dict[str, list[str]]) -> bool:',
        'sujet': 'Détectez la présence d\'au moins un cycle au sein d\'un graphe orienté '
                 'représenté par un dictionnaire (liste d\'adjacence).\n'
                 'Type de retour attendu : bool',
        'exemples': '1. input = {"A": ["B"], "B": ["C"], "C": ["A"]}\n   output = True\n\n'
                    '2. input = {"A": ["B"], "B": ["C"], "C": []}\n   output = False\n\n'
                    '3. input = {}\n   output = False',
        'capture_print': False,
        'tests': [
            ({"A": ["B"], "B": ["C"], "C": ["A"]}, True),
            ({"A": ["B"], "B": ["C"], "C": []}, False),
            ({}, False),
            ({"A": ["A"]}, True), # Self-loop
            ({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}, False), # Graph en diamant (pas de cycle)
            ({"A": ["B"], "B": ["C"], "C": ["D"], "D": ["E"], "E": ["C"]}, True),
            ({"1": ["2"], "2": ["3"], "3": [], "4": ["5"], "5": ["4"]}, True), # Graphe non connexe avec cycle
            ({"A": []}, False),
            ({"A": ["B"], "B": ["A"]}, True),
            ({"A": ["B", "C"], "B": ["C", "D"], "C": ["E"], "D": ["F"], "E": ["F", "G"], "F": ["H"], "G": ["H"], "H": []}, False) # Complexe acyclique
        ]
    },
    {
        'nom': 'Find Shortest Path',
        'categorie': 'challenging', 'niveau': 3,
        'prototype': 'def find_shortest_path(grid: list[list[int]], start: tuple[int, int], end: tuple[int, int]) -> int:',
        'sujet': 'Déterminez le nombre minimal de transitions pour aller de `start` à `end` '
                 'dans une grille (0 = libre, 1 = mur). Mouvements sur les 4 axes cardinaux.\n'
                 'Retournez -1 si aucun chemin n\'est possible.\n'
                 'Type de retour attendu : int',
        'exemples': '1. grid=[[0, 0], [0, 0]], start=(0,0), end=(1,1)\n   output = 2\n\n'
                    '2. grid=[[0, 1], [1, 0]], start=(0,0), end=(1,1)\n   output = -1\n\n'
                    '3. grid=[[0]], start=(0,0), end=(0,0)\n   output = 0',
        'capture_print': False,
        'tests': [
            (([[0, 0], [0, 0]], (0,0), (1,1)), 2),
            (([[0, 1], [0, 0]], (0,0), (1,1)), 2),
            (([[0, 1, 0], [0, 1, 0], [0, 0, 0]], (0,0), (0,2)), 6),
            (([[0, 1], [1, 0]], (0,0), (1,1)), -1), # Bloqué
            (([[0]], (0,0), (0,0)), 0), # Sur place
            (([[1]], (0,0), (0,0)), -1), # Départ dans un mur
            (([], (0,0), (1,1)), -1), # Grille vide
            (([[0, 0, 0], [1, 1, 0], [0, 0, 0]], (0,0), (2,0)), 6),
            (([[0, 0, 0, 0, 0]], (0,0), (0,4)), 4), # Ligne droite
            (
                (
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
                    ], 
                    (0, 0), # Départ en haut à gauche
                    (9, 9)  # Arrivée en bas à droite
                ), 
                54 # Résultat attendu
            )
        ]
    },
    {
        'nom': 'Maximal Square',
        'categorie': 'challenging', 'niveau': 3,
        'prototype': 'def maximal_square(matrix: list[list[str]]) -> int:',
        'sujet': 'Identifiez la taille du côté du plus grand carré composé exclusivement '
                 'd\'espaces vides `.` dans une matrice 2D (les `o` sont des murs).\n'
                 'Type de retour attendu : int',
        'exemples': "1. input = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]\n   output = 3\n\n"
                    "2. input = [['o', 'o'], ['o', 'o']]\n   output = 0\n\n"
                    "3. input = [['.', 'o'], ['o', '.']]\n   output = 1",
        'capture_print': False,
        'tests': [
            ([['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']], 3),
            ([['o', 'o'], ['o', 'o']], 0),
            ([['.', 'o'], ['o', '.']], 1),
            ([['.', '.', 'o'], ['.', '.', 'o'], ['o', 'o', 'o']], 2),
            ([['.']], 1),
            ([['o']], 0),
            ([], 0),
            ([['.', 'o', '.', '.', '.'], ['.', 'o', '.', '.', '.'], ['.', 'o', '.', '.', '.'], ['.', 'o', 'o', 'o', 'o']], 3),
            ([['.'] * 10], 1), # Ligne simple
            ([['.','.','.','.','o'],['.','.','.','.','.'],['.','.','.','.','.'],['.','.','.','.','.'],['o','.','.','.','o']], 4) # Complexe
        ]
    }
]

def main():
    print_header()
    print("Bienvenue dans le simulateur d'examen 42.")
    print("Sélectionne ton parcours :")
    print(f" {YELLOW}1{RESET} : Python basic")
    print(f" {YELLOW}2{RESET} : Python medium")
    print(f" {YELLOW}3{RESET} : Python challenging")
    print(f" {YELLOW}4{RESET} : Python in-depth")
    
    choix = input(f"\nTon choix (1-4) : {RESET}").strip()
    
    # Mapping des choix avec les catégories
    map_categories = {
        '1': 'basic',
        '2': 'medium',
        '3': 'challenging',
        '4': 'in-depth'
    }
    
    categorie_choisie = map_categories.get(choix)
    
    if not categorie_choisie:
        print(f"{RED}Choix invalide. Arrêt du programme.{RESET}")
        sys.exit()
        
    if categorie_choisie == 'in-depth':
        print(f"\n{CYAN}La catégorie 'Python in-depth' est en cours de construction. À bientôt !{RESET}")
        sys.exit()

    # Filtrage des exercices selon la catégorie
    exos_filtres = [ex for ex in EXERCICES if ex.get('categorie') == categorie_choisie]
    
    if not exos_filtres:
        print(f"{RED}Aucun exercice trouvé pour cette catégorie.{RESET}")
        sys.exit()

    # Organisation des exercices filtrés par niveau
    levels = {}
    for ex in exos_filtres:
        lvl = ex.get('niveau', 1)
        if lvl not in levels:
            levels[lvl] = []
        levels[lvl].append(ex)

    print(f"\nParcours sélectionné : {BOLD}{categorie_choisie.upper()}{RESET}")
    input(f"{YELLOW}Appuie sur Entrée pour commencer l'examen...{RESET}")

    # Boucle sur les niveaux dynamiques (basés sur les niveaux présents dans la catégorie)
    niveaux_presents = sorted(levels.keys())
    
    for niv in niveaux_presents:
        print(f"\n{CYAN}{'='*20} PASSAGE AU NIVEAU {niv} {'='*20}{RESET}")

        # 1. On récupère les exercices du niveau et on les mélange
        exos_courants = levels[niv].copy()
        random.shuffle(exos_courants)
        
        # 2. On commence par le premier exercice de la liste mélangée
        index_exo = 0
        exo = exos_courants[index_exo]

        while True:
            # Lancement du test
            result = run_tests(exo)
            
            if result == "exit":
                print(f"\n{RED}Arrêt du programme. À bientôt !{RESET}")
                sys.exit()
                
            elif result == "next":
                print(f"\n{YELLOW}>>> Changement d'exercice...{RESET}")
                time.sleep(0.5)
                # 3. On passe au suivant. 
                # Le modulo permet de revenir à 0 si on dépasse la fin de la liste
                index_exo = (index_exo + 1) % len(exos_courants)
                exo = exos_courants[index_exo]
                continue

            elif result == "up":
                print(f"\n{YELLOW}>>> Skip ! Passage forcé au niveau suivant...{RESET}")
                time.sleep(1)
                break  # On casse la boucle while, ce qui lance le niveau suivant

            elif result is True:
                # Exercice validé
                print(f"{GREEN}>>> Niveau {niv} validé ! Passage au suivant.{RESET}")
                time.sleep(1)
                break 
                
            else:
                # Exercice raté
                print(f"{RED}>>> Échec. Réessaie le même exercice.{RESET}")
                input(f"{YELLOW}Appuie sur Entrée...{RESET}")
                pass

    print(f"\n{GREEN}{'='*50}\nBRAVO ! TU AS FINI L'EXAMEN {categorie_choisie.upper()} !\n{'='*50}{RESET}")

if __name__ == "__main__":
    main()