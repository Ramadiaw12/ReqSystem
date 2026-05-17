"""
main.py — Point d'entrée de l'API SystemReq

Lance l'application avec :
    uvicorn main:app --reload --port 8000

Documentation interactive disponible sur :
    http://localhost:8000/docs      (Swagger UI)
    http://localhost:8000/redoc     (ReDoc)
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.routes import sessions, cdc

# ── Configuration du logging ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Application FastAPI ───────────────────────────────────────────────────────
app = FastAPI(
    title="SystemReq API",
    description="Système multi-agents pour la génération automatique de cahiers des charges — EPS SARL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS — autorise le frontend React ────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(
    sessions.router,
    prefix="/api/sessions",
    tags=["Sessions"],
)
app.include_router(
    cdc.router,
    prefix="/api/cdc",
    tags=["CDC"],
)

# ── Routes de santé ───────────────────────────────────────────────────────────
@app.get("/", tags=["Santé"])
async def root():
    return {
        "app":     "SystemReq API",
        "version": "1.0.0",
        "status":  "running",
        "docs":    "/docs",
    }


@app.get("/health", tags=["Santé"])
async def health():
    """Endpoint de santé — vérifie que l'API est opérationnelle."""
    return {"status": "ok", "model": settings.openai_model}


# ── Lancement direct (optionnel) ──────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug,
    )