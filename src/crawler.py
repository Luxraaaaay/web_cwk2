import time
import urllib.parse
import requests
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self, delay: int = 6):
        self.delay = delay
        self.session = requests.Session()

    def crawl(self, start_url: str):
        domain = urllib.parse.urlparse(start_url).netloc
        to_visit = [start_url]
        visited = set()
        discovered = set(to_visit)
        pages = {}

        while to_visit:
            url = to_visit.pop(0)
            if url in visited:
                continue
            parsed = urllib.parse.urlparse(url)
            if parsed.path.startswith("/login"):
                continue
            try:
                print(f"Fetching {url}")
                resp = self.session.get(url, timeout=10)
                time.sleep(self.delay)
                if resp.status_code != 200:
                    continue
                visited.add(url)
                pages[url] = resp.text
                soup = BeautifulSoup(resp.text, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = urllib.parse.urljoin(url, a["href"])
                    href_parsed = urllib.parse.urlparse(href)
                    if href_parsed.path.startswith("/login"):
                        continue
                    if href_parsed.netloc == domain and href not in visited and href not in discovered:
                        to_visit.append(href)
                        discovered.add(href)
            except Exception:
                continue
        return pages
