"""
Central configuration management for Palworld Bot
"""

import os
import logging
from typing import Optional
from pathlib import Path


class Config:
    """
    Centralized configuration for the bot.
    Loads from environment variables with defaults.
    """

    # ============================================================
    # DISCORD
    # ============================================================

    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    DISCORD_GUILD_ID: Optional[int] = (
        int(os.getenv("DISCORD_GUILD_ID")) 
        if os.getenv("DISCORD_GUILD_ID") 
        else None
    )

    # ============================================================
    # CHANNELS
    # ============================================================

    PATCH_NOTES_CHANNEL_ID: Optional[int] = (
        int(os.getenv("PATCH_NOTES_CHANNEL_ID"))
        if os.getenv("PATCH_NOTES_CHANNEL_ID")
        else None
    )

    NEWS_CHANNEL_ID: Optional[int] = (
        int(os.getenv("NEWS_CHANNEL_ID"))
        if os.getenv("NEWS_CHANNEL_ID")
        else None
    )

    EVENTS_CHANNEL_ID: Optional[int] = (
        int(os.getenv("EVENTS_CHANNEL_ID"))
        if os.getenv("EVENTS_CHANNEL_ID")
        else None
    )

    # ============================================================
    # ROLES
    # ============================================================

    PALWORLD_ROLE_ID: Optional[int] = (
        int(os.getenv("PALWORLD_ROLE_ID"))
        if os.getenv("PALWORLD_ROLE_ID")
        else None
    )

    # ============================================================
    # DATABASE
    # ============================================================

    DATABASE_PATH: Path = Path(
        os.getenv("DATABASE_PATH", "/app/data/news.db")
    )

    # ============================================================
    # NEWS
    # ============================================================

    NEWS_CHECK_INTERVAL: int = int(
        os.getenv("NEWS_CHECK_INTERVAL", "300")
    )

    NEWS_ENABLED: bool = os.getenv("NEWS_ENABLED", "true").lower() == "true"

    # ============================================================
    # PALWORLD SERVER (Future)
    # ============================================================

    PALWORLD_API_URL: Optional[str] = os.getenv("PALWORLD_API_URL")
    PALWORLD_API_KEY: Optional[str] = os.getenv("PALWORLD_API_KEY")
    PALWORLD_SERVER_URL: Optional[str] = os.getenv("PALWORLD_SERVER_URL")

    # ============================================================
    # LOGGING
    # ============================================================

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"

    # ============================================================
    # FEATURES
    # ============================================================

    TRANSLATION_ENABLED: bool = (
        os.getenv("TRANSLATION_ENABLED", "true").lower() == "true"
    )

    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour default

    # ============================================================
    # VALIDATION
    # ============================================================

    @classmethod
    def validate(cls) -> bool:
        """
        Validate critical configuration
        Returns True if valid, False otherwise
        """
        errors = []

        if not cls.DISCORD_TOKEN:
            errors.append("❌ DISCORD_TOKEN not defined")

        if not cls.DISCORD_GUILD_ID:
            errors.append("❌ DISCORD_GUILD_ID not defined")

        if not cls.NEWS_CHANNEL_ID:
            errors.append("⚠️  NEWS_CHANNEL_ID not defined (will use fallback)")

        if errors:
            for error in errors:
                logging.error(error)
            return not any("❌" in e for e in errors)  # Fail only on critical

        return True

    @classmethod
    def get_channels_config(cls) -> dict:
        """
        Get channel configuration for news sending
        """
        return {
            "patch_notes": cls.PATCH_NOTES_CHANNEL_ID or cls.NEWS_CHANNEL_ID,
            "news": cls.NEWS_CHANNEL_ID,
            "events": cls.EVENTS_CHANNEL_ID or cls.NEWS_CHANNEL_ID,
            "palworld_role": cls.PALWORLD_ROLE_ID,
        }

    @classmethod
    def summary(cls) -> str:
        """
        Return a summary of configuration (safe, no secrets)
        """
        return f"""
╔════════════════════════════════════════════════════════╗
║          Palworld Bot Configuration Summary            ║
╠════════════════════════════════════════════════════════╣
║ Guild ID:          {cls.DISCORD_GUILD_ID or 'Not set'}
║ News Channel:      {cls.NEWS_CHANNEL_ID or 'Not set'}
║ Patch Channel:     {cls.PATCH_NOTES_CHANNEL_ID or 'Uses News Channel'}
║ Events Channel:    {cls.EVENTS_CHANNEL_ID or 'Uses News Channel'}
║ Log Level:         {cls.LOG_LEVEL}
║ Debug Mode:        {cls.DEBUG_MODE}
║ News Enabled:      {cls.NEWS_ENABLED}
║ Translation:       {cls.TRANSLATION_ENABLED}
║ Cache:             {cls.CACHE_ENABLED} (TTL: {cls.CACHE_TTL}s)
║ Database:          {cls.DATABASE_PATH}
╚════════════════════════════════════════════════════════╝
        """
