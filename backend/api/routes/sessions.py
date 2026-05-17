"""
api/routes/sessions.py — Endpoints de gestion des sessions

Routes disponibles :
    POST   /api/sessions/          → créer une session depuis le formulaire
    GET    /api/sessions/          → lister toutes les sessions
    GET    /api/sessions/{id}      → état d'une session (polling frontend)
"""

import logging
from fastapi import APIRouter, HTTPException

from models.session import SessionCreate, SessionResponse
from orchestrator.coordinator import Coordinator

logger = logging.getLogger(__name__)
router = APIRouter()

# Une seule instance partagée entre toutes les requêtes
coordinator = Coordinator()


@router.post("/", response_model=SessionResponse, status_code=201)
async def create_session(data: SessionCreate):
    """
    Crée une nouvelle session à partir des données du formulaire React.

    Le frontend envoie ce body :
    {
      "client_name": "Jean Marc",
      "email": "jean@example.com",
      "telephone": "+212 06...",
      "services": ["Site Vitrine", "SEO"],
      "budget": "15000",
      "ville": "Casablanca",
      "pays": "Maroc",
      "description": "Je veux un site vitrine..."
    }
    """
    try:
        session = await coordinator.create_session(data.model_dump())
        logger.info(f"Session créée : {session['id']}")
        return SessionResponse(**session)
    except Exception as e:
        logger.error(f"Erreur création session : {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[SessionResponse])
async def list_sessions():
    """Liste toutes les sessions — utile pour un historique."""
    sessions = coordinator.list_sessions()
    return [SessionResponse(**s) for s in sessions]


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """
    Retourne l'état actuel d'une session.
    Le frontend appelle cette route toutes les 2 secondes (polling)
    pour savoir si le pipeline est terminé.

    Statuts possibles : created | collecting | analyzing | generating | done | error
    """
    session = coordinator.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' introuvable"
        )
    return SessionResponse(**session)