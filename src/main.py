import os
import shlex
from src.crawler import Crawler
from src.indexer import build_index, save_index, load_index
from src.search import print_postings, find

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
INDEX_PATH = os.path.abspath(os.path.join(DATA_DIR, "index.json"))


def cmd_build():
    url = "https://quotes.toscrape.com/"
    print(f"Crawling {url} ... (this may take a while, respecting 6s delay)")
    crawler = Crawler(delay=6)
    pages = crawler.crawl(url)
    print(f"Fetched {len(pages)} pages, building index...")
    index = build_index(pages)
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    save_index(index, INDEX_PATH)
    print(f"Index saved to {INDEX_PATH}")
    return index


def cmd_load():
    path = INDEX_PATH
    index = load_index(path)
    print(f"Loaded index with {len(index)} terms from {path}")
    return index


def cmd_print(word, index):
    if index is None:
        index = load_index(INDEX_PATH)
    print_postings(word, index)


def cmd_find(query, index):
    if index is None:
        index = load_index(INDEX_PATH)
    results = find(query, index)
    if not results:
        print("No results")
        return
    for score, url in results:
        print(f"{score}\t{url}")


def print_shell_help():
    print("Commands:")
    print("  build             Crawl website and rebuild index")
    print("  load              Load index from file (default data/index.json)")
    print("  print <word>      Print postings list for a word")
    print("  find <query>      Search pages containing all query words")
    print("  help              Show this help")
    print("  exit | quit       Exit interactive shell")


def main():
    print("Search Engine Tool (interactive shell)")
    print("Type 'help' to see commands.")
    index = None

    while True:
        try:
            line = input("search> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not line:
            continue

        try:
            parts = shlex.split(line)
        except ValueError as e:
            print(f"Invalid command format: {e}")
            continue

        command = parts[0].lower()
        args = parts[1:]

        try:
            if command in {"exit", "quit"}:
                print("Bye.")
                break
            if command == "help":
                print_shell_help()
                continue
            if command == "build":
                if args:
                    print("Usage: build")
                    continue
                index = cmd_build()
                continue
            if command == "load":
                if args:
                    print("Usage: load")
                    continue
                index = cmd_load()
                continue
            if command == "print":
                if len(args) != 1:
                    print("Usage: print <word>")
                    continue
                cmd_print(args[0], index)
                continue
            if command == "find":
                if not args:
                    print("Usage: find <query>")
                    continue
                cmd_find(" ".join(args), index)
                continue

            print("Unknown command. Type 'help' to see available commands.")
        except FileNotFoundError:
            print(f"Index file not found: {INDEX_PATH}. Run 'build' or 'load <path>' first.")
        except Exception as e:
            print(f"Command failed: {e}")


if __name__ == "__main__":
    main()
