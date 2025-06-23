import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseDB:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseDB, cls).__new__(cls)
            
            if not firebase_admin._apps:
                cred = credentials.Certificate("firebase_key.json")
                firebase_admin.initialize_app(cred)
            cls._instance.db = firestore.client()
        return cls._instance
    
    def get_instance(self):
        return self.db