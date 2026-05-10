import re
import json
from collections import defaultdict
from bs4 import BeautifulSoup


WORD_RE = re.compile(r"\b\w+\b")


def tokenize(text: str):
    return WORD_RE.findall(text.lower())


def build_index(pages: dict):
    """pages: dict[url] = html_text
    返回倒排索引：{word: {url: count, ...}, ...}
    """
    index = defaultdict(lambda: defaultdict(int))
    for url, html in pages.items():
        text = BeautifulSoup(html, "html.parser").get_text(" ")
        for w in tokenize(text):
            index[w][url] += 1
    # 转为普通 dict
    return {w: dict(d) for w, d in index.items()}


def save_index(index: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def load_index(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
