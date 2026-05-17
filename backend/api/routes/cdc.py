"""
api/routes/cdc.py — Endpoints du pipeline et export du CDC

Routes disponibles :
    POST   /api/cdc/{session_id}/run      → lancer le pipeline 3 agents
    GET    /api/cdc/{session_id}          → récupérer le CDC généré
    GET    /api/cdc/{session_id}/export/docx → télécharger en Word
    GET    /api/cdc/{session_id}/export/pdf  → télécharger en PDF
"""

import logging
import os
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from models.cdc import CDCResponse
from orchestrator.coordinator import Coordinator

logger = logging.getLogger(__name__)
router = APIRouter()
coordinator = Coordinator()


@router.post("/{session_id}/run")
async def run_pipeline(session_id: str, background_tasks: BackgroundTasks):
    """
    Lance le pipeline complet (Collect → Analyze → Generate) pour une session.

    Le pipeline tourne en tâche de fond (BackgroundTasks) pour ne pas
    bloquer la réponse HTTP. Le frontend suit la progression via polling
    sur GET /api/sessions/{session_id}.

    Réponse immédiate :
        {"message": "Pipeline démarré", "session_id": "..."}
    """
    session = coordinator.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' introuvable"
        )

    if session["status"] == "done":
        return {"message": "CDC déjà généré", "session_id": session_id}

    if session["status"] in ("collecting", "analyzing", "generating"):
        return {"message": "Pipeline déjà en cours", "session_id": session_id}

    # Lance le pipeline en arrière-plan
    background_tasks.add_task(coordinator.run_pipeline, session_id)

    logger.info(f"Pipeline démarré en arrière-plan : {session_id}")
    return {"message": "Pipeline démarré", "session_id": session_id}


@router.get("/{session_id}", response_model=CDCResponse)
async def get_cdc(session_id: str):
    """
    Retourne le CDC généré pour une session.
    À appeler une fois que le statut de la session est 'done'.
    """
    cdc = coordinator.get_cdc(session_id)
    if not cdc:
        session = coordinator.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session introuvable")

        status = session.get("status", "unknown")
        if status == "error":
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la génération : {session.get('error', 'Erreur inconnue')}"
            )
        raise HTTPException(
            status_code=202,
            detail=f"CDC pas encore prêt — statut actuel : {status}"
        )

    return CDCResponse(**cdc)


@router.get("/{session_id}/export/docx")
async def export_docx(session_id: str):
    """
    Génère et retourne le CDC en format Word (.docx).
    Le navigateur déclenche automatiquement le téléchargement.
    """
    cdc = coordinator.get_cdc(session_id)
    if not cdc:
        raise HTTPException(status_code=404, detail="CDC introuvable")

    try:
        from utils.docx_exporter import export_to_docx
        filepath = await export_to_docx(cdc)
        filename = f"CDC_{cdc['client_name'].replace(' ', '_')}_{session_id[:6]}.docx"
        return FileResponse(
            path=filepath,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=filename
        )
    except Exception as e:
        logger.error(f"Erreur export DOCX : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur export DOCX : {str(e)}")


@router.get("/{session_id}/export/pdf")
async def export_pdf(session_id: str):
    """
    Génère et retourne le CDC en format PDF.
    Le navigateur déclenche automatiquement le téléchargement.
    """
    cdc = coordinator.get_cdc(session_id)
    if not cdc:
        raise HTTPException(status_code=404, detail="CDC introuvable")

    try:
        from utils.pdf_exporter import export_to_pdf
        filepath = await export_to_pdf(cdc)
        filename = f"CDC_{cdc['client_name'].replace(' ', '_')}_{session_id[:6]}.pdf"
        return FileResponse(
            path=filepath,
            media_type="application/pdf",
            filename=filename
        )
    except Exception as e:
        logger.error(f"Erreur export PDF : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur export PDF : {str(e)}")