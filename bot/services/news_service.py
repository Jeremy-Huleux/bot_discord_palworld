import logging
import asyncio
import re
import time
import aiohttp
import feedparser
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from typing import List

from config import Config
from models import NewsArticle
from services.pocketpair import PocketpairService
from services.database import Database

logger = logging.getLogger("palworld_bot.news_service")


class NewsService:
    """
    Aggregates news from multiple sources (Steam, Pocketpair).
    Handles fetching, translation, and database storage.
    Uses dependency injection for better testability.
    """

    def __init__(self, database: Database):
        """
        Initialize news service
        
        Args:
            database: Database instance for news storage
        """
        self.database = database

        self.feeds = [
            {
                "name": "Steam",
                "url": "https://store.steampowered.com/feeds/news/app/1623730/"
            }
        ]

        # Only initialize translator if translation is enabled
        self.translator = (
            GoogleTranslator(source="auto", target="fr")
            if Config.TRANSLATION_ENABLED
            else None
        )
        self.translation_cache = {}

        self.pocketpair = PocketpairService(database)

    def categorize_news(self, title: str) -> str:
        """
        Categorize news based on title keywords
        
        Args:
            title: Article title
            
        Returns:
            Category: 'patch_notes', 'events', or 'news'
        """
        title_lower = title.lower()

        patch_keywords = [
            "patch",
            "fix",
            "update",
            "v1.",
            "v0.",
            "changelog",
            "balance",
            "bug"
        ]

        if any(kw in title_lower for kw in patch_keywords):
            return "patch_notes"

        event_keywords = [
            "event",
            "halloween",
            "sale",
            "drop",
            "tournament",
            "summer"
        ]

        if any(kw in title_lower for kw in event_keywords):
            return "events"

        return "news"

    @staticmethod
    def _article_key(article: NewsArticle) -> str:
        """Build a stable key for cross-source duplicate detection."""
        title = re.sub(r"[^a-z0-9]+", " ", article.title.lower()).strip()
        return title

    def _is_known_article(self, article: NewsArticle, seen_keys: set[str]) -> bool:
        """Check database and current batch for an already known article."""
        if self.database.news_exists(article.guid):
            return True
        if article.url and self.database.news_url_exists(article.url):
            return True

        article_key = self._article_key(article)
        if article_key and article_key in seen_keys:
            return True

        seen_keys.add(article_key)
        return False

    async def _translate(self, text: str) -> str:
        """
        Safely translate text to French
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text or original if translation disabled/failed
        """
        if not text or not self.translator:
            return text

        now = time.monotonic()
        cached = self.translation_cache.get(text)
        if Config.CACHE_ENABLED and cached:
            translated, cached_at = cached
            if now - cached_at < Config.CACHE_TTL:
                return translated
            self.translation_cache.pop(text, None)

        for attempt in range(3):
            try:
                translated = self.translator.translate(text)
                if Config.CACHE_ENABLED:
                    self.translation_cache[text] = (translated, now)
                return translated
            except Exception as error:
                if attempt == 2:
                    logger.warning(f"Translation failed: {error}")
                    return text
                await asyncio.sleep(2 ** attempt)

    def extract_details(
        self,
        html_content: str
    ):

        if not html_content:
            return "", ""

        soup = BeautifulSoup(
            html_content,
            "html.parser"
        )

        img_tag = soup.find("img")

        image_url = (
            img_tag.get("src", "")
            if img_tag
            else ""
        )

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        summary = (
            text[:300] + "..."
            if len(text) > 300
            else text
        )

        return summary, image_url

    async def fetch_steam_news(self) -> List[NewsArticle]:
        """
        Fetch news from Steam RSS feed
        
        Returns:
            List of NewsArticle dataclasses
        """
        results = []

        async with aiohttp.ClientSession() as session:

            for feed_info in self.feeds:

                try:

                    async with session.get(
                        feed_info["url"],
                        timeout=aiohttp.ClientTimeout(total=15)
                    ) as response:

                        if response.status != 200:
                            continue

                        content = await response.text()

                    feed = feedparser.parse(content)

                    for entry in feed.entries:

                        guid = entry.get("id", entry.get("link"))

                        if not guid:
                            continue

                        raw_title = entry.get("title", "Sans titre")

                        raw_summary = entry.get(
                            "summary",
                            entry.get("description", "")
                        )

                        clean_summary, image_url = (
                            self.extract_details(raw_summary)
                        )

                        # Translate title and summary if enabled
                        title_fr = await self._translate(raw_title)
                        summary_fr = await self._translate(clean_summary)

                        category = self.categorize_news(raw_title)

                        article = NewsArticle(
                            guid=guid,
                            title=title_fr,
                            summary=summary_fr,
                            image=image_url,
                            url=entry.get("link", ""),
                            published=entry.get("published", ""),
                            source="Steam",
                            category=category,
                        )

                        if not self._is_known_article(article, set()):
                            results.append(article)

                except Exception as error:
                    logger.error(f"Steam fetch error: {error}")

        return results

    async def fetch_news(self) -> List[NewsArticle]:
        """
        Fetch news from all sources (Steam, Pocketpair)
        
        Returns:
            List of NewsArticle dataclasses
        """
        results = []

        # ============================================
        # STEAM
        # ============================================

        seen_keys: set[str] = set()
        steam_news = await self.fetch_steam_news()

        for article in steam_news:
            if not self._is_known_article(article, seen_keys):
                results.append(article)

        # ============================================
        # POCKETPAIR
        # ============================================

        try:

            pocketpair_news = await self.pocketpair.fetch_news()

            for news in pocketpair_news:

                # Translate title if enabled
                if Config.TRANSLATION_ENABLED:
                    news.title = await self._translate(news.title)
                    news.summary = await self._translate(news.summary or "")

                if not self._is_known_article(news, seen_keys):
                    results.append(news)

        except Exception as error:
            logger.error(f"Pocketpair fetch error: {error}")

        return results

    def mark_as_sent(self, article: NewsArticle):
        """
        Mark an article as sent to Discord
        
        Args:
            article: Article that was sent to Discord
        """
        self.database.save_news_pending(
            guid=article.guid,
            title=article.title,
            url=article.url,
            published=article.published or "",
            source=article.source,
            category=article.category,
            summary=article.summary,
            image=article.image,
        )
        self.database.mark_as_sent(article.guid)
