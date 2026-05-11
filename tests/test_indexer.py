from src.indexer import build_index, save_index, load_index


def test_build_index_basic():
    pages = {
        "http://a/": "Hello world!",
        "http://b/": "Hello there, world world",
    }
    index = build_index(pages)
    assert "hello" in index
    assert index["hello"]["http://a/"] == 1
    assert index["world"]["http://b/"] == 2


def test_save_and_load_index_roundtrip(tmp_path):
    index = {
        "hello": {"http://a/": 1},
        "world": {"http://a/": 2, "http://b/": 1},
    }
    path = tmp_path / "index.json"

    save_index(index, path)
    loaded = load_index(path)

    assert loaded == index

