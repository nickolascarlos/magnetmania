import re

def get_season_episode_from_filename(filename):
    # Written by ChatGPT :)
    patterns = [
        r"S(\d{2})E(\d{2})",  # pattern for "SxxExx"
        r"\.(\d{1,2})x(\d{1,2})\.",  # pattern for ".xxExx."
        r"(\d{1,2})(\d{2})",  # pattern for "xxExx"
        r"(\d{1,2})\.(\d{2})",  # pattern for "xx.Exx"
    ]
    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            season = int(match.group(1))
            episode = int(match.group(2))
            return season, episode
    return None

def extract_info(title):
    title = str(title)
    
    # Regular expressions for extracting movie info
    title_regex = r'(.+?) Torrent'  # movie/TV series name before 'Torrent'
    year_regex = r'\((\d{4})\)'  # year in parentheses
    format_regex = r'(BluRay|WEB-DL|BRRip|WEBRip|HDRip|CAMRip)'  # format
    quality_regex = r'(\d+p)'  # quality
    audio_regex = r'(Dual Áudio|Legendado|Nacional)'  # audio type
    season_regex = r'(\d+)ª Temporada'  # season number
    
    # Extract movie/TV series name
    match = re.search(title_regex, title)
    if match:
        name = re.sub(r'(\d+)ª Temporada', '', match.group(1)).strip()
    else:
        name = None
    
    # Extract year
    match = re.search(year_regex, title)
    if match:
        year = match.group(1)
    else:
        year = None
    
    # Extract format
    match = re.search(format_regex, title)
    if match:
        format = match.group(1)
    else:
        format = None
    
    # Extract quality
    match = re.search(quality_regex, title)
    if match:
        quality = match.group(1)
    else:
        quality = None
    
    # Extract audio type
    match = re.search(audio_regex, title)
    if match:
        audio = match.group(1)
    else:
        audio = None
    
    # Extract season number
    match = re.search(season_regex, title)
    if match:
        season = match.group(1)
    else:
        season = None
    
    # Return info
    return {
            "name": name,
            "year": year,
            "format": format,
            "quality": quality,
            "audio": audio,
            "season": season
        }

def is_series(info):
    return info['season'] is not None