"""QuantAI application settings and configuration helpers.

Discovered from actual backend usage without exposing credentials.
"""

from __future__ import annotations

import os
from typing import Tuple
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"
DEFAULT_OPENROUTER_MODEL = "stealth/ox-alpha"
DEFAULT_PROVIDER_ORDER: Tuple[str, ...] = ("groq_primary", "groq_secondary", "openrouter_ox_alpha")


class Settings(BaseSettings):
    """Central settings model loaded from environment or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Provider credentials and model identifiers
    groq_api_key_primary: str = Field(default="", alias="GROQ_API_KEY_PRIMARY")
    groq_model_primary: str = Field(default=DEFAULT_GROQ_MODEL, alias="GROQ_MODEL_PRIMARY")
    groq_api_key_secondary: str = Field(default="", alias="GROQ_API_KEY_SECONDARY")
    groq_model_secondary: str = Field(default=DEFAULT_GROQ_MODEL, alias="GROQ_MODEL_SECONDARY")
    openrouter_api_key: str = Field(default="", alias="OPENROUTER_API_KEY")
    openrouter_model: str = Field(default=DEFAULT_OPENROUTER_MODEL, alias="OPENROUTER_MODEL")
    ai_provider_order: str = Field(default=",".join(DEFAULT_PROVIDER_ORDER), alias="AI_PROVIDER_ORDER")

    # Developer tooling & telemetry controls (must default to disabled)
    quantai_devtools: str = Field(default="0", alias="QUANTAI_DEVTOOLS")

    @property
    def provider_order(self) -> Tuple[str, ...]:
        parts = tuple(item.strip().lower() for item in self.ai_provider_order.split(",") if item.strip())
        if len(parts) != len(DEFAULT_PROVIDER_ORDER) or set(parts) != set(DEFAULT_PROVIDER_ORDER):
            return DEFAULT_PROVIDER_ORDER
        return parts

    @property
    def devtools_enabled(self) -> bool:
        # Telemetry is strictly disabled unless explicitly set to '1'
        return self.quantai_devtools.strip() == "1"


settings = Settings()
