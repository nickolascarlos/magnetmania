import re
from bs4 import BeautifulSoup
import requests
from magnet import Magnet

class TorrentDosFilmesScraper:
    __BASE_URL = 'torrentdosfilmes.site'
    
    @staticmethod
    def get_urls(content):
        soup = BeautifulSoup(content, 'html.parser')
        a_elements = soup.find('main').find_all('a')
        return [*set([element.get('href') for element in a_elements])]
    
    @staticmethod
    def is_content_relevant(content):
        # Checks if content is a media page.
        # As observed, media pages in this specific website
        # cotains an element in i-classif class, thus it
        # can be used to identify this kind of page.

        # Adapt this function to other websites!
        soup = BeautifulSoup(content, 'html.parser')
        return len(soup.select('.i-classif')) > 0
    
    @classmethod
    def get_magnets(self, content, verbose = False):
        if not self.is_content_relevant(content) and verbose:
            print(f'Ignoring :: No relevant content!')
            return []
        
        return Magnet.get_from_content(content)
    
    @classmethod
    def get_page_content_title(self, content):
        if not self.is_content_relevant(content):
            return None
        
        soup = BeautifulSoup(content, 'html.parser')
        return soup.select_one('article .title h1').text
    
    @classmethod
    def get_page_content_metadata(self, content):
        if not self.is_content_relevant(content):
            return []
        
        soup = BeautifulSoup(content, 'html.parser')
        metadata_container = soup.select_one('div.content').find_all('p')[2]
        metadata_elements = metadata_container.select('span')[1:]
        metadata = []
        for element in metadata_elements:
            if element.text != None and 'imdb' not in element.text.lower():
                metadata.append([x.strip() for x in element.text.split(':')])
        
        # Extracts IMDb id
        imdb_regex = r"(?i)imdb\.com/title/(\w+)"
        match = re.search(imdb_regex, content)
        if match:
            metadata.append(['imdb', match.group(1)])
        
        return metadata

        

