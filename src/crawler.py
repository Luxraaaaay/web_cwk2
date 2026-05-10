import time
import urllib.parse
import requests
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self, delay: int = 6):
        self.delay = delay
        self.session = requests.Session()

    def crawl(self, start_url: str, max_pages: int = 200):
        domain = urllib.parse.urlparse(start_url).netloc
        to_visit = [start_url]
        visited = set()
        pages = {}

        while to_visit and len(visited) < max_pages:
            url = to_visit.pop(0)
            if url in visited:
                continue
            try:
                resp = self.session.get(url, timeout=10)
                time.sleep(self.delay)
                if resp.status_code != 200:
                    continue
                visited.add(url)
                pages[url] = resp.text
                soup = BeautifulSoup(resp.text, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = urllib.parse.urljoin(url, a["href"])
                    if urllib.parse.urlparse(href).netloc == domain and href not in visited:
                        to_visit.append(href)
            except Exception:
                continue
        return pages
