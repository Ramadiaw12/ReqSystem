"""
utils/llm_client.py — Client OpenAI centralisé pour SystemReq
"""

import json
import logging
from openai import AsyncOpenAI
from config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Client OpenAI asynchrone partagé par tous les agents."""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model  = settings.openai_model

    async def chat(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.3,
        expect_json: bool = True,
        max_tokens: int = 4000,
    ) -> str:
        logger.info(f"[LLMClient] Appel modèle={self.model} temp={temperature} max_tokens={max_tokens}")

        kwargs = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if expect_json:
            kwargs["response_format"] = {"type": "json_object"}

        response = await self.client.chat.completions.create(**kwargs)
        content  = response.choices[0].message.content

        logger.info(f"[LLMClient] Réponse reçue ({len(content)} caractères)")
        return content

    async def chat_json(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.3,
        max_tokens: int = 4000,
    ) -> dict:
        """Appel qui parse automatiquement la réponse en dict Python."""
        raw = await self.chat(
            system_prompt, user_message,
            temperature=temperature,
            expect_json=True,
            max_tokens=max_tokens,
        )
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error(f"[LLMClient] Erreur parsing JSON : {e}")
            return {"error": "parsing_failed", "raw": raw}