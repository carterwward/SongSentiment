import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'music-bot-b24c3',
})
db = firestore.client()
