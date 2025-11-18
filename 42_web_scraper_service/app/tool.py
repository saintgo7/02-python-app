import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from typing import List, Dict, Any


class WebScraper:
    """Web scraper utility"""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def fetch_page(self, url: str) -> str:
        """Fetch HTML content from URL"""
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(html, 'html.parser')

    def extract_data(self, url: str, selectors: Dict[str, str]) -> Dict[str, Any]:
        """Extract data using CSS selectors"""
        html = self.fetch_page(url)
        soup = self.parse_html(html)

        data = {'timestamp': datetime.now().isoformat()}
        for key, selector in selectors.items():
            elements = soup.select(selector)
            data[key] = [el.get_text() for el in elements]

        return data

    def scrape_table(self, url: str, table_index: int = 0) -> List[Dict[str, str]]:
        """Scrape table from URL"""
        html = self.fetch_page(url)
        soup = self.parse_html(html)

        table = soup.find_all('table')[table_index]
        headers = [th.get_text() for th in table.find_all('th')]

        rows = []
        for tr in table.find_all('tr')[1:]:
            cells = [td.get_text() for td in tr.find_all('td')]
            if len(cells) == len(headers):
                rows.append(dict(zip(headers, cells)))

        return rows
