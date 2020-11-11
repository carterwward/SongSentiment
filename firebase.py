import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('firebase_cred.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def write_artist_dict(artist_name: str, artist_dict: dict) -> None:
    """
    
    """
    for song, info in artist_dict.items():
        if song == '':
            continue
        doc_ref = db.collection(artist_name).document(song)
        doc_ref.set({
            u'album': info['album'],
            u'year': info['year'],
            u'features': info['features'],
            u'valence': info['valence'],
            u'lyrics': info['lyrics']
        })

def read_artist_dict(artist_name):
    artist_dict = db.collection(artist_name)
    docs =  artist_dict.stream()
    artist_dict = {}
    for doc in docs:
        artist_dict[doc.id] = doc.to_dict()
    return artist_dict

def read_song_dict(artist_name, song_name):
    doc_ref = db.collection(artist_name).document(song_name)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else: 
        print('doc does not exist')
