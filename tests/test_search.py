from src.search import find
from src.search import print_postings


def test_find_basic():
    index = {
        "hello": {"u1": 1, "u2": 2},
        "world": {"u2": 1},
    }
    res = find("hello world", index)
    # only u2 contains both
    assert len(res) == 1
    assert res[0][1] == "u2"


def test_find_sorts_by_score_descending():
    index = {
        "good": {"u1": 1, "u2": 3},
        "friends": {"u1": 4, "u2": 1},
    }

    res = find("good friends", index)

    assert res == [(5, "u1"), (4, "u2")]


def test_find_no_results_returns_empty():
    index = {"hello": {"u1": 1}}
    assert find("nonexistentword", index) == []


def test_duplicate_word_query_counts_multiple_times():
    index = {"good": {"u1": 2}, "friends": {"u1": 3}}
    # query contains 'good' twice -> score should add good twice
    res = find("good good friends", index)
    assert res == [(7, "u1")]  # 2 + 2 + 3 = 7


def test_find_empty_query_returns_empty_list():
    assert find("   ", {"hello": {"u1": 1}}) == []


def test_print_postings_outputs_count_and_missing_message(capsys):
    index = {"hello": {"u1": 1, "u2": 3}}

    print_postings("Hello", index)
    output = capsys.readouterr().out.splitlines()

    assert output == ["u1 : 1", "u2 : 3"]

    print_postings("missing", index)
    output = capsys.readouterr().out.strip()
    assert output == "'missing' not found in index"

