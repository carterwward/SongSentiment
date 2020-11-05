import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('firebase_cred.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def write_artist_dict(artist_name, artist_dict):
    for song, info in artist_dict.items():
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