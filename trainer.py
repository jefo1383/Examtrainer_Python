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
    """
    Exécute les tests pour un exercice donné.
    Retourne : 
      True  -> Exercice réussi
      False -> Exercice raté
      "next" -> L'utilisateur veut changer d'exercice
      "exit" -> L'utilisateur veut quitter
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
    user_input = input(f"Commandes : 'next' pour changer, 'exit' pour quitter... {RESET}")
    
    cmd = user_input.strip().lower()
    if cmd == "exit": return "exit"
    if cmd == "next": return "next"

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


# --- LISTE COMPLETE DES 12 EXERCICES ---

EXERCICES = [
    # === NIVEAU 1 ===
    {
        'nom': '1. Case Letter',
        'niveau': 1,
        'prototype': 'def case_letter(string: str) -> str:',
        'sujet': 'Écrivez une fonction qui transforme la chaîne de caractères donnée en alternant la casse.\n'
                 'Le premier caractère doit être en minuscule, le second en majuscule, et ainsi de suite.\n'
                 'Les caractères non-alphabétiques doivent rester inchangés mais comptent dans le positionnement.\n'
                 'Type de retour attendu : str',
        'exemples': '1. input = "Hello world"\n'
                    '   output = "hElLo WoRlD"\n\n'
                    '2. input = "we123lcome"\n'
                    '   output = "wE123lCoMe"\n\n'
                    '3. input = "Python 3.8"\n'
                    '   output = "pYtHoN 3.8"',
        'capture_print': False,
        'tests': [
            ("Hello world", "hElLo WoRlD"),
            ("we123lcome", "wE123lCoMe"),
            ("Python! 3.10", "pYtHoN! 3.10"),
            ("", ""),
            ("123456", "123456"),
            ("A", "a"),
            ("a b c", "a B c"),
            ("   ", "   "),
            ("zZzZ", "zZzZ"),
            ("A!B@C#", "a!B@c#")
        ]
    },
    {
        'nom': '2. FizzBuzz',
        'niveau': 1,
        'prototype': 'def fizzbuzz(n: int) -> None:',
        'sujet': 'Écrivez un programme qui affiche les nombres de 1 à n inclus, suivis d\'un saut de ligne.\n'
                 'Pour les multiples de 3, affichez "fizz" au lieu du nombre.\n'
                 'Pour les multiples de 5, affichez "buzz".\n'
                 'Pour les multiples de 3 et 5, affichez "fizzbuzz".\n'
                 'Type de retour attendu : None (Affichage sur la sortie standard)',
        'exemples': '1. n = 3\n'
                    '   1\n   2\n   fizz\n\n'
                    '2. n = 5\n'
                    '   1\n   2\n   fizz\n   4\n   buzz\n\n'
                    '3. n = 0\n'
                    '   (Aucun affichage)',
        'capture_print': True,
        'tests': [
            (3, "1\n2\nfizz"),
            (5, "1\n2\nfizz\n4\nbuzz"),
            (15, "1\n2\nfizz\n4\nbuzz\nfizz\n7\n8\nfizz\nbuzz\n11\nfizz\n13\n14\nfizzbuzz"),
            (1, "1"),
            (0, ""),
            (2, "1\n2"),
            (6, "1\n2\nfizz\n4\nbuzz\nfizz"),
            (10, "1\n2\nfizz\n4\nbuzz\nfizz\n7\n8\nfizz\nbuzz"),
            (-5, ""),
            (100, 
             "1\n2\nfizz\n4\nbuzz\nfizz\n7\n8\nfizz\nbuzz\n11\nfizz\n13\n14\nfizzbuzz\n16\n17\nfizz\n19\nbuzz\nfizz\n22\n23\nfizz\nbuzz\n"
             "26\nfizz\n28\n29\nfizzbuzz\n31\n32\nfizz\n34\nbuzz\nfizz\n37\n38\nfizz\nbuzz\n41\nfizz\n43\n44\nfizzbuzz\n46\n47\nfizz\n49\nbuzz\n"
             "fizz\n52\n53\nfizz\nbuzz\n56\nfizz\n58\n59\nfizzbuzz\n61\n62\nfizz\n64\nbuzz\nfizz\n67\n68\nfizz\nbuzz\n71\nfizz\n73\n74\nfizzbuzz\n"
             "76\n77\nfizz\n79\nbuzz\nfizz\n82\n83\nfizz\nbuzz\n86\nfizz\n88\n89\nfizzbuzz\n91\n92\nfizz\n94\nbuzz\nfizz\n97\n98\nfizz\nbuzz")
        ]
    },
    {
        'nom': '5. Convert Base',
        'niveau': 1, 
        'prototype': 'def convert_base(n: str, base_from: int, base_to: int) -> str:',
        'sujet': 'Implémentez une fonction qui convertit une chaîne de caractères représentant un nombre\n'
                 'd\'une base donnée vers une autre base cible. La fonction doit gérer les bases allant de 2 à 36.\n'
                 'Si les paramètres de base sont invalides, la fonction doit échouer silencieusement.\n'
                 'Type de retour attendu : str ou None',
        'exemples': '1. input = ("10", 10, 2)  (Décimal vers Binaire)\n'
                    '   output = "1010"\n\n'
                    '2. input = ("FF", 16, 10) (Hexa vers Décimal)\n'
                    '   output = "255"\n\n'
                    '3. input = ("10", 1, 10)  (Base invalide)\n'
                    '   output = None',
        'capture_print': False,
        'tests': [
            (("10", 10, 2), "1010"),
            (("1A", 16, 10), "26"),
            (("1010", 2, 16), "A"),
            (("42", 10, 16), "2A"),
            (("0", 10, 2), "0"),
            (("10", 1, 10), None),
            (("10", 10, 37), None),
            (("FF", 16, 2), "11111111"),
            (("Z", 36, 10), "35"),
            (("7", 8, 2), "111")
        ]
    },
    {
        'nom': '7. Bracket Validator',
        'niveau': 1,
        'prototype': 'def bracket_validator(s: str) -> bool:',
        'sujet': 'Développez un algorithme capable de vérifier la validité d\'une expression contenant\n'
                 'des parenthèses, des crochets et des accolades. Une expression est considérée comme valide\n'
                 'si tous les ouvrants sont correctement fermés dans le bon ordre d\'imbrication.\n'
                 'Type de retour attendu : bool',
        'exemples': '1. input = "{[]}"\n'
                    '   output = True\n\n'
                    '2. input = "([)]"\n'
                    '   output = False\n\n'
                    '3. input = "(("\n'
                    '   output = False',
        'capture_print': False,
        'tests': [
            ("{[]}", True),
            ("([)]", False),
            ("({[()]})", True),
            ("((", False),
            (")", False),
            ("", True),
            ("(((((((((())))))))))", True),
            ("[]{}()", True),
            ("[[[", False),
            ("{[()]}", True)
        ]
    },

    # === NIVEAU 2 ===
    {
        'nom': '3. Matrix Reverse',
        'niveau': 2,
        'prototype': 'def matrix_reverse(matrix: list[list[int]]) -> list[list[int]]:',
        'sujet': 'Créez une fonction qui inverse l\'ordre des éléments au sein de chaque colonne (sous-liste)\n'
                 'd\'une matrice donnée. La structure des lignes doit être préservée, seul le contenu\n'
                 'des "lignes" (listes internes) est inversé.\n'
                 'Type de retour attendu : list[list[int]]',
        'exemples': '1. input = [[1, 2], [3, 4]]\n'
                    '   output = [[2, 1], [4, 3]]\n\n'
                    '2. input = [[1, 2, 3]]\n'
                    '   output = [[3, 2, 1]]\n\n'
                    '3. input = []\n'
                    '   output = []',
        'capture_print': False,
        'tests': [
            ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[3, 2, 1], [6, 5, 4], [9, 8, 7]]),
            ([], []),
            ([[], []], [[], []]),
            ([[1, 2], [], [10]], [[2, 1], [], [10]]),
            ([[100, 2000]], [[2000, 100]]),
            ([[1]], [[1]]),
            ([[1, 2, 3, 4, 5]], [[5, 4, 3, 2, 1]]),
            ([[0, 0, 1]], [[1, 0, 0]]),
            ([[-1, -2]], [[-2, -1]]),
            ([[1, 2], [1]], [[2, 1], [1]])
        ]
    },
    {
        'nom': '12. Is Palindrome',
        'niveau': 2,
        'prototype': 'def is_palindrome(s: str) -> bool:',
        'sujet': 'Écrivez une fonction permettant de déterminer si une chaîne de caractères est un palindrome.\n'
                 'La comparaison doit être insensible à la casse et ne doit pas tenir compte des espaces.\n'
                 'Type de retour attendu : bool',
        'exemples': '1. input = "Kayak"\n'
                    '   output = True\n\n'
                    '2. input = "Elu par cette crapule"\n'
                    '   output = True\n\n'
                    '3. input = "Bonjour"\n'
                    '   output = False',
        'capture_print': False,
        'tests': [
            ("Kayak", True),
            ("test", False),
            ("A man a plan a canal Panama", True),
            ("Elu par cette crapule", True),
            ("", True),
            ("a", True),
            ("ab", False),
            ("Noon", True),
            ("Was it a car or a cat I saw", True),
            ("Python", False)
        ]
    },
    {
        'nom': '10. Sort Rev Matrix',
        'niveau': 2,
        'prototype': 'def sort_rev_matrix(matrix: list[list[int]]) -> list[list[int]]:',
        'sujet': 'Implémentez une fonction qui trie indépendamment chaque ligne d\'une matrice 2D.\n'
                 'Le tri doit s\'effectuer par ordre décroissant (valeurs numériques).\n'
                 'L\'ordre relatif des lignes dans la matrice ne doit pas être modifié.\n'
                 'Type de retour attendu : list[list[int]]',
        'exemples': '1. input = [[1, 5, 2], [8, 3]]\n'
                    '   output = [[5, 2, 1], [8, 3]]\n\n'
                    '2. input = [[10, 10, 10]]\n'
                    '   output = [[10, 10, 10]]\n\n'
                    '3. input = [[-5, 0, 5]]\n'
                    '   output = [[5, 0, -5]]',
        'capture_print': False,
        'tests': [
            ([[1, 5, 2], [8, 3]], [[5, 2, 1], [8, 3]]),
            ([[1, 2, 3]], [[3, 2, 1]]),
            ([[-5, -1, -10]], [[-1, -5, -10]]),
            ([], []),
            ([[10, 2, 30], [5, 5, 5]], [[30, 10, 2], [5, 5, 5]]),
            ([[1]], [[1]]),
            ([[1, 3], [2, 4]], [[3, 1], [4, 2]]),
            ([[0], [0, 1]], [[0], [1, 0]]),
            ([[100, 1, 50]], [[100, 50, 1]]),
            ([[-1, -2, -3]], [[-1, -2, -3]])
        ]
    },

    # === NIVEAU 3 ===
    {
        'nom': '4. Swap Chunk',
        'niveau': 3,
        'prototype': 'def swap_chunk(arr: list[int], k: int) -> list[int]:',
        'sujet': 'Déplacez les k derniers éléments de la liste vers le début de celle-ci.\n'
                 'La liste d\'origine ne doit pas être modifiée.\n'
                 'Seules des listes d\'entiers valides sont données en arguments.\n'
                 'Type de retour attendu : list[int]',
        'exemples': '1. input = [0, 1, 2, 3, 4, 5], k=2\n'
                    '   output = [4, 5, 0, 1, 2, 3]\n\n'
                    '2. input = [1, 2, 3], k=4\n'
                    '   output = [3, 1, 2]\n\n'
                    '3. input = [10, 20], k=1\n'
                    '   output = [20, 10]',
        'capture_print': False,
        'tests': [
            (([0, 1, 2, 3, 4, 5], 2), [4, 5, 0, 1, 2, 3]),
            (([1, 2, 3, 4], 10), [3, 4, 1, 2]),
            (([], 5), []),
            (([1, 2, 3], 3), [1, 2, 3]),
            # Ajout test valid (grand k) à la place du test string
            (([1, 2, 3, 4, 5], 7), [4, 5, 1, 2, 3]),
            (([1, 2, 3], 0), [1, 2, 3]),
            (([1], 10), [1]),
            (([1, 2], 1), [2, 1]),
            (([10, 20, 30], 2), [20, 30, 10]),
            # Ajout test valid (negatifs) à la place du test mixte
            (([-10, -20, -30], 1), [-30, -10, -20])
        ]
    },
    {
        'nom': '8. Rot 13',
        'niveau': 3,
        'prototype': 'def rot13(txt: str) -> str:',
        'sujet': 'Reproduisez l\'algorithme de chiffrement par substitution ROT13.\n'
                 'Chaque lettre alphabétique doit être décalée de 13 positions.\n'
                 'La casse doit être préservée et les caractères spéciaux ignorés.\n'
                 'Type de retour attendu : str',
        'exemples': '1. input = "abc"\n'
                    '   output = "nop"\n\n'
                    '2. input = "Hello World!"\n'
                    '   output = "Uryyb Jbeyq!"\n\n'
                    '3. input = "12345"\n'
                    '   output = "12345"',
        'capture_print': False,
        'tests': [
            ("abc", "nop"),
            ("nop", "abc"),
            ("Hello World!", "Uryyb Jbeyq!"),
            ("Python 3.10", "Clguba 3.10"),
            ("", ""),
            ("1234567890", "1234567890"),
            ("M", "Z"),
            ("N", "A"),
            ("z", "m"),
            ("a", "n")
        ]
    },
    {
        'nom': '11. Transpose Matrix',
        'niveau': 3,
        'prototype': 'def transpose_matrix(matrix: list[list[int]]) -> list[list[int]]:',
        'sujet': 'Calculez et retournez la transposée de la matrice fournie en entrée.\n'
                 'L\'opération consiste à échanger les lignes et les colonnes.\n'
                 'Type de retour attendu : list[list[int]]',
        'exemples': '1. input = [[1, 2, 3], [4, 5, 6]]\n'
                    '   output = [[1, 4], [2, 5], [3, 6]]\n\n'
                    '2. input = [[1], [2], [3]]\n'
                    '   output = [[1, 2, 3]]\n\n'
                    '3. input = []\n'
                    '   output = []',
        'capture_print': False,
        'tests': [
            ([[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]]),
            ([[1, 2], [3, 4]], [[1, 3], [2, 4]]),
            ([[1], [2], [3]], [[1, 2, 3]]),
            ([], []),
            ([[1]], [[1]]),
            ([[1, 2, 3]], [[1], [2], [3]]),
            ([[1, 2], [3, 4], [5, 6]], [[1, 3, 5], [2, 4, 6]]),
            ([[0, 0], [1, 1]], [[0, 1], [0, 1]]),
            ([[10, 20], [30, 40]], [[10, 30], [20, 40]]),
            ([[-1]], [[-1]])
        ]
    },

    # === NIVEAU 4 ===
    {
        'nom': '6. Crispy Sort',
        'niveau': 4,
        'prototype': 'def crispy_sort(strings: list[str]) -> list[str]:',
        'sujet': 'Triez une liste de chaînes de caractères en appliquant successivement les critères suivants :\n'
                 '1. La longueur de la chaîne (croissant).\n'
                 '2. Le nombre de voyelles présentes (croissant).\n'
                 '3. L\'ordre alphabétique standard (croissant).\n'
                 'Type de retour attendu : list[str]',
        'exemples': '1. input = ["aa", "bz"]\n'
                    '   output = ["bz", "aa"]\n\n'
                    '2. input = ["ccc", "bb", "a"]\n'
                    '   output = ["a", "bb", "ccc"]\n\n'
                    '3. input = ["chat", "char"]\n'
                    '   output = ["char", "chat"]',
        'capture_print': False,
        'tests': [
            (["ccc", "bb", "a"], ["a", "bb", "ccc"]),
            (["chat", "char"], ["char", "chat"]),
            (["banane", "pomme", "kiwi", "sac", "arc", "a", ""], 
             ["", "a", "arc", "sac", "kiwi", "pomme", "banane"]),
            ([], []),
            (["aa", "bz"], ["bz", "aa"]),
            (["ddd", "cc", "b", "a"], ["b", "a", "cc", "ddd"]),
            (["b", "a"], ["b", "a"]),
            (["A", "a"], ["A", "a"]),
            (["test", "tost"], ["test", "tost"]),
            (["aaaa", "bb"], ["bb", "aaaa"])
        ]
    },
    {
        'nom': '9. Custom Sort',
        'niveau': 4,
        'prototype': 'def custom_sort(words: list[str]) -> list[str]:',
        'sujet': 'Ordonnez la liste des mots fournie selon une logique spécifique :\n'
                 '1. Par longueur de mot croissante.\n'
                 '2. Par ordre alphabétique insensible à la casse.\n'
                 '3. En cas d\'égalité parfaite, le mot débutant par une majuscule est prioritaire.\n'
                 'Type de retour attendu : list[str]',
        'exemples': '1. input = ["b", "A", "a", "B"]\n'
                    '   output = ["A", "a", "B", "b"]\n\n'
                    '2. input = ["Zoo", "abeille"]\n'
                    '   output = ["Zoo", "abeille"]\n\n'
                    '3. input = ["Test", "test"]\n'
                    '   output = ["Test", "test"]',
        'capture_print': False,
        'tests': [
            (["b", "A", "a", "B"], ["A", "a", "B", "b"]),
            (["aa", "Ab", "ac"], ["Ab", "aa", "ac"]),
            (["Zoo", "abeille"], ["Zoo", "abeille"]),
            (["", "a"], ["", "a"]),
            (["c", "C"], ["C", "c"]),
            (["beta", "Alpha"], ["Alpha", "beta"]),
            (["A", "B", "C"], ["A", "B", "C"]),
            (["a", "b", "c"], ["a", "b", "c"]),
            (["Z", "z", "a"], ["a", "Z", "z"]),
            (["Test", "test"], ["Test", "test"])
        ]
    }
]

def main():
    # Organisation des exercices par niveau
    levels = {}
    for ex in EXERCICES:
        lvl = ex.get('niveau', 1)
        if lvl not in levels:
            levels[lvl] = []
        levels[lvl].append(ex)

    print_header()
    print("Bienvenue dans le simulateur d'examen 42.")
    print("Un exercice sera tiré au sort pour chaque niveau (1 à 4).")
    input(f"{YELLOW}Appuie sur Entrée pour commencer...{RESET}")

    # Boucle sur les niveaux 1 à 4
    for niv in range(1, 5):
        if niv not in levels or not levels[niv]:
            continue

        print(f"\n{CYAN}{'='*20} PASSAGE AU NIVEAU {niv} {'='*20}{RESET}")
        
        while True:
            # Choix aléatoire d'un exercice dans le niveau courant
            exo = random.choice(levels[niv])
            
            # Lancement du test
            result = run_tests(exo)
            
            if result == "exit":
                print(f"\n{RED}Arrêt du programme. À bientôt !{RESET}")
                sys.exit()
                
            elif result == "next":
                print(f"\n{YELLOW}>>> Changement d'exercice...{RESET}")
                time.sleep(0.5)
                continue 
                
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

    print(f"\n{GREEN}{'='*50}\nBRAVO ! TU AS FINI L'EXAMEN COMPLET (NIV 1->4) !\n{'='*50}{RESET}")

if __name__ == "__main__":
    main()