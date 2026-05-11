Project: COMP/XJCO3011 - Coursework 2: Search Engine Tool

Project Overview and Purpose
- This project implements a mini search engine for https://quotes.toscrape.com/.
- It crawls pages from the target website, builds an inverted index, and supports keyword search from a command-line interface.
- The purpose is to demonstrate core information retrieval workflow: crawl -> index -> query.

Installation / Setup

Get the project code from GitHub:

```bash
git clone https://github.com/Luxraaaaay/web_cwk2.git
cd web_cwk2
```

Using a virtual environment (venv or conda) is recommended.

Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies

The project dependencies are managed in `requirements.txt` and include:
- `requests` for HTTP crawling
- `beautifulsoup4` for HTML parsing
- `pytest` for automated tests
- `pytest-benchmark` for performance-style testing support

Usage Examples

Start the interactive shell:

```bash
python -m src.main
```

Then run these commands in the shell. Each command below shows the expected effect after execution.

- Build the index (crawl and save to `data/index.json`):

	- Crawls the target website, builds the inverted index, saves it to `data/index.json`, and prints how many pages were fetched.

```bash
build
```

- Load the index (prints load information only):

	- Loads `data/index.json` from disk and prints how many terms were loaded.

```bash
load
```

- Print postings for a specific word:

	- Shows all pages containing the word together with the occurrence count on each page.

```bash
print love
```

- Find pages containing the query terms (multi-word AND query):

	- Returns pages that contain all query words and prints them with a score based on term frequency.

```bash
find "life love"
```

Helpful commands:

```bash
help
exit
```

Testing

This project includes three kinds of automated tests:
- Unit tests for the crawler, indexer, search logic, and CLI command handling.
- An end-to-end integration test that covers crawl -> build index -> query using mocked HTTP responses.
- Simple performance-oriented tests that measure indexing and query latency on synthetic data.

Run the full test suite:

```bash
pytest -q
```

Run only the end-to-end integration test:

```bash
pytest -q tests/test_e2e.py
```

Run only the performance-oriented tests:

```bash
pytest -q tests/test_performance.py
```

The tests use mocking to avoid real network calls and to keep execution fast and reproducible.
