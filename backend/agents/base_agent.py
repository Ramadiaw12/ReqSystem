"""
agents/base_agent.py — Classe de base pour tous les agents de SystemReq

Chaque agent (Collector, Analyzer, Generator) hérite de BaseAgent.
Cela garantit :
  - Une interface commune : méthode run() obligatoire
  - Un accès partagé au LLMClient
  - Un système de logging cohérent
  - Une gestion d'erreurs centralisée
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from utils.llm_client import LLMClient

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Classe abstraite dont héritent les 3 agents de SystemReq.

    Structure d'un agent concret :
    ─────────────────────────────
        class CollectorAgent(BaseAgent):
            def __init__(self):
                super().__init__(name="CollectorAgent")

            async def run(self, session_id: str, payload: dict) -> dict:
                result = await self.ask_llm(SYSTEM_PROMPT, user_message)
                return result
    """

    def __init__(self, name: str):
        """
        Args:
            name : identifiant lisible de l'agent (utilisé dans les logs)
        """
        self.name = name
        self.llm = LLMClient()
        self.logger = logging.getLogger(f"systemreq.{name}")

    # ── Interface obligatoire ─────────────────────────────────────────────────

    @abstractmethod
    async def run(self, session_id: str, payload: dict) -> dict:
        """
        Point d'entrée principal de l'agent.

        Args:
            session_id : identifiant unique de la session en cours
            payload    : données transmises par l'orchestrateur

        Returns:
            dict : résultat structuré de l'agent
        """
        pass

    # ── Méthodes utilitaires ──────────────────────────────────────────────────

    async def ask_llm(self, system_prompt: str, user_message: str) -> dict:
        """
        Appel simplifié au LLM — retourne directement un dict Python.
        Gère les erreurs de parsing et log l'activité.

        Args:
            system_prompt : rôle et instructions du modèle
            user_message  : données à analyser

        Returns:
            dict : réponse JSON parsée
        """
        self.log(f"Appel LLM en cours...")
        result = await self.llm.chat_json(system_prompt, user_message)

        if "error" in result:
            self.log(f"Erreur LLM : {result['error']}", level="error")

        return result

    async def ask_llm_text(self, system_prompt: str, user_message: str) -> str:
        """
        Variante qui retourne du texte libre (sans forcer le JSON).
        Utile pour générer du contenu narratif (ex: sections du CDC).
        """
        self.log("Appel LLM texte libre...")
        return await self.llm.chat(
            system_prompt, user_message, expect_json=False
        )

    def log(self, message: str, level: str = "info"):
        """
        Log formaté avec le nom de l'agent.

        Exemple de sortie :
            [CollectorAgent] Démarrage collecte pour session abc-123
        """
        full_msg = f"[{self.name}] {message}"
        if level == "error":
            self.logger.error(full_msg)
        elif level == "warning":
            self.logger.warning(full_msg)
        else:
            self.logger.info(full_msg)
        # Affiche aussi dans la console pendant le développement
        print(full_msg)

    def build_error_response(self, error_msg: str, session_id: str) -> dict:
        """
        Retourne un dict d'erreur standardisé — évite les crashs en cascade.

        Returns:
            dict : {"success": False, "error": "...", "session_id": "..."}
        """
        self.log(f"Erreur sur session {session_id} : {error_msg}", level="error")
        return {
            "success": False,
            "error": error_msg,
            "session_id": session_id,
            "agent": self.name,
        }