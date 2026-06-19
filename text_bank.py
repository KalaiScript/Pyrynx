"""
Typing Takedown — Text Bank
Python-themed words, commands, code snippets organized by difficulty and mode.
"""

import random

# ─── Classic / Survival Words by Difficulty ───────────────────────────────────

WORDS_EASY = [
    "print", "input", "list", "int", "float", "str", "True", "False",
    "None", "break", "pass", "type", "len", "range", "map", "set",
    "dict", "tuple", "bool", "abs", "max", "min", "sum", "zip",
    "open", "close", "read", "write", "class", "self", "init",
    "not", "and", "or", "if", "else", "for", "in", "while",
    "def", "return", "yield", "from", "import", "as", "with",
    "try", "except", "raise", "del", "is", "lambda", "global",
    "sort", "copy", "pop", "keys", "items", "index", "count",
    "join", "split", "strip", "lower", "upper", "find", "format",
]

WORDS_MEDIUM = [
    "append()", "return x", "import os", "elif x:", "try:", "except:",
    "lambda x:", "print(x)", "input()", "len(arr)", "range(10)",
    "list.sort()", "dict.keys()", "str.split()", "os.path", "sys.argv",
    "random.choice", "math.sqrt", "json.loads", "time.sleep",
    "enumerate()", "isinstance()", "sorted(arr)", "reversed()",
    "map(fn, x)", "filter(fn)", "zip(a, b)", "any(lst)", "all(lst)",
    "set.add(x)", "dict.get(k)", "list.pop(0)", "str.join(x)",
    "f\"{name}\"", "@property", "@staticmethod", "super().__init__",
    "raise ValueError", "assert x > 0", "yield value", "global count",
    "from os import", "import json as", "class Node:", "def main():",
    "while True:", "for item in:", "if __name__:", "not in list",
]

WORDS_HARD = [
    "for i in range(10):", "def calculate_score():", "with open(f) as f:",
    "class Player(object):", "if x is not None:", "while len(q) > 0:",
    "return sorted(arr)[:k]", "except ValueError as e:",
    "from typing import List", "import collections",
    "dict.setdefault(k, [])", "os.path.join(a, b)",
    "list(map(int, input()))", "lambda x: x * 2 + 1",
    "[x for x in range(n)]", "{k: v for k, v in d}",
    "def __init__(self, val):", "super().__init__(args)",
    "raise NotImplementedError", "if isinstance(x, int):",
    "from functools import lru", "threading.Thread(target)",
    "async def fetch(url):", "await response.json()",
    "try:\\n    result = fn()", "with suppress(KeyError):",
    "sys.stdin.readline()", "heapq.heappush(h, x)",
    "collections.Counter(s)", "itertools.chain(*lists)",
]

WORDS_BOSS = [
    "if user_input.isdigit():",
    "for key, value in data.items():",
    "from collections import Counter",
    "def binary_search(arr, target):",
    "while left <= right:",
    "class LinkedList:",
    "    def __init__(self):",
    "        self.head = None",
    "return max(dp[n-1], dp[n-2])",
    "sorted(arr, key=lambda x: x[1])",
    "with open('data.json', 'r') as f:",
    "    data = json.load(f)",
    "if __name__ == '__main__':",
    "    main()",
    "from typing import Optional, List",
    "def merge_sort(arr: List[int]):",
    "result = {k: v for k, v in items}",
    "except (ValueError, KeyError) as e:",
    "logging.getLogger(__name__)",
    "os.environ.get('API_KEY', '')",
]

# ─── Command Line Mode ───────────────────────────────────────────────────────

WORDS_COMMANDS = [
    "python main.py", "pip install pygame", "git commit -m 'fix'",
    "cd project", "ls -la", "mkdir src", "rm -rf build",
    "git status", "git push origin main", "git pull --rebase",
    "pip freeze > req.txt", "python -m venv env", "source env/bin/activate",
    "chmod +x script.sh", "cat README.md", "grep -r 'def '",
    "docker build -t app .", "docker run -p 8080:80", "curl localhost:8080",
    "npm install", "node server.js", "ssh user@server",
    "scp file.py remote:/", "tar -xzf archive.tar.gz", "wget url.com/file",
    "echo $PATH", "export API_KEY=abc", "ps aux | grep python",
    "kill -9 1234", "htop", "df -h", "du -sh *",
    "git log --oneline -5", "git diff HEAD~1", "git checkout -b feat",
    "python -c 'print(1)'", "pip show requests", "pytest -v tests/",
    "black main.py", "flake8 src/", "mypy --strict app.py",
]

