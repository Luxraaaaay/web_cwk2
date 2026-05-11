from src.crawler import Crawler


class FakeResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code


def test_default_delay():
    c = Crawler()
    assert c.delay == 6


def test_crawl_skips_login_and_deduplicates(monkeypatch):
    crawler = Crawler(delay=0)
    start_url = "https://quotes.toscrape.com/"

    pages = {
        start_url: (
            '<html><body>'
            '<a href="/page/2/">next</a>'
            '<a href="/page/2/">dup</a>'
            '<a href="/login">login</a>'
            '</body></html>'
        ),
        "https://quotes.toscrape.com/page/2/": "<html><body>page 2</body></html>",
    }

    calls = []

    def fake_get(url, timeout=10):
        calls.append(url)
        return FakeResponse(pages[url])

    monkeypatch.setattr(crawler.session, "get", fake_get)
    monkeypatch.setattr("src.crawler.time.sleep", lambda _: None)

    result = crawler.crawl(start_url)

    assert calls == [start_url, "https://quotes.toscrape.com/page/2/"]
    assert "https://quotes.toscrape.com/login" not in result
    assert set(result) == set(pages)


def test_crawl_continues_after_request_exception_and_non_200(monkeypatch):
    crawler = Crawler(delay=0)
    start_url = "https://quotes.toscrape.com/"

    pages = {
        start_url: FakeResponse(
            (
            '<html><body>'
            '<a href="/boom/">boom</a>'
            '<a href="/error/">error</a>'
            '<a href="/ok/">ok</a>'
            '</body></html>'
            )
        ),
        "https://quotes.toscrape.com/boom/": RuntimeError("network down"),
        "https://quotes.toscrape.com/error/": FakeResponse("<html>error</html>", status_code=500),
        "https://quotes.toscrape.com/ok/": FakeResponse("<html>ok</html>", status_code=200),
    }

    calls = []

    def fake_get(url, timeout=10):
        calls.append(url)
        value = pages[url]
        if isinstance(value, Exception):
            raise value
        return value

    monkeypatch.setattr(crawler.session, "get", fake_get)
    monkeypatch.setattr("src.crawler.time.sleep", lambda _: None)

    result = crawler.crawl(start_url)

    assert calls == [
        start_url,
        "https://quotes.toscrape.com/boom/",
        "https://quotes.toscrape.com/error/",
        "https://quotes.toscrape.com/ok/",
    ]
    assert start_url in result
    assert "https://quotes.toscrape.com/boom/" not in result
    assert "https://quotes.toscrape.com/error/" not in result
    assert "https://quotes.toscrape.com/ok/" in result

