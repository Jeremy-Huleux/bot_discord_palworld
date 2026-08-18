import re
import logging

import discord
from discord.ext import commands, tasks

from config import Config
from models import NewsArticle
from utils import EmbedBuilder, ViewBuilder, Formatter

logger = logging.getLogger("palworld_bot.news")


class NewsCog(commands.Cog):
    """
    Discord cog for news management
    Handles fetching, checking, and sending Palworld news to Discord channels
    """

    def __init__(self, bot):

        self.bot = bot
        self.news_check.start()

    def cog_unload(self):

        self.news_check.cancel()

    # =========================================================
    # UTILITIES
    # =========================================================

    def is_major_update(self, title: str) -> bool:
        """
        Check if an article title indicates a major update
        """
        title_lower = title.lower()

        major_keywords = [
            "major update",
            "major version",
            "official launch",
            "new version",
            "version 1.",
            "version 2.",
            "v1.",
            "v2.",
            "palworld 1.0",
            "palworld 2.0"
        ]

        return any(
            keyword in title_lower
            for keyword in major_keywords
        )

    # =========================================================
    # AUTOMATIC VERIFICATION
    # =========================================================

    @tasks.loop(minutes=5)
    async def news_check(self):

        logger.info("Vérification des actualités Palworld...")

        try:

            news_list = (
                await self.bot.news_service.fetch_news()
            )

            if not news_list:

                logger.debug("Aucune nouvelle actualité détectée")

                return

            logger.info(
                f"Détection de {len(news_list)} nouvelle(s) actualité(s)"
            )

            for news in reversed(news_list):

                await self.send_news(
                    news
                )

        except Exception as error:

            logger.error(
                f"Erreur système news: {error}"
            )

    # =========================================================
    # DISCORD SEND
    # =========================================================

    async def send_news(self, article: NewsArticle) -> bool:
        """
        Send a news article to Discord
        
        Args:
            article: NewsArticle dataclass
            
        Returns:
            True if sent successfully, False otherwise
        """
        channels_config = Config.get_channels_config()

        channel_id = (
            channels_config.get(article.category)
            or channels_config.get("news")
        )

        if not channel_id:
            logger.warning("No Discord channel configured for news")
            return False

        channel = self.bot.get_channel(channel_id)

        if not channel:
            logger.warning(f"Discord channel {channel_id} not found")
            return False

        # Build embed and view using builders
        embed = EmbedBuilder.news_embed(article)
        view = ViewBuilder.news_view(article)

        # Handle major update mentions
        content = None

        if self.is_major_update(article.title):
            palworld_role_id = channels_config.get("palworld_role")

            if palworld_role_id:
                content = f"<@&{palworld_role_id}>"

        # Send to Discord
        try:
            await channel.send(
                content=content,
                embed=embed,
                view=view
            )

        except Exception as error:
            logger.error(f"Discord send error: {error}")
            return False

        # Mark as sent in database
        self.bot.news_service.mark_as_sent(article.guid)

        logger.info(f"News sent: {article.title}")

        return True

    # =========================================================
    # AVANT LE LOOP
    # =========================================================

    @news_check.before_loop
    async def before_news_check(self):

        await self.bot.wait_until_ready()

        print(
            "📰 Système automatique News prêt."
        )

    # =========================================================
    # COMMANDE /NEWS
    # =========================================================

    @commands.hybrid_command(
        name="news",
        description=(
            "Affiche les dernières actualités "
            "Palworld."
        )
    )
    async def news(self, ctx):

        news_list = (
            await self.bot.news_service.fetch_news()
        )

        if not news_list:

            await ctx.send(
                "📰 Aucune nouvelle actualité "
                "disponible non-envoyée."
            )

            return

        for news in news_list[:3]:

            await self.send_news(
                news
            )

    # =========================================================
    # COMMANDE /TESTNEWS
    # =========================================================

    @commands.hybrid_command(
        name="testnews",
        description=(
            "Envoie un embed de test du système News."
        )
    )
    async def testnews(self, ctx):

        test_news = {

            "guid": "test:discord-embed",

            "title": (
                "Palworld 1.0 est disponible "
                "MAINTENANT !"
            ),

            "summary": (
                "Palworld quitte officiellement "
                "l'accès anticipé avec la sortie "
                "de la version 1.0 !"
            ),

            "image": (
                "https://cdn.getshifter.co/"
                "4cf51f4bd2c52300046e22057221adc8e88f21a9/"
                "uploads/2026/07/"
                "JP_40MSS7-1200x630.png"
            ),

            "url": (
                "https://www.pocketpair.jp/en/"
                "game-news/"
                "%e3%80%8a%e5%b9%bb%e5%85%bd%e5%b8%95%e9%b2%81"
                "%e3%80%8b1-0%e6%ad%a3%e5%bc%8f%e7%89%88%e7%8e%b0"
                "%e5%b7%b2%e4%b8%8a%e7%ba%bf%ef%bc%81/"
            ),

            "published": "2026.07.10",

            "source": "Pocketpair",

            "category": "patch_notes"
        }

        embed = self.build_news_embed(
            test_news
        )

        view = self.build_news_view(
            test_news
        )

        role_id = (
            self.bot.channels_config.get(
                "palworld_role"
            )
        )

        content = None

        if role_id:

            content = (
                f"<@&{role_id}>"
            )

        await ctx.send(
            content=content,
            embed=embed,
            view=view
        )

        print(
            "🧪 Embed News de test envoyé."
        )


async def setup(bot):

    await bot.add_cog(
        NewsCog(bot)
    )
