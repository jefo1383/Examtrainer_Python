import sys
import time
import importlib.util
import os
import io
import re
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
    print(f"      EXAM TRAINER - 42 - PYTHON BASIC")
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
    func_name = get_function_name(exercice['prototype'])
    if not func_name:
        print(f"{RED}Erreur config: Prototype invalide pour {exercice['nom']}{RESET}")
        return False

    print(f"{BOLD}Exercice : {exercice['nom']}{RESET}\n")
    print(f"Prototype : {YELLOW}{exercice['prototype']}{RESET}\n")
    print(f"Consigne : {exercice['sujet']}\n")
    print(f"Exemples :\n{CYAN}{exercice['exemples']}{RESET}\n")
    print(f"{YELLOW}Modifie 'solution.py' et appuie sur Entrée...{RESET}")
    input()

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
                if isinstance(args, tuple): result = user_func(*args)
                else: result = user_func(args)
                
            if result != expected:
                print(f"\n{RED}❌ TEST {i+1} ÉCHOUÉ{RESET}")
                print(f"   Entrée   : {args}")
                print(f"   Attendu  : {repr(expected)}")
                print(f"   Reçu     : {repr(result)}")
                return False
            else:
                print(f"{GREEN}TEST {i+1} ---------- 🔥{RESET}")

        except Exception as e:
            print(f"\n{RED}❌ ERREUR TEST {i+1}: {e}{RESET}")
            return False

    print(f"\n{GREEN}✅ EXERCICE VALIDÉ !{RESET}\n")
    time.sleep(1)
    return True


