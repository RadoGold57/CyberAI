import asyncio
import httpx
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

async def fetch(client, url):
    try:
        r = await client.get(url, timeout=10)
        return url, r.text
    except:
        return url, None

async def async_crawl(base_url, max_pages=100, concurrency=30):
    seen = set()
    queue = asyncio.Queue()
    results = []

    if not base_url.startswith("http"):
        base_url = "https://" + base_url
    await queue.put(base_url)
    seen.add(base_url)
    parsed_base = urlparse(base_url).netloc

    async with httpx.AsyncClient(follow_redirects=True) as client:
        while not queue.empty() and len(seen) < max_pages:
            tasks = []
            for _ in range(min(concurrency, queue.qsize())):
                url = await queue.get()
                tasks.append(fetch(client, url))
            for url, text in await asyncio.gather(*tasks):
                if text:
                    results.append(url)
                    soup = BeautifulSoup(text, "lxml")
                    for tag in soup.find_all(["a", "script", "link"], href=True) + soup.find_all("a", src=True):
                        link = tag.get("href") or tag.get("src")
                        full = urljoin(url, link)
                        if urlparse(full).netloc == parsed_base and full not in seen:
                            seen.add(full)
                            await queue.put(full)
    return results
