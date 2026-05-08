"""
Web Scraping Service - Extract data from websites using BeautifulSoup
"""
from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

class ScraperService:
    def __init__(self):
        """Initialize scraper service"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        print("[ScraperService] Initialized")
    
    def scrape_url(self, url: str, selectors: Optional[List[str]] = None) -> Dict:
        """
        Scrape data from URL
        selectors: CSS selectors to extract specific elements
        """
        try:
            # Fetch page
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            result = {
                "success": True,
                "url": url,
                "title": soup.title.string if soup.title else "",
                "data": {}
            }
            
            # Extract specific selectors
            if selectors:
                for selector in selectors:
                    elements = soup.select(selector)
                    result["data"][selector] = [elem.get_text(strip=True) for elem in elements]
            else:
                # Extract common elements
                result["data"] = {
                    "headings": [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])],
                    "paragraphs": [p.get_text(strip=True) for p in soup.find_all('p')[:10]],
                    "links": [{"text": a.get_text(strip=True), "href": urljoin(url, a.get('href', ''))} 
                             for a in soup.find_all('a', href=True)[:20]]
                }
            
            return result
            
        except requests.RequestException as e:
            return {"success": False, "error": f"Request error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_text(self, url: str) -> Dict:
        """Extract all text content from URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return {
                "success": True,
                "url": url,
                "text": text,
                "word_count": len(text.split())
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_table(self, url: str, table_index: int = 0) -> Dict:
        """Extract table data from URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')
            
            if not tables:
                return {"success": False, "error": "No tables found"}
            
            if table_index >= len(tables):
                return {"success": False, "error": f"Table index {table_index} out of range"}
            
            table = tables[table_index]
            
            # Extract headers
            headers = []
            header_row = table.find('thead')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
            
            # Extract rows
            rows = []
            for tr in table.find_all('tr')[1:]:  # Skip header row
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    rows.append(cells)
            
            return {
                "success": True,
                "headers": headers,
                "rows": rows,
                "row_count": len(rows)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def download_file(self, url: str, save_path: str) -> Dict:
        """Download file from URL"""
        try:
            response = requests.get(url, headers=self.headers, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return {
                "success": True,
                "filepath": save_path,
                "size_bytes": os.path.getsize(save_path)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
