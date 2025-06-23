from config.db_config import FirebaseDB
from fastapi import HTTPException
from fastapi.responses import Response
from models import IslandCulture
from typing import List

firebase = FirebaseDB()

class FirebaseService:
    def __init__(self):
        self.db = firebase.get_instance()
    
    def get_all_culture(self):
        result = self.db.collection("pulau").stream()
        data = [{"id": doc.id, "data": doc.to_dict()} for doc in result]
        return data
    
    def get_culture_by_id(self, id: str):
        doc_ref = self.db.collection("pulau").document(id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="Pulau tidak ditemukan")

firebase_serivce = FirebaseService()