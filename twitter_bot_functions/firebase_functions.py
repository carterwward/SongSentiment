import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import string
import re
cred = credentials.Certificate('firebase_cred.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def write_artist_dict(artist_name: str, artist_dict: dict) -> None:
    artist_name = artist_name.lower()
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

def update_song_doc(artist_name: str, song_name: str, field: str, value):
    doc_ref = db.collection(artist_name).document(song_name)

    doc_ref.set({
        field: value
        }, merge=True)

def read_artist_dict(artist_name):
    artist_name = artist_name.lower()
    artist_dict = db.collection(artist_name)
    docs =  artist_dict.stream()
    artist_dict = {}
    for doc in docs:
        artist_dict[doc.id] = doc.to_dict()
    return artist_dict

def read_song_dict(artist_name, song_name):
    artist_name = artist_name.lower()
    song_name = song_name.lower()
    song_name = song_name.translate(str.maketrans('', '', string.punctuation)).replace('  ', ' ').strip()
    doc_ref = db.collection(artist_name).document(song_name)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else: 
        print(song_name, 'not found')
        return {}        

def read_all_discogs():
    db_ref = db.collections()
    collection_dict = {}
    for collection in db_ref:
        artist_name = collection.id
        docs = collection.list_documents()
        for doc in docs: 
            doc_obj = doc.get()
            if doc_obj.id not in collection_dict.keys():
                collection_dict[artist_name + "_" + doc_obj.id] = doc_obj.to_dict()
            else:
                print('duplicate', doc_obj.id)

    return collection_dict
