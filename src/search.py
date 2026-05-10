import re
from typing import Dict, List, Tuple


WORD_RE = re.compile(r"\w+")


def print_postings(word: str, index: Dict[str, Dict[str, int]]):
    w = word.lower()
    postings = index.get(w)
    if not postings:
        print(f"'{word}' not found in index")
        return
    for url, count in postings.items():
        print(f"{url} : {count}")


def find(query: str, index: Dict[str, Dict[str, int]], top_n: int = 10) -> List[Tuple[int, str]]:
    words = [w.lower() for w in WORD_RE.findall(query)]
    if not words:
        return []
    sets = [set(index.get(w, {}).keys()) for w in words]
    if not sets:
        return []
    common = set.intersection(*sets) if len(sets) > 1 else sets[0]
    results = []
    for url in common:
        score = sum(index[w][url] for w in words)
        results.append((score, url))
    results.sort(reverse=True)
    return results[:top_n]
