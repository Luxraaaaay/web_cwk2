import argparse
import os
from src.crawler import Crawler
from src.indexer import build_index, save_index, load_index
from src.search import print_postings, find

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
INDEX_PATH = os.path.abspath(os.path.join(DATA_DIR, "index.json"))


def cmd_build(args):
    url = args.url or "https://quotes.toscrape.com/"
    print(f"Crawling {url} ... (this may take a while, respecting 6s delay)")
    crawler = Crawler(delay=6)
    pages = crawler.crawl(url)
    print(f"Fetched {len(pages)} pages, building index...")
    index = build_index(pages)
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    save_index(index, INDEX_PATH)
    print(f"Index saved to {INDEX_PATH}")


def cmd_load(args):
    path = args.path or INDEX_PATH
    index = load_index(path)
    print(f"Loaded index with {len(index)} terms from {path}")
    # store in args for subsequent commands
    return index


def cmd_print(args, index):
    if index is None:
        index = load_index(INDEX_PATH)
    print_postings(args.word, index)


def cmd_find(args, index):
    if index is None:
        index = load_index(INDEX_PATH)
    results = find(args.query, index)
    if not results:
        print("No results")
        return
    for score, url in results:
        print(f"{score}\t{url}")


def main():
    parser = argparse.ArgumentParser(description="Simple Web Crawler, Indexer and Searcher")
    sub = parser.add_subparsers(dest="cmd")

    p_build = sub.add_parser("build")
    p_build.add_argument("--url", help="URL to start crawling from (default quotes.toscrape.com)")

    p_load = sub.add_parser("load")
    p_load.add_argument("--path", help="Path to index file")

    p_print = sub.add_parser("print")
    p_print.add_argument("word", help="Word to print postings for")

    p_find = sub.add_parser("find")
    p_find.add_argument("query", help="Query to search for (supports multiple words)")

    args = parser.parse_args()
    index = None
    if args.cmd == "build":
        cmd_build(args)
    elif args.cmd == "load":
        cmd_load(args)
    elif args.cmd == "print":
        cmd_print(args, index)
    elif args.cmd == "find":
        cmd_find(args, index)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
