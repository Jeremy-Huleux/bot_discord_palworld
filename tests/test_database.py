"""
Unit tests for Palworld Bot database
"""

import pytest
import tempfile
from pathlib import Path
from models import NewsArticle
from services.database import Database


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(db_path=db_path)
        yield db
        # Cleanup happens automatically when context manager exits


class TestDatabase:
    """Test Database class"""

    def test_database_creation(self, temp_db):
        """Test creating a database"""
        assert temp_db.db_path.exists()

    def test_create_tables(self, temp_db):
        """Test that tables are created"""
        cursor = temp_db.connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='news'"
        )
        assert cursor.fetchone() is not None

    def test_news_exists_false(self, temp_db):
        """Test checking if non-existent news exists"""
        assert not temp_db.news_exists("test:1")

    def test_save_and_check_news(self, temp_db):
        """Test saving and checking news"""
        temp_db.save_news_pending(
            guid="test:1",
            title="Test Article",
            url="https://example.com",
            published="2026.01.01",
            source="Test"
        )

        assert temp_db.news_exists("test:1")

    def test_get_unsent_news(self, temp_db):
        """Test getting unsent news"""
        # Save some news
        temp_db.save_news_pending(
            guid="test:1",
            title="Article 1",
            url="https://example.com/1",
            published="2026.01.01",
            source="Test"
        )

        temp_db.save_news_pending(
            guid="test:2",
            title="Article 2",
            url="https://example.com/2",
            published="2026.01.02",
            source="Test"
        )

        unsent = temp_db.get_unsent_news()

        assert len(unsent) == 2
        assert all(isinstance(a, NewsArticle) for a in unsent)

    def test_mark_as_sent(self, temp_db):
        """Test marking news as sent"""
        temp_db.save_news_pending(
            guid="test:1",
            title="Test Article",
            url="https://example.com",
            published="2026.01.01",
            source="Test"
        )

        temp_db.mark_as_sent("test:1")

        unsent = temp_db.get_unsent_news()
        assert len(unsent) == 0

    def test_news_url_exists(self, temp_db):
        """Test checking if URL exists"""
        url = "https://example.com/test"

        temp_db.save_news_pending(
            guid="test:1",
            title="Test",
            url=url,
            published="2026.01.01",
            source="Test"
        )

        assert temp_db.news_url_exists(url)
        assert not temp_db.news_url_exists("https://example.com/other")

    def test_duplicate_insert_ignored(self, temp_db):
        """Test that duplicate GUIDs are ignored"""
        guid = "test:1"

        # Insert first
        temp_db.save_news_pending(
            guid=guid,
            title="Article 1",
            url="https://example.com/1",
            published="2026.01.01",
            source="Test"
        )

        # Try to insert same GUID (should be ignored)
        temp_db.save_news_pending(
            guid=guid,
            title="Article 2 (Different)",
            url="https://example.com/2",
            published="2026.01.02",
            source="Test"
        )

        unsent = temp_db.get_unsent_news()
        assert len(unsent) == 1
        assert unsent[0].title == "Article 1"

    def test_save_with_category(self, temp_db):
        """Test saving news with category"""
        temp_db.save_news_pending(
            guid="test:patch",
            title="Patch 1.0",
            url="https://example.com",
            published="2026.01.01",
            source="Pocketpair",
            category="patch_notes",
            summary="Patch summary"
        )

        unsent = temp_db.get_unsent_news()
        assert len(unsent) == 1
        assert unsent[0].category == "patch_notes"
        assert unsent[0].summary == "Patch summary"

    def test_row_to_article_conversion(self, temp_db):
        """Test converting database row to NewsArticle"""
        temp_db.save_news_pending(
            guid="test:1",
            title="Test Article",
            url="https://example.com",
            published="2026.01.01",
            source="Test",
            category="news",
            summary="Test summary",
            image="https://example.com/image.png"
        )

        articles = temp_db.get_unsent_news()
        article = articles[0]

        assert article.guid == "test:1"
        assert article.title == "Test Article"
        assert article.source == "Test"
        assert article.summary == "Test summary"
        assert article.image == "https://example.com/image.png"
