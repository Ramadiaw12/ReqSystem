"""
models/cdc.py — Schémas Pydantic pour le cahier des charges
"""

from pydantic import BaseModel
from typing import List, Optional


class Requirement(BaseModel):
    """Une exigence structurée issue de l'AnalyzerAgent."""
    id:          str
    category:    str
    priority:    str
    moscow:      str
    description: str
    source:      Optional[str] = "explicite"


class CDCSection(BaseModel):
    """Une section du cahier des charges issue du GeneratorAgent."""
    id:      str
    title:   str
    content: str


class CDCStats(BaseModel):
    """Statistiques sur les exigences."""
    total:   int = 0
    haute:   int = 0
    moyenne: int = 0
    basse:   int = 0


class CDCResponse(BaseModel):
    """CDC complet retourné au frontend après le pipeline."""
    session_id:   str
    client_name:  str
    project_name: str
    services:     List[str]      = []
    budget:       Optional[str]  = None
    ville:        Optional[str]  = None
    pays:         Optional[str]  = None
    requirements: List[dict]     = []
    stats:        dict           = {}
    sections:     List[dict]     = []
    metadata:     dict           = {}
    summary:      Optional[str]  = None
    questions:    List[str]      = []
    generated_at: str