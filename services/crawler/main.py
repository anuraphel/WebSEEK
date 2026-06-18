import asyncio
import os
from dotenv import load_dotenv
from crawler import Crawler

load_dotenv()

async def main():
    # Example start URLs
    start_urls = [
        "https://quotes.toscrape.com/",
        "https://example.com"
    ]
    
    crawler = Crawler(start_urls=start_urls)
    
    print("Starting Crawler Service...")
    await crawler.run(max_concurrent=10)

if __name__ == "__main__":
    asyncio.run(main())
