import spotipy
import re
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
    song_names = {}
    album_set= set() 
    for album in albums['albums']:
        track_uris = []
        album_name = re.sub(r'[\(\[].*?[\)\]]', '', album['name']).rstrip()
        if album_name in album_set:
            continue
        album_set.add(album_name)
        print(album_name, album['type'])
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
            song_name = song_names[audio_feature['uri']]
            # load dict with valence and album
            song_dict["valence"] = audio_feature['valence']
            song_dict["album"] = album_name
            # load song_info with song dict with song name as key
            song_info[song_name] = song_dict
    # print(song_info)
    #TODO fix so that we aren't overwriting the album of a song just because it is the single of that album

get_valence("chance the rapper")
