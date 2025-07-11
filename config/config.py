from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_key: str = Field(..., env="SUPABASE_KEY")
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()