import re
import requests
from urllib.parse import unquote

MAGNET_REGEX = "magnet:\??(?:(?:(?:[a-z]{2,5}=[^&\"]*))&?(?:\#038;)?)*"
MAGNET_PROPERTY_REGEX = "(?:([a-z]{2,5})=([^&\"]*))"

class Magnet:
    def __init__(self, link):
        self.link = link
        self.parse()

    @staticmethod
    def get_from_content(content):
        found_magnets = re.findall(MAGNET_REGEX, content)
        return [Magnet(magnet) for magnet in found_magnets]
    
    @staticmethod
    async def get_from_url(url):
        return Magnet.get_from_content(requests.get(url).text)
    
    def parse(self):
        properties = re.findall(MAGNET_PROPERTY_REGEX, self.link)
        self.properties = [(prop[0], unquote(prop[1])) for prop in properties]
    
    def get_property(self, property_name):
        return [prop[1] for prop in self.properties if prop[0] == property_name]
    
    def get_properties(self):
        return self.properties
    
    def as_str(self):
        try:
            return 'magnet:?xt=' + self.get_hash()
        except:
            return self.link
    
    def get_filename(self):
        # [-1] => latter ovewrites former
        try:
            return self.get_property('dn')[-1]
        except:
            return None
    
    def get_trackers(self):
        try:
            return self.get_property('tr')
        except:
            return None
    
    def get_hash(self):
        # [-1] => latter ovewrites former
        try:
            return self.get_property('xt')[-1]
        except:
            return None