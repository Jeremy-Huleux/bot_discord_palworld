"""
Unit tests for Palworld Bot models
"""

import pytest
from models import NewsArticle, Pal, Item, Boss, ServerStatus, Player


class TestNewsArticle:
    """Test NewsArticle dataclass"""

    def test_news_article_creation(self):
        """Test creating a NewsArticle"""
        article = NewsArticle(
            guid="test:1",
            title="Test Article",
            url="https://example.com",
            source="Test",
            published="2026.01.01"
        )

        assert article.guid == "test:1"
        assert article.title == "Test Article"
        assert article.source == "Test"
        assert article.category == "news"
        assert not article.is_sent()

    def test_news_article_missing_guid(self):
        """Test that NewsArticle requires GUID"""
        with pytest.raises(ValueError):
            NewsArticle(
                guid="",
                title="Test",
                url="https://example.com"
            )

    def test_news_article_missing_title(self):
        """Test that NewsArticle requires title"""
        with pytest.raises(ValueError):
            NewsArticle(
                guid="test:1",
                title="",
                url="https://example.com"
            )

    def test_mark_as_sent(self):
        """Test marking article as sent"""
        article = NewsArticle(
            guid="test:1",
            title="Test",
            url="https://example.com"
        )

        assert not article.is_sent()

        article.mark_as_sent()

        assert article.is_sent()
        assert article.sent_at is not None

    def test_article_to_dict(self):
        """Test converting article to dictionary"""
        article = NewsArticle(
            guid="test:1",
            title="Test Article",
            url="https://example.com",
            source="Test",
            category="patch_notes",
            summary="Test summary"
        )

        article_dict = article.to_dict()

        assert article_dict["guid"] == "test:1"
        assert article_dict["title"] == "Test Article"
        assert article_dict["category"] == "patch_notes"


class TestPal:
    """Test Pal dataclass"""

    def test_pal_creation(self):
        """Test creating a Pal"""
        pal = Pal(
            id=1,
            name="Fuack",
            name_en="Fuack",
            type=["Grass", "Flying"],
            rarity=4,
            hp=100
        )

        assert pal.id == 1
        assert pal.name == "Fuack"
        assert "Grass" in pal.type

    def test_pal_missing_name(self):
        """Test that Pal requires name"""
        with pytest.raises(ValueError):
            Pal(id=1, name="")


class TestServerStatus:
    """Test ServerStatus dataclass"""

    def test_server_status_creation(self):
        """Test creating ServerStatus"""
        status = ServerStatus(
            is_online=True,
            player_count=5,
            max_players=10
        )

        assert status.is_online
        assert status.player_slots_available == 5

    def test_server_offline(self):
        """Test offline server"""
        status = ServerStatus(
            is_online=False,
            player_count=0,
            max_players=10
        )

        assert not status.is_online
        assert status.player_slots_available == 10


class TestPlayer:
    """Test Player dataclass"""

    def test_player_creation(self):
        """Test creating a Player"""
        player = Player(
            uid="123456",
            name="TestPlayer",
            level=50,
            is_online=True
        )

        assert player.uid == "123456"
        assert player.name == "TestPlayer"
        assert player.is_online

    def test_player_to_dict(self):
        """Test converting player to dictionary"""
        player = Player(
            uid="123456",
            name="TestPlayer",
            level=50
        )

        player_dict = player.to_dict()

        assert player_dict["uid"] == "123456"
        assert player_dict["level"] == 50
