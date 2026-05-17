from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str = Field(..., description="Clé API OpenAI")
    openai_model: str = Field("gpt-4o", description="Modèle OpenAI")
    app_host: str = Field("0.0.0.0")
    app_port: int = Field(8000)
    debug: bool = Field(True)
    frontend_url: str = Field("http://localhost:3000")
    database_url: str = Field("sqlite:///./systemreq.db")
    secret_key: str = Field("change-this-in-production")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()
