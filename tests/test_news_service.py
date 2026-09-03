"""Tests for NewsService orchestration."""

from unittest.mock import Mock
import asyncio

from models import NewsArticle
from services.news_service import NewsService


def test_translation_uses_cache():
    """Repeated text should be translated only once while cached."""
    database = Mock()
    service = NewsService(database)
    translator = Mock()
    translator.translate.return_value = "Texte traduit"
    service.translator = translator

    first = asyncio.run(service._translate("same text"))
    second = asyncio.run(service._translate("same text"))

    assert first == second == "Texte traduit"
    translator.translate.assert_called_once_with("same text")


def test_mark_as_sent_persists_article():
    """Sending an article should make it known to the database."""
    database = Mock()
    service = NewsService(database)
    article = NewsArticle(
        guid="test:1",
        title="Test article",
        url="https://example.com",
        source="Test",
        category="news",
        summary="Summary",
        image="https://example.com/image.png",
    )

    service.mark_as_sent(article)

    database.save_news_pending.assert_called_once_with(
        guid="test:1",
        title="Test article",
        url="https://example.com",
        published="",
        source="Test",
        category="news",
        summary="Summary",
        image="https://example.com/image.png",
    )
    database.mark_as_sent.assert_called_once_with("test:1")
