from join_data import join_spotify_genius
from firebase import write_artist_dict
import time

def scrape_artists(artist_names):
    for artist_name in artist_names:
        time.sleep(30)
        artist_dict = join_spotify_genius(artist_name)

        write_artist_dict(artist_name, artist_dict)

if __name__ == "__main__":
    artist_names = ['mick jenkins', 'femdot', 'parliament', 'wavves', 'kanye west', 'joey bada$$', 'billy joel']
    scrape_artists(artist_names)
    