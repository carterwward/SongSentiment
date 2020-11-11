import spotipy
import re
import string
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_credentials import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))

def get_valence(artist_name):
    results = sp.search(q = "artist:" + artist_name, type = "artist")
    #print(results['artists']['items'])

    # initialize uri variable as empty string
    artist_uri = ""
    # iterate over list of artist dictionaries results['artists']['items']
    for artist_dict in results['artists']['items']:
        #print(artist_dict)
        # check to see if all lower case version of artist_name and name in each dict are equivalent
        if artist_name.lower() == artist_dict['name'].lower():
            # read uri into variable and break from loop
            #print(artist_dict['name'])
            artist_uri = artist_dict['uri']
            break
    #get discography
    discography = sp.artist_albums(artist_uri)
    #print(type(discography['items']))
    disco_uris = []
    for disco_album in discography['items']:
        disco_uris.append(disco_album['uri'])
    #print(disco_uris)

    albums = sp.albums(disco_uris)
    # print(type(albums['albums']))

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
            # print(track.keys())
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
            # print(song_name)
            if "feat." in song_name or '(with' in song_name:
                # print(song_name)
                song_name = re.sub(r'[\(\[].*?[\)\]]', '', song_name).rstrip()
                # print(song_name)
            
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

# print(get_valence('jpegmafia'))