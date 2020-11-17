from join_data import join_spotify_genius
from firebase import write_artist_dict
import time

def scrape_artists(artist_names):
    for artist_name in artist_names:
        artist_dict = join_spotify_genius(artist_name)

        write_artist_dict(artist_name, artist_dict)
        time.sleep(40)

if __name__ == "__main__":
    artist_names = ['eminem', 'justin bieber', 'nirvana', 'prince', 'queen', 'sza', 'ari lennox']
    scrape_artists(artist_names)
