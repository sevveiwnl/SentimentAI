import os
import requests
from bs4 import BeautifulSoup
import re

#get api token from environment variable
GENIUS_API_TOKEN = os.getenv('GENIUS_ACCESS_TOKEN')
BASE_URL = 'https://api.genius.com'

def search_song(title, artist):

    #set API endpoint URL and searc parameters 
    search_url = f"{BASE_URL}/search"
    headers = {'Authorization': f'Bearer {GENIUS_API_TOKEN}'}
    params = {'q': f'{title} {artist}'}
    
    #request to genius api to search for the song
    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()

    #parse the response and return first results if match is found
    if 'response' in data and data['response']['hits']:
        return data['response']['hits'][0]['result']
    return None


def get_lyrics(url):
    #request song page and then use soup to parse html
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all divs that are containers for lyrics
    lyrics_containers = soup.find_all('div', attrs={"data-lyrics-container": "true"})
    if not lyrics_containers:
        return None

    lyrics = ''
    for container in lyrics_containers:
        # Extract text, handling any <br> tags as newlines
        for element in container.descendants:
            if isinstance(element, str):
                lyrics += element
            elif element.name == 'br':
                lyrics += '\n'
        lyrics += '\n'  # Add extra newline between containers if needed

    return lyrics.strip()
