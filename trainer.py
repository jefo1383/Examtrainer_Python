import sys
import time
import importlib.util
import os
import io
import re
import random
import inspect
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
    if not module:
        return False
    
    # --- DÉTECTION DE L'ARCHITECTURE POO AVANCÉE ---
    if 'classes_requises' in exercice:
        for class_name, required_methods in exercice['classes_requises'].items():
            
            # 1. Vérifier si la classe existe
            if not hasattr(module, class_name) or not inspect.isclass(getattr(module, class_name)):
                print(f"\n{RED}❌ ARCHITECTURE INVALIDE : La classe '{class_name}' est introuvable.{RESET}")
                print("   Objectif manqué : Tu dois créer la classe demandée.")
                return False
                
            # 2. Vérifier si les méthodes obligatoires existent dans cette classe
            user_class = getattr(module, class_name)
            for method_name in required_methods:
                # Cas spécial pour le constructeur (éviter la validation du constructeur par défaut)
                if method_name == '__init__':
                    if getattr(user_class, '__init__') is object.__init__:
                        print(f"\n{RED}❌ ARCHITECTURE INVALIDE : Le constructeur '__init__' est manquant.{RESET}")
                        print(f"   Objectif manqué : La classe '{class_name}' doit définir son propre '__init__'.")
                        return False
                else:
                    # Cas classique pour les autres méthodes
                    if not hasattr(user_class, method_name) or not callable(getattr(user_class, method_name)):
                        print(f"\n{RED}❌ ARCHITECTURE INVALIDE : La méthode '{method_name}' est introuvable.{RESET}")
                        print(f"   Objectif manqué : La classe '{class_name}' doit implémenter '{method_name}'.")
                        return False
    # ------------------------------------------------------

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
            (([8, 3, -1, -3, 5, 3, 6, 7, 9, 2, 4, 1, 5], 4), [8, 5, 5, 6, 7, 9, 9, 9, 9, 5]) # Cas complexe plus long
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
        'categorie': 'medium', 
        'niveau': 1,
        'prototype': 'def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:',
        'sujet': 'Générez une grille carrée de taille `size` x `size` sous forme de liste de chaînes.\n'
                 'Les espaces vides sont représentés par des points `.` et les étoiles par des `*`.\n'
                 'Les étoiles sont fournies sous la forme de tuples de coordonnées (ligne, colonne).\n'
                 'Règle : Si une étoile possède des coordonnées en dehors des limites de la grille, elle doit être ignorée.\n'
                 'Type de retour attendu : list[str]',
        'exemples': '1. input = ([(0, 0), (1, 1)], 2)\n'
                    '   output = ["*.", ".*"]\n\n'
                    '2. input = ([(0, 2), (5, 5)], 3)\n'
                    '   output = ["..*", "...", "..."]\n\n'
                    '3. input = ([], 1)\n'
                    '   output = ["."]',
        'capture_print': False,
        'tests': [
            (([(0, 0), (1, 1)], 2), ["*.", ".*"]),
            (([(0, 2)], 3), ["..*", "...", "..."]),
            (([], 1), ["."]),
            (([(0, 0), (0, 1), (0, 2)], 3), ["***", "...", "..."]),
            # TEST MODIFIÉ : Ajout de (5, 5) qui est > size, et (-1, 0) qui est < 0
            (([(2, 2), (5, 5), (-1, 0)], 3), ["...", "...", "..*"]), 
            (([(0, 0), (1, 3), (2, 2), (4, 4)], 5), ["*....", "...*.", "..*..", ".....", "....*"]),
            (([], 0), []),
            (([(1, 1), (1, 1)], 3), ["...", ".*.", "..."]),
            (([(i, i) for i in range(4)], 4), ["*...", ".*..", "..*.", "...*"]),
            (([(0,9), (1,8), (2,7), (3,6), (4,5), (5,4), (6,3), (7,2), (8,1), (9,0)], 10), 
             [".........*", "........*.", ".......*..", "......*...", ".....*....", "....*.....", "...*......", "..*.......", ".*........", "*........."])
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
    },

    # =======================================
    # === CATEGORIE : PYTHON CHALLENGING  ===
    # =======================================
    {
        'nom': 'Spiral Weaver',
        'categorie': 'challenging', 
        'niveau': 1,
        'prototype': 'def spiral_weaver(size: int) -> list[list[int]]:',
        'sujet': 'Générez une matrice carrée de taille `size * size`.\n'
                 'Remplissez-la avec les nombres de 1 à `size * size` en spirale,\n'
                 'en commençant en haut à gauche et en suivant la direction : droite -> bas -> gauche -> haut.\n'
                 'Type de retour attendu : list[list[int]]',
        'exemples': '1. input = 3\n'
                    '   output = [[1, 2, 3], [8, 9, 4], [7, 6, 5]]\n\n'
                    '2. input = 1\n'
                    '   output = [[1]]\n\n'
                    '3. input = 0\n'
                    '   output = []',
        'capture_print': False,
        'tests': [
            (3, [[1, 2, 3], [8, 9, 4], [7, 6, 5]]),
            (1, [[1]]),
            (2, [[1, 2], [4, 3]]),
            (4, [[1, 2, 3, 4], [12, 13, 14, 5], [11, 16, 15, 6], [10, 9, 8, 7]]),
            (0, []),
            (5, [[1, 2, 3, 4, 5], [16, 17, 18, 19, 6], [15, 24, 25, 20, 7], [14, 23, 22, 21, 8], [13, 12, 11, 10, 9]]),
            (6, [[1, 2, 3, 4, 5, 6], [20, 21, 22, 23, 24, 7], [19, 32, 33, 34, 25, 8], [18, 31, 36, 35, 26, 9], [17, 30, 29, 28, 27, 10], [16, 15, 14, 13, 12, 11]]),
            (7, [[1, 2, 3, 4, 5, 6, 7], [24, 25, 26, 27, 28, 29, 8], [23, 40, 41, 42, 43, 30, 9], [22, 39, 48, 49, 44, 31, 10], [21, 38, 47, 46, 45, 32, 11], [20, 37, 36, 35, 34, 33, 12], [19, 18, 17, 16, 15, 14, 13]]),
            (8, [[1, 2, 3, 4, 5, 6, 7, 8], [28, 29, 30, 31, 32, 33, 34, 9], [27, 48, 49, 50, 51, 52, 35, 10], [26, 47, 60, 61, 62, 53, 36, 11], [25, 46, 59, 64, 63, 54, 37, 12], [24, 45, 58, 57, 56, 55, 38, 13], [23, 44, 43, 42, 41, 40, 39, 14], [22, 21, 20, 19, 18, 17, 16, 15]]),
            (9, [[1, 2, 3, 4, 5, 6, 7, 8, 9], [32, 33, 34, 35, 36, 37, 38, 39, 10], [31, 56, 57, 58, 59, 60, 61, 40, 11], [30, 55, 72, 73, 74, 75, 62, 41, 12], [29, 54, 71, 80, 81, 76, 63, 42, 13], [28, 53, 70, 79, 78, 77, 64, 43, 14], [27, 52, 69, 68, 67, 66, 65, 44, 15], [26, 51, 50, 49, 48, 47, 46, 45, 16], [25, 24, 23, 22, 21, 20, 19, 18, 17]])
        ]
    },
    {
        'nom': 'Matrix Island',
        'categorie': 'challenging', 
        'niveau': 1,
        'prototype': 'def matrix_island(matrix: list[list[int]]) -> int:',
        'sujet': 'Retournez le nombre d\'îlots composées de `1` dans une matrice.\n'
                 'Un îlot est un groupe de `1` connectés horizontalement ou verticalement.\n'
                 'Type de retour attendu : int',
        'exemples': '1. input = [[1, 1, 0, 1, 1], [1, 1, 0, 1, 1]]\n'
                    '   output = 2\n\n'
                    '2. input = [[1, 1, 1, 1, 1], [1, 1, 0, 1, 1]]\n'
                    '   output = 1\n\n'
                    '3. input = []\n'
                    '   output = 0',
        'capture_print': False,
        'tests': [
            ([[1, 1, 0, 1, 1], [1, 1, 0, 1, 1]], 2),
            ([[1, 1, 1, 1, 1], [1, 1, 0, 1, 1]], 1),
            ([], 0),
            ([[0]], 0),
            ([[1]], 1),
            ([[1, 0, 1], [0, 1, 0], [1, 0, 1]], 5),
            ([[0, 0], [0, 0]], 0),
            ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 1),
            ([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], 4),
            ([[1, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0]], 2)
        ]
    },
    {
        'nom': 'Graph Cycle Resolver',
        'categorie': 'challenging', 
        'niveau': 2,
        'prototype': 'def graph_cycle_resolver(graph: dict[int, list[int]]) -> bool:',
        'sujet': 'Prend en paramètre un graphe orienté représenté sous forme de dictionnaire.\n'
                 'Retournez `True` si un cycle est détecté dans le graphe, sinon `False`.\n'
                 'Type de retour attendu : bool',
        'exemples': '1. input = {0: [1], 1: [2], 2: []}\n'
                    '   output = False\n\n'
                    '2. input = {0: [1], 1: [2], 2: [1]}\n'
                    '   output = True\n\n'
                    '3. input = {}\n'
                    '   output = False',
        'capture_print': False,
        'tests': [
            ({0: [1], 1: [2], 2: []}, False),
            ({0: [1], 1: [2], 2: [1]}, True),
            ({0: [1], 1: [3], 2: [3], 3: []}, False),
            ({}, False),
            ({0: [0]}, True),
            ({1: [2], 2: [3], 3: [4], 4: [5], 5: []}, False),
            ({1: [2], 2: [3], 3: [4], 4: [1]}, True),
            ({1: [2, 3], 2: [4], 3: [4], 4: []}, False),
            ({0: [1, 2], 1: [2], 2: [0]}, True),
            ({10: [20], 20: [30], 30: [40], 40: [50], 50: [20]}, True)
        ]
    },
    {
        'nom': 'Compression',
        'categorie': 'challenging', 
        'niveau': 2,
        'prototype': 'def compression(text: str, rule: str) -> str | None:',
        'sujet': 'Écrivez une fonction qui compresse ou décompresse une chaîne selon la règle ("compress" ou "decompress").\n'
                 'Compression : remplacez les répétitions par le caractère suivi du nombre (ex: "aaa" -> "a3").\n'
                 'Règle stricte : Si la chaîne compressée n\'est pas plus courte que l\'originale, on retourne la chaîne originale.\n'
                 'Décompression : inversez le processus. Retournez None si le format est invalide.\n'
                 'Type de retour attendu : str ou None',
        'exemples': '1. input = ("aabcccccaaa", "compress")\n'
                    '   output = "a2b1c5a3"\n\n'
                    '2. input = ("aabb", "compress")\n'
                    '   output = "aabb"\n\n'
                    '3. input = ("a2b1c5a3", "decompress")\n'
                    '   output = "aabcccccaaa"',
        'capture_print': False,
        'tests': [
            (("aabcccccaaa", "compress"), "a2b1c5a3"),
            (("abcd", "compress"), "abcd"),
            (("aabb", "compress"), "aabb"), 
            (("a2b1c5a3", "decompress"), "aabcccccaaa"),
            (("1a", "decompress"), None),
            (("", "compress"), ""),
            (("a", "decompress"), None),
            (("a0b1", "decompress"), None),
            (("aaabbbccc", "compress"), "a3b3c3"),
            (("a12", "decompress"), "aaaaaaaaaaaa")
        ]
    },
    {
        'nom': 'Word Ladder',
        'categorie': 'challenging', 
        'niveau': 2,
        'prototype': 'def word_ladder(start: str, end: str, word_list: list[str]) -> int:',
        'sujet': 'Trouvez la longueur du plus court chemin pour transformer le mot `start` en `end`.\n'
                 'A chaque étape, on ne change qu\'une lettre. Chaque mot intermédiaire doit être dans `word_list`.\n'
                 'S\'il n\'y a pas de chemin possible, retournez 0.\n'
                 'Type de retour attendu : int',
        'exemples': '1. input = ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])\n'
                    '   output = 5\n\n'
                    '2. input = ("a", "c", ["a", "b", "c"])\n'
                    '   output = 2\n\n'
                    '3. input = ("hot", "hot", ["hot"])\n'
                    '   output = 1',
        'capture_print': False,
        'tests': [
            (("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), 5),
            (("a", "c", ["a", "b", "c"]), 2),
            (("hot", "hot", ["hot"]), 1),
            (("hit", "cog", ["hot", "dot", "dog", "lot", "log"]), 0),
            (("cat", "dog", ["cot", "dot", "dog"]), 4),
            (("lead", "gold", ["load", "goad", "gold", "lead"]), 4),
            (("a", "z", ["b"]), 0),
            (("same", "same", []), 1),
            (("run", "walk", ["ran", "man"]), 0),
            (("cold", "warm", ["cord", "card", "ward", "warm"]), 5)
        ]
    },
    {
        'nom': 'Prisme Detector',
        'categorie': 'challenging', 
        'niveau': 2,
        'prototype': 'def prisme_detector(matrix: list[str], word: str) -> list[tuple[int, int, str]]:',
        'sujet': 'Cherchez toutes les occurrences d\'un mot dans une matrice de caractères.\n'
                 'Le mot peut être lu horizontalement, verticalement, en diagonale, et dans tous les sens.\n'
                 'Retournez une liste de tuples contenant (ligne, colonne, direction_name).\n'
                 'Directions : "up", "down", "left", "right", "up_left", "up_right", "down_left", "down_right".\n'
                 'Type de retour attendu : list[tuple[int, int, str]]',
        'exemples': '1. input = (["ABC", "DEF", "GHI"], "ABC")\n'
                    '   output = [(0, 0, "right")]\n\n'
                    '2. input = (["ABC", "DEF", "GHI"], "ADG")\n'
                    '   output = [(0, 0, "down")]\n\n'
                    '3. input = (["ABC", "DEF", "GHI"], "AFI")\n'
                    '   output = []',
        'capture_print': False,
        'tests': [
            ((["ABC", "DEF", "GHI"], "ABC"), [(0, 0, "right")]),
            ((["ABC", "DEF", "GHI"], "CBA"), [(0, 2, "left")]),
            ((["ABC", "DEF", "GHI"], "ADG"), [(0, 0, "down")]),
            ((["ABC", "DEF", "GHI"], "GDA"), [(2, 0, "up")]),
            ((["ABC", "DEF", "GHI"], "AEI"), [(0, 0, "down_right")]),
            ((["ABC", "DEF", "GHI"], "IEA"), [(2, 2, "up_left")]),
            ((["ABC", "DEF", "GHI"], "CEG"), [(0, 2, "down_left")]),
            ((["ABC", "DEF", "GHI"], "GEC"), [(2, 0, "up_right")]),
            ((["ABC", "DEF", "GHI"], "AFI"), []),
            ((["XY", "YX"], "XY"), [(0, 0, "right"), (0, 0, "down"), (1, 1, "up"), (1, 1, "left")])
        ]
    },
    {
        'nom': 'Meeting Planner',
        'categorie': 'challenging', 
        'niveau': 3,
        'prototype': 'def meeting_planner(meetings: list[list[int]]) -> dict:',
        'sujet': 'Placez une liste de réunions (start_time, end_time) dans un minimum de salles possibles.\n'
                 'Retournez un dictionnaire contenant :\n'
                 '- "needed_rooms" : le nombre minimal de salles.\n'
                 '- "rooms_assignements" : un sous-dictionnaire liant chaque numéro de salle à son planning.\n'
                 'Type de retour attendu : dict',
        'exemples': '1. input = [[9, 10], [9, 12], [10, 11], [11, 12]]\n'
                    '   output = {"needed_rooms": 2, "rooms_assignements": {1: [[9, 10], [10, 11], [11, 12]], 2: [[9, 12]]}}\n\n'
                    '2. input = []\n'
                    '   output = {"needed_rooms": 0, "rooms_assignements": {}}',
        'capture_print': False,
        'tests': [
            ([[9, 10], [9, 12], [10, 11], [11, 12]], {"needed_rooms": 2, "rooms_assignements": {1: [[9, 10], [10, 11], [11, 12]], 2: [[9, 12]]}}),
            ([], {"needed_rooms": 0, "rooms_assignements": {}}),
            ([[1, 2], [2, 3], [3, 4]], {"needed_rooms": 1, "rooms_assignements": {1: [[1, 2], [2, 3], [3, 4]]}}),
            ([[1, 5], [2, 5], [3, 5], [4, 5]], {"needed_rooms": 4, "rooms_assignements": {1: [[1, 5]], 2: [[2, 5]], 3: [[3, 5]], 4: [[4, 5]]}}),
            ([[10, 12], [12, 14], [10, 14]], {"needed_rooms": 2, "rooms_assignements": {1: [[10, 12], [12, 14]], 2: [[10, 14]]}}),
            ([[1, 2], [1, 2], [1, 2]], {"needed_rooms": 3, "rooms_assignements": {1: [[1, 2]], 2: [[1, 2]], 3: [[1, 2]]}}),
            ([[5, 10]], {"needed_rooms": 1, "rooms_assignements": {1: [[5, 10]]}}),
            ([[1, 3], [2, 4], [3, 5], [4, 6]], {"needed_rooms": 2, "rooms_assignements": {1: [[1, 3], [3, 5]], 2: [[2, 4], [4, 6]]}}),
            ([[0, 1], [0, 2], [1, 3], [2, 4]], {"needed_rooms": 2, "rooms_assignements": {1: [[0, 1], [1, 3]], 2: [[0, 2], [2, 4]]}}),
            ([[10, 11], [9, 10], [11, 12]], {"needed_rooms": 1, "rooms_assignements": {1: [[9, 10], [10, 11], [11, 12]]}})
        ]
    },
    {
        'nom': 'Course Schedule',
        'categorie': 'challenging',
        'niveau': 3,
        'prototype': 'def can_finish_courses(num_courses: int, prerequisites: list[list[int]]) -> bool:',
        'sujet': 'Les cours sont numérotés de 0 à `num_courses - 1`.\n'
                 'Chaque prérequis est défini sous la forme [cours, cours_requis].\n'
                 'Exemple : [1, 0] signifie que vous devez terminer le cours 0 avant le cours 1.\n'
                 'Retournez `True` s\'il est possible de terminer tous les cours, sinon `False` (s\'il y a un cycle).\n'
                 'Type de retour attendu : bool',
        'exemples': '1. input = (2, [[1, 0]])\n'
                    '   output = True\n\n'
                    '2. input = (2, [[1, 0], [0, 1]])\n'
                    '   output = False\n\n'
                    '3. input = (1, [])\n'
                    '   output = True',
        'capture_print': False,
        'tests': [
            ((2, [[1, 0]]), True),
            ((2, [[1, 0], [0, 1]]), False),
            ((4, [[1, 0], [2, 1], [3, 2]]), True),
            ((4, [[1, 0], [2, 1], [3, 2], [1, 3]]), False),
            ((1, []), True),
            ((5, [[1, 4], [2, 4], [3, 1], [3, 2]]), True),
            ((3, [[0, 1], [1, 2], [2, 0]]), False),
            ((5, []), True),
            ((6, [[1, 0], [2, 0], [3, 1], [4, 2], [5, 3], [5, 4]]), True),
            ((10, [[1, 0], [2, 1], [3, 2], [4, 3], [5, 4], [6, 5], [7, 6], [8, 7], [9, 8], [0, 9]]), False)
        ]
    },
    {
        'nom': 'Assign Meeting Rooms',
        'categorie': 'challenging',
        'niveau': 3,
        'prototype': 'def assign_meeting_rooms(intervals: list[list[int]]) -> list[list[list[int]]]:',
        'sujet': 'Répartissez des réunions `[start, end]` dans le minimum de salles possible.\n'
                 'Une réunion se terminant à `x` ne rentre pas en conflit avec une commençant à `x`.\n'
                 'Parcourez les salles existantes dans leur ordre de création.\nAssignez la réunion à la *première* '
                 'salle disponible.\nSi aucune ne convient, créez une nouvelle salle.\n'
                 'Les salles doivent etre dans l\'ordre chronologique des reunions.\n'
                 'Type de retour attendu : list[list[list[int]]]',
        'exemples': '1. input = [[0, 40], [5, 10], [15, 20]]\n'
                    '   output = [[[0, 40]], [[5, 10], [15, 20]]]\n\n'
                    '2. input = [[7, 10], [2, 4]]\n'
                    '   output = [[[2, 4], [7, 10]]]\n\n'
                    '3. input = []\n'
                    '   output = []',
        'capture_print': False,
        'tests': [
            ([[0, 40], [5, 10], [15, 20]], [[[0, 40]], [[5, 10], [15, 20]]]),
            ([[7, 10], [2, 4]], [[[2, 4], [7, 10]]]),
            ([], []),
            ([[1, 2], [2, 3], [3, 4]], [[[1, 2], [2, 3], [3, 4]]]),
            ([[1, 5], [2, 6], [3, 7]], [[[1, 5]], [[2, 6]], [[3, 7]]]),
            ([[1, 10], [2, 5], [6, 8], [9, 12]], [[[1, 10]], [[2, 5], [6, 8], [9, 12]]]),
            ([[1, 3], [1, 3], [1, 3]], [[[1, 3]], [[1, 3]], [[1, 3]]]),
            ([[5, 10]], [[[5, 10]]]),
            ([[10, 15], [5, 10], [0, 5]], [[[0, 5], [5, 10], [10, 15]]]),
            ([[1, 10], [2, 7], [3, 19], [8, 12], [10, 20], [11, 30]], [[[1, 10], [10, 20]], [[2, 7], [8, 12]], [[3, 19]], [[11, 30]]])
        ]
    },

    # =======================================
    # === CATEGORIE : PYTHON IN-DEPTH     ===
    # =======================================
    {
        'nom': 'Search Suggestions System',
        'categorie': 'in-depth',
        'niveau': 1,
        'prototype': 'def suggested_products(products: list[str], search_word: str) -> list[list[str]]:',
        'sujet': 'Étant donné une liste de noms de produits et un mot de recherche, retournez une liste de suggestions après chaque caractère tapé du mot de recherche.\n'
                 'Pour chaque préfixe du mot de recherche :\n'
                 '- trouvez tous les produits qui commencent par ce préfixe.\n'
                 '- retournez au maximum trois noms de produits.\n'
                 '- les suggestions doivent être triées par ordre lexicographique (alphabétique).\n'
                 'Si aucun produit ne correspond à un préfixe, retournez une liste vide pour ce préfixe.\n'
                 'Type de retour attendu : list[list[str]]',
        'exemples': '1. products = ["mobile", "mouse", "moneypot", "monitor", "mousepad"], search_word = "mouse"\n'
                    '   output = [["mobile", "moneypot", "monitor"], ["mobile", "moneypot", "monitor"], ["mouse", "mousepad"], ["mouse", "mousepad"], ["mouse", "mousepad"]]\n\n'
                    '2. products = ["havana"], search_word = "havana"\n'
                    '   output = [["havana"], ["havana"], ["havana"], ["havana"], ["havana"], ["havana"]]\n\n'
                    '3. products = ["bags","baggage","banner","box","cloths"], search_word = "bags"\n'
                    '   output = [["baggage", "bags", "banner"], ["baggage", "bags", "banner"], ["baggage", "bags"], ["bags"]]',
        'capture_print': False,
        'tests': [
            ((["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mouse"), [["mobile", "moneypot", "monitor"], ["mobile", "moneypot", "monitor"], ["mouse", "mousepad"], ["mouse", "mousepad"], ["mouse", "mousepad"]]),
            ((["havana"], "havana"), [["havana"], ["havana"], ["havana"], ["havana"], ["havana"], ["havana"]]),
            ((["bags", "baggage", "banner", "box", "cloths"], "bags"), [["baggage", "bags", "banner"], ["baggage", "bags", "banner"], ["baggage", "bags"], ["bags"]]),
            ((["havana"], "tatiana"), [[], [], [], [], [], [], []]),
            (([], "test"), [[], [], [], []]),
            ((["apple", "app", "application", "aptitude"], "app"), [["app", "apple", "application"], ["app", "apple", "application"], ["app", "apple", "application"]]),
            ((["a", "b", "c", "d"], "a"), [["a"]]),
            ((["zebra", "zorro", "zero", "z"], "z"), [["z", "zebra", "zero"]]),
            ((["abcd", "abce", "abcf", "abcg", "abch"], "abc"), [["abcd", "abce", "abcf"], ["abcd", "abce", "abcf"], ["abcd", "abce", "abcf"]]),
            ((["x", "xy", "xyz"], "xyza"), [["x", "xy", "xyz"], ["xy", "xyz"], ["xyz"], []])
        ]
    },
    {
        'nom': 'Set Merge / Union Find',
        'categorie': 'in-depth',
        'niveau': 2,
        'classes_requises': {'UnionFind': ['__init__', 'find', 'union', 'connected']},
        'prototype': 'def simulate_union_find(n: int, operations: list[tuple[str, int, int]]) -> list[int]:',
        'sujet': 'Implémentez une structure de données UnionFind.\n'
                 'La structure doit supporter :\n'
                 '  - trouver le représentant d\'une valeur\n'
                 '  - fusionner deux ensembles\n'
                 '  - vérifier si deux valeurs sont connectées\n\n'
                 'Méthodes :\n'
                 '  __init__(n)\n'
                 '    Créer n ensembles séparés.\n\n'
                 '  find(x)\n'
                 '    Retourner le représentant de l\'ensemble contenant x.\n'
                 '    Retourner -1 si x n\'est pas présent.\n\n'
                 '  union(x, y)\n'
                 '    Fusionner les ensembles contenant x et y.\n'
                 '    Retourner True si une fusion a eu lieu.\n'
                 '    Retourner False si x et y étaient déjà dans le même ensemble.\n\n'
                 '  connected(x, y)\n'
                 '    Retourner True si x et y sont dans le même ensemble.\n'
                 '    Retourner False sinon.\n\n'
                 'Implémentez la classe ET la fonction utilitaire `simulate_union_find(n, operations)`.\n'
                 'Type de retour attendu pour le wrapper : list[int]',
        'exemples': '1. n = 5, operations = [("connected", 0, 1), ("union", 0, 1), ("connected", 0, 1), ("union", 0, 1)]\n'
                    '   output = [0, 1, 1, 0]  (False, True, True, False)\n\n'
                    '2. n = 3, operations = [("union", 0, 1), ("union", 1, 2), ("connected", 0, 2)]\n'
                    '   output = [1, 1, 1]\n\n'
                    '3. n = 2, operations = [("find", 0, 0), ("find", 1, 0)]\n'
                    '   output = [0, 1] (En supposant que find retourne la racine)',
        'capture_print': False,
        'tests': [
            ((5, [("connected", 0, 1), ("union", 0, 1), ("connected", 0, 1), ("union", 0, 1)]), [0, 1, 1, 0]),
            ((3, [("union", 0, 1), ("union", 1, 2), ("connected", 0, 2)]), [1, 1, 1]),
            ((4, [("connected", 0, 3), ("union", 0, 1), ("union", 2, 3), ("union", 1, 2), ("connected", 0, 3)]), [0, 1, 1, 1, 1]),
            ((2, [("union", 0, 0)]), [0]),
            ((1, [("connected", 0, 0)]), [1]),
            ((5, [("union", 0, 1), ("union", 2, 3), ("connected", 1, 2)]), [1, 1, 0]),
            ((10, [("union", i, i+1) for i in range(9)] + [("connected", 0, 9)]), [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            ((3, [("union", 0, 1), ("union", 0, 1), ("union", 0, 1)]), [1, 0, 0]),
            ((4, [("connected", 1, 3)]), [0]),
            ((6, [("union", 0, 1), ("union", 4, 5), ("union", 2, 3), ("union", 1, 2), ("connected", 0, 3), ("connected", 0, 5)]), [1, 1, 1, 1, 1, 0])
        ]
    },
    {
        'nom': 'LRU Cache',
        'categorie': 'in-depth',
        'niveau': 2,
        'classes_requises': {'LRUCache': ['__init__', 'get', 'put']},
        'prototype': 'def simulate_lru_cache(capacity: int, operations: list[tuple[str, int, int]]) -> list[int]:',
        'sujet': 'Implémentez une classe de cache LRU (Least Recently Used).\n'
                 'Le cache stocke des clés entières et des valeurs entières.\n'
                 'Il a une capacité positive fixe.\n\n'
                 'Méthodes :\n'
                 '  __init__(capacity)\n'
                 '    Créer un cache vide avec la capacité donnée.\n\n'
                 '  get(key)\n'
                 '    Si la clé existe, retourner sa valeur et la marquer comme récemment utilisée.\n'
                 '    Si la clé n\'existe pas, retourner -1.\n\n'
                 '  put(key, value)\n'
                 '    Insérer ou mettre à jour la clé avec la valeur.\n'
                 '    Marquer la clé comme récemment utilisée.\n'
                 '    Si le cache dépasse sa capacité, supprimer la clé la moins récemment utilisée.\n\n'
                 'Implémentez la classe ET la fonction utilitaire `simulate_lru_cache(capacity, operations)`.\n'
                 'Retournez une liste contenant UNIQUEMENT les résultats des "get".\n'
                 'Type de retour attendu pour le wrapper : list[int]',
        'exemples': '1. capacity = 2, operations = [("put", 1, 1), ("put", 2, 2), ("get", 1, 0), ("put", 3, 3), ("get", 2, 0)]\n'
                    '   output = [1, -1]\n\n'
                    '2. capacity = 1, operations = [("put", 1, 1), ("get", 1, 0), ("put", 2, 2), ("get", 1, 0)]\n'
                    '   output = [1, -1]\n\n'
                    '3. capacity = 2, operations = [("get", 5, 0)]\n'
                    '   output = [-1]',
        'capture_print': False,
        'tests': [
            ((2, [("put", 1, 1), ("put", 2, 2), ("get", 1, 0), ("put", 3, 3), ("get", 2, 0), ("put", 4, 4), ("get", 1, 0), ("get", 3, 0), ("get", 4, 0)]), [1, -1, -1, 3, 4]),
            ((1, [("put", 1, 1), ("get", 1, 0), ("put", 2, 2), ("get", 1, 0)]), [1, -1]),
            ((2, [("get", 5, 0)]), [-1]),
            ((2, [("put", 2, 1), ("put", 1, 1), ("put", 2, 3), ("put", 4, 1), ("get", 1, 0), ("get", 2, 0)]), [-1, 3]),
            ((3, [("put", 1, 1), ("put", 2, 2), ("put", 3, 3), ("put", 4, 4), ("get", 4, 0), ("get", 3, 0), ("get", 2, 0), ("get", 1, 0), ("put", 5, 5), ("get", 1, 0), ("get", 2, 0), ("get", 3, 0), ("get", 4, 0), ("get", 5, 0)]), [4, 3, 2, -1, -1, 2, 3, -1, 5]),
            ((2, [("put", 2, 1), ("put", 2, 2), ("get", 2, 0), ("put", 1, 1), ("put", 4, 1), ("get", 2, 0)]), [2, -1]),
            ((1, [("put", 1, 10), ("put", 2, 20), ("put", 3, 30), ("get", 1, 0), ("get", 2, 0), ("get", 3, 0)]), [-1, -1, 30]),
            ((4, [("put", 1, 1), ("put", 2, 2), ("put", 3, 3), ("get", 1, 0), ("put", 4, 4), ("put", 5, 5), ("get", 2, 0), ("get", 3, 0)]), [1, -1, 3]),
            ((2, [("put", 1, 0), ("put", 2, 2), ("get", 1, 0), ("put", 3, 3), ("get", 2, 0), ("put", 4, 4), ("get", 1, 0), ("get", 3, 0), ("get", 4, 0)]), [0, -1, -1, 3, 4]),
            ((2, []), [])
        ]
    },
    {
        'nom': 'Bridge Connections',
        'categorie': 'in-depth',
        'niveau': 3,
        'prototype': 'def find_bridges(graph: dict[int, list[int]]) -> list[tuple[int, int]]:',
        'sujet': 'Étant donné un graphe non orienté, retournez tous les ponts (bridges) du graphe.\n'
                 'Un pont est une arête qui déconnecte le graphe si elle est supprimée.\n'
                 'Règles :\n'
                 '- Retournez chaque pont une seule fois.\n'
                 '- Chaque arête retournée doit être ordonnée ainsi : (noeud_le_plus_petit, noeud_le_plus_grand).\n'
                 '- La liste finale doit être triée par ordre croissant.\n'
                 'Type de retour attendu : list[tuple[int, int]]',
        'exemples': '1. graph = {0: [1], 1: [0, 2], 2: [1]}\n'
                    '   output = [(0, 1), (1, 2)]\n\n'
                    '2. graph = {0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2]}\n'
                    '   output = [(2, 3)]\n\n'
                    '3. graph = {0: [1, 2], 1: [0, 2], 2: [0, 1]}\n'
                    '   output = []',
        'capture_print': False,
        'tests': [
            ({0: [1], 1: [0, 2], 2: [1]}, [(0, 1), (1, 2)]),
            ({0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2]}, [(2, 3)]),
            ({0: [1, 2], 1: [0, 2], 2: [0, 1]}, []),
            ({0: [1], 1: [0]}, [(0, 1)]),
            ({0: []}, []),
            ({0: [1], 1: [0], 2: [3], 3: [2]}, [(0, 1), (2, 3)]),
            ({0: [1, 2, 3], 1: [0], 2: [0], 3: [0]}, [(0, 1), (0, 2), (0, 3)]),
            ({0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2, 4, 5], 4: [3, 5], 5: [3, 4]}, [(2, 3)]),
            ({0: [1, 2, 3], 1: [0, 2, 3], 2: [0, 1, 3], 3: [0, 1, 2]}, []),
            ({0: [1], 1: [0, 2], 2: [1, 3], 3: [2, 4], 4: [3]}, [(0, 1), (1, 2), (2, 3), (3, 4)])
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