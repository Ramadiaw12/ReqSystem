"""
orchestrator/coordinator.py — Orchestrateur central de SystemReq

Rôle : coordonner les 3 agents en séquence et gérer l'état des sessions.

Pipeline :
    Formulaire client
        └─► CollectorAgent  (extraction des besoins)
                └─► AnalyzerAgent   (classification + priorisation)
                        └─► GeneratorAgent  (génération du CDC complet)
"""

import uuid
import logging
from datetime import datetime
from typing import Optional

from agents.collector  import CollectorAgent
from agents.analyzer   import AnalyzerAgent
from agents.generator  import GeneratorAgent

logger = logging.getLogger(__name__)

# Stockage en mémoire
# Pour la phase de développement. À remplacer par PostgreSQL/SQLite en production.
_sessions: dict = {}   # session_id → données de la session
_cdcs: dict     = {}   # session_id → CDC généré


class Coordinator:
    """
    Orchestrateur central — gère le cycle de vie des sessions et
    enchaîne les 3 agents dans le bon ordre.

    Usage depuis les routes FastAPI :
        coordinator = Coordinator()

        # Créer une session
        session = await coordinator.create_session(form_data)

        # Lancer le pipeline complet
        cdc = await coordinator.run_pipeline(session["id"])

        # Récupérer le résultat
        cdc = coordinator.get_cdc(session_id)
    """

    def __init__(self):
        self.collector  = CollectorAgent()
        self.analyzer   = AnalyzerAgent()
        self.generator  = GeneratorAgent()

    # Gestion des sessions 

    async def create_session(self, form_data: dict) -> dict:
        """
        Crée une nouvelle session à partir des données du formulaire EPS SARL.

        Args:
            form_data : données brutes du formulaire React
                {
                  client_name, email, telephone, site_web,
                  ville, pays, budget, services, description
                }

        Returns:
            dict : session créée avec son identifiant unique
        """
        session_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        session = {
            "id":          session_id,
            "status":      "created",        # created | collecting | analyzing | generating | done | error
            "form_data":   form_data,
            "client_name": form_data.get("client_name", "Client"),
            "project_name": form_data.get("project_name", "Projet web"),
            "created_at":  now,
            "updated_at":  now,
            # Résultats intermédiaires (remplis au fur et à mesure)
            "collected":   None,
            "analyzed":    None,
            "error":       None,
        }

        _sessions[session_id] = session
        logger.info(f"[Coordinator] Session créée : {session_id}")
        return session

    def get_session(self, session_id: str) -> Optional[dict]:
        """Retourne la session ou None si introuvable."""
        return _sessions.get(session_id)

    def list_sessions(self) -> list:
        """Retourne toutes les sessions (pour l'historique)."""
        return list(_sessions.values())

    def get_cdc(self, session_id: str) -> Optional[dict]:
        """Retourne le CDC généré ou None si pas encore prêt."""
        return _cdcs.get(session_id)

    # Pipeline principal

    async def run_pipeline(self, session_id: str) -> dict:
        """
        Lance le pipeline complet : Collect → Analyze → Generate.

        Met à jour le statut de la session à chaque étape.
        En cas d'erreur sur un agent, stoppe le pipeline et retourne l'erreur.

        Args:
            session_id : identifiant de la session à traiter

        Returns:
            dict : CDC généré complet, ou dict d'erreur
        """
        session = _sessions.get(session_id)
        if not session:
            return {"success": False, "error": f"Session {session_id} introuvable"}

        form_data = session["form_data"]

        try:
            # Étape 1 : Collecte 
            self._set_status(session_id, "collecting")
            logger.info(f"[Coordinator] Étape 1 — Collecte ({session_id})")

            collected = await self.collector.run(session_id, form_data)

            if not collected.get("success"):
                return self._handle_error(session_id, "Échec de la collecte", collected)

            _sessions[session_id]["collected"] = collected

            # Étape 2 : Analyse 
            self._set_status(session_id, "analyzing")
            logger.info(f"[Coordinator] Étape 2 — Analyse ({session_id})")

            analyzer_payload = {
                **form_data,
                "needs": collected.get("needs", []),
            }
            analyzed = await self.analyzer.run(session_id, analyzer_payload)

            if not analyzed.get("success"):
                return self._handle_error(session_id, "Échec de l'analyse", analyzed)

            _sessions[session_id]["analyzed"] = analyzed

            # Étape 3 : Génération 
            self._set_status(session_id, "generating")
            logger.info(f"[Coordinator] Étape 3 — Génération CDC ({session_id})")

            generator_payload = {
                **form_data,
                "requirements": analyzed.get("requirements", []),
            }
            generated = await self.generator.run(session_id, generator_payload)

            if not generated.get("success"):
                return self._handle_error(session_id, "Échec de la génération", generated)

            # ── Assemblage du CDC final ───────────────────────────────────
            cdc = {
                "session_id":   session_id,
                "client_name":  form_data.get("client_name", ""),
                "project_name": form_data.get("project_name", "Projet web"),
                "services":     form_data.get("services", []),
                "budget":       form_data.get("budget", ""),
                "ville":        form_data.get("ville", ""),
                "pays":         form_data.get("pays", ""),
                "requirements": analyzed.get("requirements", []),
                "stats":        analyzed.get("stats", {}),
                "sections":     generated.get("sections", []),
                "metadata":     generated.get("metadata", {}),
                "summary":      collected.get("summary", ""),
                "questions":    collected.get("questions", []),
                "generated_at": datetime.utcnow().isoformat(),
            }

            _cdcs[session_id] = cdc
            self._set_status(session_id, "done")
            logger.info(f"[Coordinator] Pipeline terminé — session {session_id}")
            return cdc

        except Exception as e:
            logger.error(f"[Coordinator] Erreur inattendue : {e}")
            return self._handle_error(session_id, str(e), {})

    # ── Méthodes privées ──────────────────────────────────────────────────────

    def _set_status(self, session_id: str, status: str):
        """Met à jour le statut de la session."""
        if session_id in _sessions:
            _sessions[session_id]["status"]     = status
            _sessions[session_id]["updated_at"] = datetime.utcnow().isoformat()

    def _handle_error(self, session_id: str, message: str, details: dict) -> dict:
        """Passe la session en état d'erreur et retourne un dict d'erreur."""
        self._set_status(session_id, "error")
        if session_id in _sessions:
            _sessions[session_id]["error"] = message
        return {"success": False, "error": message, "details": details}