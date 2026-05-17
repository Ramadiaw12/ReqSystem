"""
config.py — Configuration centralisée de SystemReq
Lit les variables depuis le fichier .env via pydantic-settings.
Toute l'application importe `settings` depuis ce module.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Toutes les variables de configuration du projet.
    Pydantic valide les types au démarrage — si une variable obligatoire
    est absente, l'application s'arrête immédiatement avec un message clair.
    """

    # ── OpenAI ────────────────────────────────────────────────────────────
    openai_api_key: str = Field(..., description="Clé API OpenAI (obligatoire)")
    openai_model: str = Field("gpt-4o", description="Modèle OpenAI à utiliser")

    # ── Serveur ───────────────────────────────────────────────────────────
    app_host: str = Field("0.0.0.0", description="Hôte de l'API FastAPI")
    app_port: int = Field(8000, description="Port de l'API FastAPI")
    debug: bool = Field(True, description="Mode debug — désactiver en production")

    # ── CORS ──────────────────────────────────────────────────────────────
    frontend_url: str = Field(
        "http://localhost:3000",
        description="URL du frontend React (pour les headers CORS)"
    )

    # ── Base de données ───────────────────────────────────────────────────
    database_url: str = Field(
        "sqlite:///./systemreq.db",
        description="URL de connexion SQLAlchemy"
    )

    # ── Sécurité ──────────────────────────────────────────────────────────
    secret_key: str = Field(
        "change-this-in-production",
        description="Clé secrète pour les tokens JWT (si besoin futur)"
    )

    class Config:
        env_file = ".env"          # Fichier à charger
        env_file_encoding = "utf-8"
        case_sensitive = False     # OPENAI_API_KEY == openai_api_key


# ── Instance globale ──────────────────────────────────────────────────────────
# Import dans les autres modules :  from config import settings
settings = Settings()