import requests

class Page:
    def __init__(self, url, scraper):
        self.url = url
        self.scraper = scraper
        self.content = requests.get(url).text

    def get_urls(self):
        return self.scraper.get_urls(self.content)
    
    def get_magnets(self):
        return self.scraper.get_magnets(self.content)
    
    def get_page_content_title(self):
        return self.scraper.get_page_content_title(self.content)
    
    def get_page_content_metadata(self):
        return self.scraper.get_page_content_metadata(self.content)
    
    def is_content_relevant(self):
        return self.scraper.is_content_relevant(self.content)