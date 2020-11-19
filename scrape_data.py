from firebase import write_artist_dict
import time
import re
import string
import lyricsgenius
from genius_credentials import client_access_token
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_credentials import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

def get_discography(artist):
    genius = lyricsgenius.Genius(client_access_token)
    genius.verbose = False
    genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
    # genius.skip_non_songs = False # Include hits thought to be non-songs (e.g. track lists)
    genius.excluded_terms = ["(Remix)", "(Live)"] # Exclude songs with these words in their title
    print(artist, "...")
    try:
        disco = genius.search_artist(artist)

        discog = {}

        for song in disco.songs:
            song_dict = {}
            if song.lyrics == "Transcribing needed":
                continue

            features = [feature_dict['name'] for feature_dict in song.featured_artists]

            song_dict['features'] = features
            song_dict['album_name'] = song.album
            song_dict['lyrics'] = song.lyrics
            song_dict['year'] = song.year
            song_name = song.title.encode('ascii', 'ignore').decode().lower()
            song_name = song_name.translate(str.maketrans('', '', string.punctuation)).replace('  ', ' ')
            discog[song_name] = song_dict

        return discog
    except:
        time.sleep(60)
        print('restart')
        get_discography(artist)

def get_valence(artist_name):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))
    results = sp.search(q = "artist:" + artist_name, type = "artist")

    # initialize uri variable as empty string
    artist_uri = ""

    # iterate over list of artist dictionaries results['artists']['items']
    for artist_dict in results['artists']['items']:

        # check to see if all lower case version of artist_name and name in each dict are equivalent
        if artist_name.lower() == artist_dict['name'].lower():

            # read uri into variable and break from loop
            artist_uri = artist_dict['uri']
            break

    #get discography
    discography = sp.artist_albums(artist_uri)

    disco_uris = []
    for disco_album in discography['items']:
        disco_uris.append(disco_album['uri'])

    albums = sp.albums(disco_uris)

    song_info = {}
    sin_songs_info = {}
    song_names = {}
    album_set= set() 
    for album in albums['albums']:
        track_uris = []
        album_name = re.sub(r'[\(\[].*?[\)\]]', '', album['name']).rstrip().lower()

        if album_name in album_set:
            continue
        album_set.add(album_name)
        num_tracks = album['total_tracks']
        # iterate over tracks
        for track in album['tracks']['items']:
            # get audio features data via uri
            track_uris.append(track['uri'])
            song_names[track['uri']] = track['name']
        audio_features = sp.audio_features(track_uris)
        # add valence and album name to track dict
        for audio_feature in audio_features:
            # initialize dict for song
            song_dict = {}
            # retrieve name using uri
            song_name = song_names[audio_feature['uri']].lower()
            # if the song has a feature, remove that part of the name
            if "feat." in song_name or '(with' in song_name:

                song_name = re.sub(r'[\(\[].*?[\)\]]', '', song_name).rstrip()

            
            if '- remix' in song_name or " remix)" in song_name:
                continue

            song_name = song_name.translate(str.maketrans('', '', string.punctuation)).replace('  ', ' ')

            # load dict with valence and album
            song_dict["valence"] = audio_feature['valence']
            song_dict["album"] = album_name
            # load song_info with song dict with song name as key
            if num_tracks > 4:
                song_info[song_name] = song_dict
            else: 
                sin_songs_info[song_name] = song_dict
 
    single_set = set(sin_songs_info.keys()) - set(song_info.keys())

    for single_name in single_set:
        song_info[single_name] = sin_songs_info[single_name]
    return song_info

def join_spotify_genius(artist):
    spotify_dict = get_valence(artist)
    genius_dict = get_discography(artist)
    common_keys = set(genius_dict.keys()) & set(spotify_dict.keys())
    # print("in spot not genius Keys:", set(spotify_dict.keys()) - set(genius_dict.keys()), '\n')
    # print("in genius not spot Keys:", set(genius_dict.keys()) - set(spotify_dict.keys()), '\n')
    # print("Common Keys:", common_keys)
    print("len of discog", len(common_keys))
    full_dict = {}
    for key in common_keys:
        song_dict = {}

        song_dict['valence'] = spotify_dict[key]['valence']
        song_dict['album'] = spotify_dict[key]['album']
        song_dict['lyrics'] = genius_dict[key]['lyrics']
        song_dict['year'] = genius_dict[key]['year']
        song_dict['features'] = genius_dict[key]['features']
        full_dict[key] = song_dict
    return full_dict

def scrape_artists(artist_names):
    for artist_name in artist_names:
        artist_dict = join_spotify_genius(artist_name)

        write_artist_dict(artist_name, artist_dict)
        time.sleep(40)

if __name__ == "__main__":
    artist_names = []
    scrape_artists(artist_names)
