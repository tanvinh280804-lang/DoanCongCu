from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_name: str = "Homestay Manager"
    database_url: str = "sqlite:///./homestay.db"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    groq_api_key: str = ""
    
    class Config:
        env_file = ".env"
        extra = "ignore"
settings = Settings()
    