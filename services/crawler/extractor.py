from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class Extractor:
    @staticmethod
    def extract_links(html, base_url):
        """Extract all absolute links from the HTML."""
        soup = BeautifulSoup(html, 'lxml')
        links = set()
        for a in soup.find_all('a', href=True):
            link = urljoin(base_url, a['href'])
            # Only include http/https links and stay within the same domain (optional)
            if link.startswith('http'):
                links.add(link)
        return links

    @staticmethod
    def extract_content(html):
        """Extract title and cleaned text content from HTML."""
        soup = BeautifulSoup(html, 'lxml')
        
        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        title = soup.title.string if soup.title else ""
        
        # Get text, collapse whitespace
        text = soup.get_text(separator=' ')
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)

        return title, clean_text