# ─── Debug Mode (broken → fixed pairs) ───────────────────────────────────────

WORDS_DEBUG = [
    # (broken_display, correct_answer)
    ("pritn('hello')", "print('hello')"),
    ("for i in rnage(5):", "for i in range(5):"),
    ("def add(a b):", "def add(a, b):"),
    ("improt random", "import random"),
    ("retrun x + y", "return x + y"),
    ("whlie True:", "while True:"),
    ("lst.apend(x)", "lst.append(x)"),
    ("if x = 5:", "if x == 5:"),
    ("form os import path", "from os import path"),
    ("class Dog(obejct):", "class Dog(object):"),
    ("excpet ValueError:", "except ValueError:"),
    ("x = int(imput())", "x = int(input())"),
    ("dct.get(ky, None)", "dct.get(key, None)"),
    ("os.path.jion(a, b)", "os.path.join(a, b)"),
    ("rsult = sorted(lst)", "result = sorted(lst)"),
    ("lmbda x: x ** 2", "lambda x: x ** 2"),
    ("yeild value", "yield value"),
    ("asert x > 0", "assert x > 0"),
    ("rais Exception()", "raise Exception()"),
    ("gobal counter", "global counter"),
]

# ─── Interview Mode ──────────────────────────────────────────────────────────

WORDS_INTERVIEW = [
    "binary search", "linked list", "hash map", "stack", "queue",
    "O(n log n)", "depth first", "breadth first", "dynamic programming",
    "greedy algorithm", "merge sort", "quick sort", "heap sort",
    "binary tree", "graph traversal", "backtracking", "memoization",
    "two pointers", "sliding window", "divide and conquer",
    "recursion", "iteration", "time complexity", "space complexity",
    "Big O notation", "amortized O(1)", "hash collision", "load factor",
    "AVL tree", "red black tree", "trie", "segment tree",
    "topological sort", "shortest path", "minimum spanning", "union find",
    "bit manipulation", "prefix sum", "monotonic stack", "deque",
    "in-order traversal", "level-order scan", "Dijkstra algorithm",
    "Floyd Warshall", "Bellman Ford", "Kruskal MST", "Prim MST",
]

# ─── Selection Functions ──────────────────────────────────────────────────────

def get_classic_word(complexity: str) -> str:
    """Get a random word for Classic/Survival mode based on complexity."""
    if complexity == "easy":
        pool = WORDS_EASY
    elif complexity == "medium":
        pool = WORDS_EASY + WORDS_MEDIUM
    else:  # hard
        pool = WORDS_EASY + WORDS_MEDIUM + WORDS_HARD
    return random.choice(pool)


def get_boss_word() -> str:
    """Get a random boss-tier word."""
    return random.choice(WORDS_BOSS)


def get_command_word(complexity: str) -> str:
    """Get a random terminal command."""
    if complexity == "easy":
        # shorter commands only
        short = [w for w in WORDS_COMMANDS if len(w) <= 14]
        return random.choice(short) if short else random.choice(WORDS_COMMANDS)
    return random.choice(WORDS_COMMANDS)


def get_debug_pair() -> tuple:
    """Get a (broken, correct) pair for Debug Mode."""
    return random.choice(WORDS_DEBUG)


def get_interview_word(complexity: str) -> str:
    """Get a random interview/DSA term."""
    if complexity == "easy":
        short = [w for w in WORDS_INTERVIEW if len(w) <= 12]
        return random.choice(short) if short else random.choice(WORDS_INTERVIEW)
    return random.choice(WORDS_INTERVIEW)


def get_word_for_mode(mode: str, complexity: str, is_boss: bool = False) -> str | tuple:
    """
    Get a word/snippet appropriate for the current mode and difficulty.
    For Debug mode, returns (broken, correct) tuple.
    For all others, returns a string.
    """
    from settings import (
        MODE_CLASSIC, MODE_TIME_ATTACK, MODE_BOSS_RUSH,
        MODE_DEBUG, MODE_COMMAND_LINE, MODE_INTERVIEW,
    )

    if is_boss:
        return get_boss_word()

    if mode in (MODE_CLASSIC, MODE_TIME_ATTACK):
        return get_classic_word(complexity)
    elif mode == MODE_BOSS_RUSH:
        return get_boss_word()
    elif mode == MODE_DEBUG:
        return get_debug_pair()
    elif mode == MODE_COMMAND_LINE:
        return get_command_word(complexity)
    elif mode == MODE_INTERVIEW:
        return get_interview_word(complexity)
    else:
        return get_classic_word(complexity)