EXERCICES = [
    # === NIVEAU 1 ===
    {
        'nom': '1. Case Letter',
        'niveau': 1,
        'prototype': 'def case_letter(string: str) -> str:',
        'sujet': 'Modifiez la casse (min/maj) sur les lettres de la string reçue en argument.\n'
                 'La première lettre doit être en minuscule, la deuxième en majuscule, etc.\n'
                 'Les chiffres et caractères spéciaux ne doivent pas être modifiés (et ne comptent pas).',
        'exemples': 'input = "Hello world"\n'
                    'output attendu = "hElLo WoRlD"\n'
                    '\n'
                    'input = "we123lcome"\n'
                    'output attendu = "wE123lCoMe"\n'
                    '\n'
                    'input = "Python! 3.10"\n'
                    'output attendu = "pYtHoN! 3.10"\n',
        'capture_print': False,
        'tests': [
            ("Hello world", "hElLo WoRlD"),
            ("we123lcome", "wE123lCoMe"),
            ("Python! 3.10", "pYtHoN! 3.10"),
            ("", ""),
            ("123456", "123456"),
            ("...---...", "...---..."),
            ("A", "a"),
            ("a b c", "a B c"),
            ("hELLO", "hElLo"),
            ("42 is THE answer", "42 iS tHe AnSwEr")
        ]
    },
    {
        'nom': '2. FizzBuzz',
        'niveau': 1,
        'prototype': 'def fizzbuzz(n: int) -> None:',
        'sujet': 'Écrivez un programme qui affiche n nombres, séparés par un saut de ligne.\n'
                 'Si le nombre est un multiple de 3, il affiche « fizz ».\n'
                 'Si le nombre est un multiple de 5, il affiche « buzz ».\n'
                 'Si le nombre est à la fois un multiple de 3 et un multiple de 5, il affiche « fizzbuzz ».',
        'exemples': 'n = 10\n1\n2\nfizz\n4\nbuzz\nfizz\n7\n8\nfizz\nbuzz\n11\nfizz\n13\n14\nfizzbuzz',
        'capture_print': True,
        'tests': [
            (3, "1\n2\nfizz"),
            (5, "1\n2\nfizz\n4\nbuzz"),
            (15, "1\n2\nfizz\n4\nbuzz\nfizz\n7\n8\nfizz\nbuzz\n11\nfizz\n13\n14\nfizzbuzz"),
            (1, "1"),
            (0, ""),
            (-5, ""),
            (2, "1\n2"),
            (6, "1\n2\nfizz\n4\nbuzz\nfizz"),
            (10, "1\n2\nfizz\n4\nbuzz\nfizz\n7\n8\nfizz\nbuzz"),
            (16, "1\n2\nfizz\n4\nbuzz\nfizz\n7\n8\nfizz\nbuzz\n11\nfizz\n13\n14\nfizzbuzz\n16"),
            # 11. Test long (100)
            (100, 
             "1\n2\nfizz\n4\nbuzz\nfizz\n7\n8\nfizz\nbuzz\n11\nfizz\n13\n14\nfizzbuzz\n16\n17\nfizz\n19\nbuzz\nfizz\n22\n23\nfizz\nbuzz\n"
             "26\nfizz\n28\n29\nfizzbuzz\n31\n32\nfizz\n34\nbuzz\nfizz\n37\n38\nfizz\nbuzz\n41\nfizz\n43\n44\nfizzbuzz\n46\n47\nfizz\n49\nbuzz\n"
             "fizz\n52\n53\nfizz\nbuzz\n56\nfizz\n58\n59\nfizzbuzz\n61\n62\nfizz\n64\nbuzz\nfizz\n67\n68\nfizz\nbuzz\n71\nfizz\n73\n74\nfizzbuzz\n"
             "76\n77\nfizz\n79\nbuzz\nfizz\n82\n83\nfizz\nbuzz\n86\nfizz\n88\n89\nfizzbuzz\n91\n92\nfizz\n94\nbuzz\nfizz\n97\n98\nfizz\nbuzz")
        ]
    },
    
    # === NIVEAU 2 ===
    {
        'nom': '3. Matrix Reverse',
        'niveau': 2,
        'prototype': 'def matrix_reverse(matrix: list[list[int]]) -> list[list[int]]:',
        'sujet': 'Vous recevez une matrice 2D en arguments. Retournez une matrice dont les éléments\n'
        'de chaque colonne sont inversés, mais où l\'ordre des lignes reste inchangé.',
        'exemples': 'input = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\n'
                    'output attendu = [[3, 2, 1], [6, 5, 4], [9, 8, 7]]\n'
                    '\n'
                    'input = [[], [6, 7, 8], [2, 5, 9]]\n'
                    'output attendu = [[], [8, 7, 6], [9, 5, 2]]\n',
        'capture_print': False,
        'tests': [
            ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[3, 2, 1], [6, 5, 4], [9, 8, 7]]),
            ([], []),
            ([[], []], [[], []]),
            ([[1, 2], [], [10]], [[2, 1], [], [10]]),
            ([[1, 2, 3, 4]], [[4, 3, 2, 1]]),
            ([[1], [2], [3]], [[1], [2], [3]]),
            ([[-1, -2], [-3, -4]], [[-2, -1], [-4, -3]]),
            ([[100, 2000]], [[2000, 100]]),
            ([[0, 1]], [[1, 0]]),
            ([[3, 2, 1]], [[1, 2, 3]])
        ]
    },

    # === NIVEAU 3 ===
    {
        'nom': '4. Swap Chunk',
        'niveau': 3,
        'prototype': 'def swap_chunk(arr: list[int], k: int) -> list[int]:',
        'sujet': 'Déplacez les k derniers éléments de la liste donnee en argument au début de la liste.\n'
                 'La liste d origine ne doit pas etre modifiee\n'
                 'La fonction doit fonctionner si k est plus grand que la liste',
        'exemples': 'input = [0, 1, 2, 3, 4, 5] k = 2\n'
                    'output attendu = [4, 5, 0, 1, 2, 3]\n'
                    '\n'
                    'input = [1, 2, 3, 4]   k = 10\n'
                    'output attendu = [3, 4, 1, 2]',
        'capture_print': False,
        'tests': [
            (([0, 1, 2, 3, 4, 5], 2), [4, 5, 0, 1, 2, 3]),
            (([1, 2, 3, 4], 10), [3, 4, 1, 2]),
            (([1, 2, 3], 0), [1, 2, 3]),
            (([], 5), []),
            (([1, 2, 3], 3), [1, 2, 3]),
            (([1, 2], 4), [1, 2]),
            (([9], 5), [9]),
            (([1, 2, 3], 3001), [3, 1, 2]),
            (([1, 2, 3], 1), [3, 1, 2]),
            (([7, 41, 32], 3), [7, 41, 32])
        ]
    },

    # === NIVEAU 4 ===
    {
        'nom': '5. Convert Base',
        'niveau': 4,
        'prototype': 'def convert_base(n: str, base_from: int, base_to: int) -> str:',
        'sujet': 'Convertit la string "n" de base "base_from" donnee en argument\n'
                 'en base "base_to" et retourne une string convertie.',
        'exemples': 'input = ("10", 10, 2)\n'
                    'output attendu = "1010"\n'
                    '\n'
                    'input = ("1A", 16, 10)\n'
                    'output attendu = "26"',
        'capture_print': False,
        'tests': [
            (("10", 10, 2), "1010"),
            (("1A", 16, 10), "26"),
            (("1010", 2, 16), "A"),
            (("42", 10, 16), "2A"),
            (("0", 10, 2), "0"),
            (("Z", 36, 10), "35"),
            (("1000", 2, 36), "8"),
            (("10", 1, 10), None),
            (("10", 10, 37), None),
            (("FF", 16, 2), "11111111")
        ]
    },
    {
        'nom': '6. Crispy Sort',
        'niveau': 4,
        'prototype': 'def crispy_sort(strings: list[str]) -> list[str]:',
        'sujet': 'Trier la liste donnee en argument par 3 criteres avec ordre de priorite:\n'
                 '1.Longueur, 2.Nombre de voyelles, 3.Ordre alphabetique.\n'
                 'et retourner la liste triee. Les listes vides doivent etre gerees.',
        'exemples': 'input = ["ccc", "bb", "a"]\n'
                    'output attendu = ["a", "bb", "ccc"]\n'
                    '\n'
                    'input = ["chat", "char"]\n'
                    'output attendu = ["char", "chat"]\n'
                    '\n'
                    'input = ["", "a", ""]\n'
                    'output = ["", "", "a"]',
        'capture_print': False,
        'tests': [
            (["ccc", "bb", "a"], ["a", "bb", "ccc"]),
            (["chat", "char"], ["char", "chat"]),
            (["banane", "pomme", "kiwi", "sac", "arc", "a", ""], 
             ["", "a", "arc", "sac", "kiwi", "pomme", "banane"]),
            ([], []),
            (["", "a", ""], ["", "", "a"]),
            (["test", "test"], ["test", "test"]),
            (["a", "Z"], ["Z", "a"]),
            (["aa", "bz"], ["bz", "aa"]),
            (["solo"], ["solo"]),
            (["ddd", "cc", "b", "a"], ["b", "a", "cc", "ddd"])
        ]
    }
]

def main():
    print_header()
    for i, exo in enumerate(EXERCICES):
        niveau = exo.get('niveau', '?') 
        print(f"{CYAN}--- NIVEAU {niveau} ---{RESET}")
        
        while not run_tests(exo):
            print(f"{YELLOW}Réessaie... (Entrée){RESET}")
            input()
            print_header()
    print(f"\n{GREEN}{'='*50}\nBRAVO ! TOUS LES EXERCICES SONT VALIDÉS !\n{'='*50}{RESET}")

if __name__ == "__main__":
    main()