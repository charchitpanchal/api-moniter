import json
import logging
from abc import ABC, abstractmethod
from app.core.config import settings

logger = logging.getLogger("ai.provider")


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """
    Works with any OpenAI-API-compatible endpoint (OpenAI itself, or
    Groq, which exposes the same API shape at a different base_url).
    """
    def __init__(self, api_key: str, model: str, base_url: str | None = None):
        from openai import AsyncOpenAI
        if base_url:
            self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str):
        from anthropic import AsyncAnthropic
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text


def get_provider() -> LLMProvider:
    provider_name = settings.ai_provider.lower()

    if provider_name == "openai":
        return OpenAIProvider(api_key=settings.ai_api_key, model=settings.ai_model)
    elif provider_name == "groq":
        return OpenAIProvider(
            api_key=settings.ai_api_key,
            model=settings.ai_model,
            base_url="https://api.groq.com/openai/v1",
        )
    elif provider_name == "anthropic":
        return AnthropicProvider(api_key=settings.ai_api_key, model=settings.ai_model)
    else:
        raise ValueError(f"Unsupported AI_PROVIDER: {provider_name}")