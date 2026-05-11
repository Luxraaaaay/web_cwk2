import time

from src.indexer import build_index


def test_build_index_performance():
    # generate a moderate-size synthetic corpus
    pages = {f"http://a/{i}": "word " * 100 for i in range(200)}

    t0 = time.perf_counter()
    idx = build_index(pages)
    dt = time.perf_counter() - t0

    # sanity check: token appeared and timing is reasonable
    assert "word" in idx
    assert dt < 2.0


def test_find_query_performance():
    pages = {f"http://a/{i}": ("alpha beta gamma " * 30) for i in range(200)}
    idx = build_index(pages)

    t0 = time.perf_counter()
    res = idx.get("alpha", {})
    _ = sorted(((cnt, url) for url, cnt in res.items()), reverse=True)
    dt = time.perf_counter() - t0

    assert dt < 0.5
