from src.crawler import Crawler
from src.indexer import build_index
from src.search import find


class FakeResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code


def test_end_to_end_crawl_index_query(monkeypatch):
    crawler = Crawler(delay=0)
    start_url = "https://quotes.toscrape.com/"

    pages = {
        start_url: (
            '<html><body>'
            '<a href="/page/2/">next</a>'
            '<div class="quote">Life is beautiful</div>'
            '</body></html>'
        ),
        "https://quotes.toscrape.com/page/2/": (
            '<html><body>'
            '<div class="quote">Beautiful things are happening</div>'
            '</body></html>'
        ),
    }

    def fake_get(url, timeout=10):
        return FakeResponse(pages[url])

    monkeypatch.setattr(crawler.session, "get", fake_get)
    monkeypatch.setattr("src.crawler.time.sleep", lambda _: None)

    crawled = crawler.crawl(start_url)

    idx = build_index(crawled)

    # query for a word present across pages
    res = find("beautiful", idx)
    # both pages contain the token 'beautiful' -> two results
    urls = {r[1] for r in res}
    assert "https://quotes.toscrape.com/" in urls
    assert "https://quotes.toscrape.com/page/2/" in urls
