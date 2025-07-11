from fastapi import HTTPException
from fastapi.responses import Response, JSONResponse
from supabase import create_client, Client
from config.config import settings
from models import RumahAdatModel, PakaianAdatModel, AlatMusikModel, BudayaModel

class ProvinceService:
    def __init__(self):
        self.url = settings.supabase_url
        self.supabase_key = settings.supabase_key

    def get_all(self):
        supabase: Client = create_client(self.url, self.supabase_key)
        response = supabase.table('budaya').select("*").execute()
        return [self.map_budaya_model(row) for row in response.data]

    def get_by_id(self, id):
        supabase: Client = create_client(self.url, self.supabase_key)
        response = supabase.table("budaya").select("*").eq("id", id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Data tidak ditemukan")
        return self.map_budaya_model(response.data[0])

    def map_budaya_model(self, row: dict) -> BudayaModel:
        return BudayaModel(
            id=row["id"],
            nama_provinsi=row["nama_provinsi"],
            slug=row["slug"],
            rumah_adat=RumahAdatModel(
                nama_rumah_adat=row["nama_rumah_adat"],
                deskripsi_rumah_adat=row["deskripsi_rumah_adat"],
                url_rumah_adat=row["url_rumah_adat"],
            ),
            pakaian_adat=PakaianAdatModel(
                nama_pakaian_adat=row["nama_pakaian_adat"],
                deskripsi_pakaian_adat=row["deskripsi_pakaian_adat"],
                url_pakaian_adat=row["url_pakaian_adat"],
            ),
            alat_musik=AlatMusikModel(
                nama_alat_musik=row["nama_alat_musik"],
                deskripsi_alat_musik=row["deskripsi_alat_musik"],
                url_alat_musik=row["url_alat_musik"],
            ),
        )

province_service = ProvinceService()
