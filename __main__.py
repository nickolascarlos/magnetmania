from TorrentDosFilmesScraper import *
from page import Page
from utils import *
from database import *

def main():
    for i in range(1, 200):
        print(f'\n\n\nPágina {i-1}/{228} ({(i-1)/228*100}%)\n')
        try:
            page = Page("https://torrentdosfilmes.site/filmes/page/" + str(i), TorrentDosFilmesScraper)
        except:
            print(f"OOPS! Something caused page {i} to be jumped! See it later...")
            continue
        
        for url in page.get_urls():
            save_magnets_from_url(url)

def register_media_and_metadata(content_info, content_metadata):
    params = [content_info['name'], int(content_info['year'] or '-1') if not is_series(content_info) else -1]
    if register_media(*params):
        # Register some metadata
        media_id = get_media_id(*params)
        for metadata in content_metadata:
            if 'xt' in metadata[0]: continue
            if len(metadata) >= 2:
                set_media_metadata(media_id, metadata[0], metadata[1])
        return media_id
    else:
        print('Não foi possível cadastrar essa mídia')
        return None

def register_magnet_and_metadata(magnet, media_id):
    magnet_hash = magnet.get_hash()

    # Function register_magnet returns False if magnet is already
    # registered, preventing, thus, multiple metadata records :)
    if magnet_hash and register_magnet(magnet_hash, media_id):
        magnet_metadata = magnet.get_properties()
        for metadata in magnet_metadata:
            set_magnet_metadata(magnet_hash, metadata[0], metadata[1])

        try:
            season, episode = get_season_episode_from_filename(magnet.get_filename())
            if season or episode:
                set_magnet_metadata(magnet_hash, 'season', season)
                set_magnet_metadata(magnet_hash, 'episode', episode)
        except:
            pass

        return magnet_hash
    else:
        print('Não foi possível cadastrar esse magnet')
        return None
    
def save_magnets_from_url(url):
    try:
        url_page = Page(url, TorrentDosFilmesScraper)
    except:
        print(f"OOPS! Something caused {url} to be jumped! See it later...")
        return False
    
    if not url_page.is_content_relevant():
        return True

    print(url_page.get_page_content_title() or '')
    
    content_info = extract_info(url_page.get_page_content_title())
    content_metadata = url_page.get_page_content_metadata()
    media_id = register_media_and_metadata(content_info, content_metadata)
    
    if media_id:
        page_magnets = url_page.get_magnets()
        for magnet in page_magnets:
            register_magnet_and_metadata(magnet, media_id)

    return True
            

if __name__ == '__main__':
    main()
