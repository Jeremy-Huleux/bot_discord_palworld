"""
Unit tests for Palworld Bot utils (builders, formatters)
"""

import pytest
import discord
from models import NewsArticle, ServerStatus
from utils import EmbedBuilder, ViewBuilder, Formatter


class TestEmbedBuilder:
    """Test EmbedBuilder utility class"""

    def test_news_embed_basic(self):
        """Test building a basic news embed"""
        article = NewsArticle(
            guid="test:1",
            title="Test Article",
            url="https://example.com",
            source="Steam",
            summary="Test summary"
        )

        embed = EmbedBuilder.news_embed(article)

        assert isinstance(embed, discord.Embed)
        assert "Test Article" in embed.title
        assert embed.url == "https://example.com"

    def test_news_embed_patch_notes(self):
        """Test building a patch notes embed"""
        article = NewsArticle(
            guid="test:patch",
            title="Patch 1.0",
            url="https://example.com",
            source="Pocketpair",
            category="patch_notes"
        )

        embed = EmbedBuilder.news_embed(article)

        assert "🔧" in embed.title
        assert embed.color == discord.Color.green()

    def test_news_embed_events(self):
        """Test building an events embed"""
        article = NewsArticle(
            guid="test:event",
            title="Summer Event",
            url="https://example.com",
            source="Pocketpair",
            category="events"
        )

        embed = EmbedBuilder.news_embed(article)

        assert "🎁" in embed.title
        assert embed.color == discord.Color.gold()

    def test_server_status_embed(self):
        """Test building a server status embed"""
        status = ServerStatus(
            is_online=True,
            player_count=10,
            max_players=32,
            version="1.0.0"
        )

        embed = EmbedBuilder.server_status_embed(status)

        assert isinstance(embed, discord.Embed)
        assert "🟢" in embed.title
        assert "EN LIGNE" in embed.description


class TestViewBuilder:
    """Test ViewBuilder utility class"""

    def test_news_view_with_url(self):
        """Test building a news view with URL"""
        article = NewsArticle(
            guid="test:1",
            title="Test",
            url="https://example.com"
        )

        view = ViewBuilder.news_view(article)

        assert isinstance(view, discord.ui.View)
        assert len(view.children) > 0

    def test_news_view_without_url(self):
        """Test building a news view without URL"""
        article = NewsArticle(
            guid="test:1",
            title="Test",
            url=""
        )

        view = ViewBuilder.news_view(article)

        assert isinstance(view, discord.ui.View)
        assert len(view.children) == 0


class TestFormatter:
    """Test Formatter utility class"""

    def test_format_date_pocketpair(self):
        """Test formatting Pocketpair date (YYYY.MM.DD)"""
        formatted = Formatter.format_date("2026.07.10")

        assert formatted == "10/07/2026"

    def test_format_date_invalid(self):
        """Test formatting invalid date"""
        formatted = Formatter.format_date("invalid")

        assert formatted == "invalid"

    def test_format_date_none(self):
        """Test formatting None date"""
        formatted = Formatter.format_date(None)

        assert formatted == "Non disponible"

    def test_truncate_long_text(self):
        """Test truncating long text"""
        long_text = "a" * 150
        truncated = Formatter.truncate(long_text, max_length=100)

        assert len(truncated) <= 103  # max_length + len("...")
        assert truncated.endswith("...")

    def test_truncate_short_text(self):
        """Test truncating short text (should not truncate)"""
        short_text = "Hello World"
        truncated = Formatter.truncate(short_text, max_length=100)

        assert truncated == short_text

    def test_format_uptime(self):
        """Test formatting uptime"""
        # 1 day, 2 hours, 30 minutes
        seconds = 86400 + 7200 + 1800

        formatted = Formatter.format_uptime(seconds)

        assert "1j" in formatted
        assert "2h" in formatted
        assert "30m" in formatted

    def test_format_uptime_zero(self):
        """Test formatting zero uptime"""
        formatted = Formatter.format_uptime(0)

        assert formatted == "0m"
