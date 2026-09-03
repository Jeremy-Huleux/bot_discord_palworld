"""Regression tests for cross-source news deduplication."""

from unittest.mock import Mock

from models import NewsArticle
from services.news_service import NewsService


def test_same_title_from_two_sources_is_sent_once():
    """Steam and Pocketpair copies of one article must collapse to one item."""
    database = Mock()
    database.news_exists.return_value = False
    database.news_url_exists.return_value = False
    service = NewsService(database)
    seen_keys = set()

    steam_article = NewsArticle(
        guid="steam:1",
        title="Palworld 1.0 is out now",
        url="https://store.steampowered.com/news/1",
        source="Steam",
    )
    pocketpair_article = NewsArticle(
        guid="pocketpair:1",
        title="Palworld 1.0 is out now!",
        url="https://www.pocketpair.jp/en/game-news/1",
        source="Pocketpair",
    )

    assert not service._is_known_article(steam_article, seen_keys)
    assert service._is_known_article(pocketpair_article, seen_keys)
