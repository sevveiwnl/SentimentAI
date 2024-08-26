import os
import requests
from bs4 import BeautifulSoup

GENIUS_API_TOKEN = os.getenv('GENIUS_ACCESS_TOKEN')
BASE_URL = 'https://api.genius.com'

def search_song(title, artist):
    search_url = f"{BASE_URL}/search"
    headers = {'Authorization': f'Bearer {GENIUS_API_TOKEN}'}
    params = {'q': f'{title} {artist}'}
    
    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()
    
    if 'response' in data and data['response']['hits']:
        return data['response']['hits'][0]['result']
    return None

def get_lyrics(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    lyrics_div = soup.find('div', class_='lyrics')
    if not lyrics_div:
        lyrics_div = soup.find('div', class_='Lyrics__Container-sc-1ynbvzw-6')
    if not lyrics_div:
        lyrics_div = soup.find('div', attrs={"data-lyrics-container": "true"})
    
    if lyrics_div:
        return lyrics_div.get_text(separator="\n")
    
    return None