from pydantic_settings import BaseSettings
from pathlib import Path

# Tìm file .env theo đường dẫn tuyệt đối
ENV_FILE = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    app_name: str = "Homestay Manager"
    database_url: str = "sqlite:///./homestay.db"
    secret_key: str = "default-secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    groq_api_key: str = ""
    
    class Config:
        env_file = str(ENV_FILE)
        extra = "ignore"

settings = Settings()
    