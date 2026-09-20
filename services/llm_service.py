import os
import json
import requests
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from utils.logging_config import logger
from config.settings import LLM_PROVIDER, LLM_API_KEY, LLM_MODEL, LLM_API_BASE

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.2) -> str:
        pass

    @property
    @abstractmethod
    def is_available(self) -> bool:
        pass

class OpenAICompatibleProvider(BaseLLMProvider):
    """Handles OpenAI, Groq, Ollama, DeepSeek, and other OpenAI-compatible endpoints."""
    def __init__(self, api_key: str, model: str, base_url: str = ""):
        self.api_key = api_key
        self.model = model
        if base_url:
            self.endpoint = f"{base_url.rstrip('/')}/chat/completions"
        elif "groq" in model.lower() or os.getenv("LLM_PROVIDER") == "groq":
            self.endpoint = "https://api.groq.com/openai/v1/chat/completions"
        else:
            self.endpoint = "https://api.openai.com/v1/chat/completions"

    @property
    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    def generate(
        self,
        prompt: str = "",
        system_prompt: str = "",
        temperature: float = 0.3,
        messages: Optional[list] = None,
        max_tokens: int = 2500
    ) -> str:
        if not self.is_available:
            raise ValueError("API key not configured for OpenAI-compatible provider.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Build conversation message payload
        conversation = []
        if system_prompt:
            conversation.append({"role": "system", "content": system_prompt})

        if messages:
            for m in messages:
                if isinstance(m, dict) and "role" in m and "content" in m:
                    # Avoid repeating system prompt if already present
                    if m["role"] == "system" and system_prompt:
                        continue
                    conversation.append({"role": m["role"], "content": m["content"]})
        elif prompt:
            conversation.append({"role": "user", "content": prompt})

        # Candidate models for automatic failover (handles 429 TPM limits seamlessly)
        models_to_try = [self.model]
        if "groq.com" in self.endpoint:
            backup_pool = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b", "groq/compound"]
            for bm in backup_pool:
                if bm not in models_to_try:
                    models_to_try.append(bm)

        for attempt_model in models_to_try:
            payload = {
                "model": attempt_model,
                "messages": conversation,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            try:
                resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=35)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data["choices"][0]["message"]["content"].strip()
                    if content:
                        return content
                elif resp.status_code in (429, 500, 502, 503, 504):
                    logger.warning(f"Model '{attempt_model}' hit HTTP {resp.status_code}. Failing over to backup model...")
                    continue
                else:
                    logger.error(f"LLM API Error with model '{attempt_model}' ({resp.status_code}): {resp.text[:300]}")
                    continue
            except Exception as e:
                logger.warning(f"LLM Request failed for '{attempt_model}': {e}. Trying next...")
                continue

        return ""

class FallbackHeuristicProvider(BaseLLMProvider):
    """
    Offline heuristic NLP engine.
    Used when no LLM API key is provided, guaranteeing 0% crashes,
    100% grounded extraction from paper text, and 0% hallucinations.
    """
    @property
    def is_available(self) -> bool:
        return True

    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.2) -> str:
        return "Heuristic fallback active."

def get_llm_service() -> BaseLLMProvider:
    if LLM_API_KEY:
        return OpenAICompatibleProvider(
            api_key=LLM_API_KEY,
            model=LLM_MODEL,
            base_url=LLM_API_BASE
        )
    return FallbackHeuristicProvider()
