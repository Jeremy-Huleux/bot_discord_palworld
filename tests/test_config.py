"""
Unit tests for Palworld Bot configuration
"""

import pytest
import os
from config import Config


class TestConfig:
    """Test Config class"""

    def test_config_loading(self):
        """Test that config loads environment variables"""
        # These should load without error
        assert Config.LOG_LEVEL is not None
        assert isinstance(Config.NEWS_CHECK_INTERVAL, int)
        assert Config.NEWS_CHECK_INTERVAL > 0

    def test_default_values(self):
        """Test default values"""
        assert Config.LOG_LEVEL == "INFO"
        assert Config.NEWS_CHECK_INTERVAL == 300
        assert Config.TRANSLATION_ENABLED == True
        assert Config.CACHE_ENABLED == True

    def test_get_channels_config(self):
        """Test getting channels configuration"""
        channels = Config.get_channels_config()

        assert isinstance(channels, dict)
        assert "patch_notes" in channels
        assert "news" in channels
        assert "events" in channels
        assert "palworld_role" in channels

    def test_config_summary(self):
        """Test config summary output"""
        summary = Config.summary()

        assert isinstance(summary, str)
        assert "Configuration" in summary or "Palworld" in summary

    def test_database_path(self):
        """Test database path configuration"""
        db_path = Config.DATABASE_PATH

        assert db_path is not None
        assert "/app/data" in str(db_path) or "data" in str(db_path)

    def test_feature_toggles(self):
        """Test feature toggle configuration"""
        assert isinstance(Config.NEWS_ENABLED, bool)
        assert isinstance(Config.TRANSLATION_ENABLED, bool)
        assert isinstance(Config.CACHE_ENABLED, bool)
        assert isinstance(Config.DEBUG_MODE, bool)

    def test_cache_ttl(self):
        """Test cache TTL configuration"""
        assert isinstance(Config.CACHE_TTL, int)
        assert Config.CACHE_TTL > 0
        assert Config.CACHE_TTL == 3600  # Default 1 hour


class TestConfigValidation:
    """Test Config validation"""

    def test_validate_returns_bool(self):
        """Test that validate returns a boolean"""
        result = Config.validate()
        assert isinstance(result, bool)
