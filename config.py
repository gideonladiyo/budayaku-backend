from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field(..., env="APP_NAME")
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()