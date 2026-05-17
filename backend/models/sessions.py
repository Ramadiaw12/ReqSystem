"""
models/session.py — Schémas Pydantic pour les sessions SystemReq

Pydantic valide automatiquement les données entrantes et sortantes
de l'API. Si un champ obligatoire manque ou a le mauvais type,
FastAPI retourne une erreur 422 claire au frontend.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from enum import Enum


class SessionStatus(str, Enum):
    CREATED    = "created"
    COLLECTING = "collecting"
    ANALYZING  = "analyzing"
    GENERATING = "generating"
    DONE       = "done"
    ERROR      = "error"


class SessionCreate(BaseModel):
    """Données reçues depuis le formulaire React (ClientForm.js)."""

    client_name:  str            = Field(..., min_length=2, description="Nom complet du client")
    email:        str            = Field(..., description="Email de contact")
    telephone:    Optional[str]  = Field(None, description="Numéro de téléphone")
    site_web:     Optional[str]  = Field(None, description="Site web actuel")
    ville:        Optional[str]  = Field(None, description="Ville du client")
    pays:         Optional[str]  = Field(None, description="Pays du client")
    budget:       Optional[str]  = Field(None, description="Budget en EUR")
    services:     List[str]      = Field(default=[], description="Services cochés dans le formulaire")
    description:  Optional[str]  = Field(None, description="Description libre du projet")
    project_name: Optional[str]  = Field("Projet web", description="Nom du projet")


class SessionResponse(BaseModel):
    """Données retournées au frontend après création d'une session."""

    id:           str
    status:       SessionStatus
    client_name:  str
    project_name: str
    created_at:   str
    updated_at:   str
    error:        Optional[str] = None

    class Config:
        from_attributes = True