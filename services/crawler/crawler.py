import aiohttp
import asyncio
from queue import URLQueue
from db import DBManager
from extractor import Extractor

class Crawler:
    def __init__(self, start_urls=None):
        self.queue = URLQueue()
        self.db = DBManager()
        self.extractor = Extractor()
        
        if start_urls:
            for url in start_urls:
                self.queue.push(url)

    async def fetch(self, session, url):
        """Fetch a URL and return its content."""
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    async def crawl_page(self, session, url):
        """Crawl a single page: fetch, extract, save, and queue links."""
        if self.queue.is_visited(url):
            return

        print(f"Crawling: {url}")
        html = await self.fetch(session, url)
        self.queue.mark_visited(url)

        if html:
            title, content = self.extractor.extract_content(html)
            self.db.save_page(url, title, content, html)
            
            links = self.extractor.extract_links(html, url)
            for link in links:
                self.queue.push(link)

    async def run(self, max_concurrent=5):
        """Run the crawler with a concurrency limit."""
        async with aiohttp.ClientSession() as session:
            while True:
                url = self.queue.pop()
                if not url:
                    print("Queue empty, waiting...")
                    await asyncio.sleep(5)
                    continue

                await self.crawl_page(session, url)
                # Simple delay to be nice to servers
                await asyncio.sleep(1)
