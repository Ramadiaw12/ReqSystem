"""
utils/llm_client.py — Client OpenAI centralisé pour SystemReq

Ce module expose une seule classe LLMClient utilisée par les 3 agents.
Avantages :
  - La clé API et le modèle sont configurés en un seul endroit
  - On peut facilement changer de modèle (ex: gpt-4o-mini pour tests)
  - Gestion des erreurs et du logging centralisés
"""

import json
import logging
from typing import Optional
from openai import AsyncOpenAI
from config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Client OpenAI asynchrone partagé par tous les agents de SystemReq.

    Usage dans un agent :
        response = await self.llm.chat(
            system_prompt="Tu es un expert...",
            user_message="Voici les besoins du client : ...",
        )
    """

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    async def chat(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.3,
        expect_json: bool = True,
    ) -> str:
        """
        Envoie un message au modèle et retourne la réponse en texte brut.

        Args:
            system_prompt : instructions de rôle pour le modèle
            user_message  : contenu envoyé par l'agent
            temperature   : 0.0 = déterministe, 1.0 = créatif
            expect_json   : si True, force le mode JSON (response_format)

        Returns:
            str : réponse brute du modèle (JSON string ou texte libre)
        """
        logger.info(f"[LLMClient] Appel modèle={self.model} temp={temperature}")

        kwargs = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message},
            ],
            "temperature": temperature,
            "max_tokens": 4000,
        }

        # Mode JSON structuré garanti que la réponse est du JSON valide
        if expect_json:
            kwargs["response_format"] = {"type": "json_object"}

        response = await self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content

        logger.info(f"[LLMClient] Réponse reçue ({len(content)} caractères)")
        return content

    async def chat_json(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.3,
    ) -> dict:
        """
        Variante de chat() qui parse automatiquement la réponse en dict Python.

        Returns:
            dict : réponse JSON parsée, ou dict avec clé 'error' en cas d'échec
        """
        raw = await self.chat(system_prompt, user_message, temperature, expect_json=True)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error(f"[LLMClient] Erreur parsing JSON : {e}")
            logger.error(f"[LLMClient] Réponse brute : {raw[:300]}")
            return {"error": "parsing_failed", "raw": raw}