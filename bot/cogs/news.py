import re
import logging

import discord
from discord.ext import commands, tasks
from datetime import datetime

logger = logging.getLogger("palworld_bot.news")


class NewsCog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.news_check.start()

    def cog_unload(self):

        self.news_check.cancel()

    # =========================================================
    # OUTILS
    # =========================================================

    def format_date(self, published):

        if not published:
            return "Non disponible"

        # Pocketpair : YYYY.MM.DD
        try:

            if re.match(
                r"^\d{4}\.\d{2}\.\d{2}$",
                published
            ):

                date = datetime.strptime(
                    published,
                    "%Y.%m.%d"
                )

                return date.strftime(
                    "%d/%m/%Y"
                )

        except Exception:
            pass

        return published

    def get_category_design(self, category):

        if category == "patch_notes":

            return {
                "color": discord.Color.green(),
                "emoji": "🔧",
                "label": "MISE À JOUR & CORRECTIF"
            }

        if category == "events":

            return {
                "color": discord.Color.gold(),
                "emoji": "🎁",
                "label": "ÉVÉNEMENT SPÉCIAL"
            }

        return {
            "color": discord.Color.blue(),
            "emoji": "📰",
            "label": "ACTUALITÉ PALWORLD"
        }

    def is_major_update(self, title):

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
    # CONSTRUCTION DE L'EMBED
    # =========================================================

    def build_news_embed(self, news):

        category = news.get(
            "category",
            "news"
        )

        design = self.get_category_design(
            category
        )

        emoji = design["emoji"]
        label = design["label"]
        color = design["color"]

        title = news.get(
            "title",
            "Actualité Palworld"
        )

        summary = news.get(
            "summary",
            ""
        )

        source = news.get(
            "source",
            "Inconnue"
        )

        published = news.get(
            "published",
            ""
        )

        url = news.get(
            "url",
            ""
        )

        image = news.get(
            "image",
            ""
        )

        # -----------------------------------------------------
        # DESCRIPTION
        # -----------------------------------------------------

        if summary:

            description = (
                f"**{label}**\n\n"
                f"{summary}"
            )

        else:

            description = (
                f"**{label}**\n\n"
                "Une nouvelle publication "
                "Palworld est disponible."
            )

        # -----------------------------------------------------
        # EMBED
        # -----------------------------------------------------

        embed = discord.Embed(
            title=f"{emoji} {title}",
            description=description,
            url=url if url else discord.Embed.Empty,
            color=color
        )

        # -----------------------------------------------------
        # IMAGE
        # -----------------------------------------------------

        if image:

            embed.set_image(
                url=image
            )

        # -----------------------------------------------------
        # INFORMATIONS
        # -----------------------------------------------------

        embed.add_field(
            name="📅 Date",
            value=self.format_date(
                published
            ),
            inline=True
        )

        embed.add_field(
            name="📰 Source",
            value=source,
            inline=True
        )

        # -----------------------------------------------------
        # FOOTER
        # -----------------------------------------------------

        embed.set_footer(
            text="Zaelos Palworld Bot"
        )

        return embed

    # =========================================================
    # BOUTON ARTICLE
    # =========================================================

    def build_news_view(self, news):

        url = news.get(
            "url",
            ""
        )

        view = discord.ui.View(
            timeout=None
        )

        if url:

            view.add_item(
                discord.ui.Button(
                    label="Lire l'article",
                    url=url,
                    emoji="🔗"
                )
            )

        return view

    # =========================================================
    # VERIFICATION AUTOMATIQUE
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
    # ENVOI DISCORD
    # =========================================================

    async def send_news(self, news):

        category = news.get(
            "category",
            "news"
        )

        channel_id_str = (
            self.bot.channels_config.get(
                category
            )
        )

        if not channel_id_str:

            channel_id_str = (
                self.bot.channels_config.get(
                    "news"
                )
            )

        if not channel_id_str:

            print(
                "⚠️ Aucun salon Discord configuré."
            )

            return False

        try:

            channel_id = int(
                channel_id_str
            )

        except ValueError:

            print(
                f"❌ ID de salon invalide : "
                f"{channel_id_str}"
            )

            return False

        channel = self.bot.get_channel(
            channel_id
        )

        if not channel:

            print(
                f"⚠️ Salon Discord "
                f"{channel_id_str} introuvable."
            )

            return False

        # -----------------------------------------------------
        # EMBED
        # -----------------------------------------------------

        embed = self.build_news_embed(
            news
        )

        # -----------------------------------------------------
        # BOUTON
        # -----------------------------------------------------

        view = self.build_news_view(
            news
        )

        # -----------------------------------------------------
        # MENTION GROSSE MISE À JOUR
        # -----------------------------------------------------

        content = None

        title = news.get(
            "title",
            ""
        )

        if self.is_major_update(
            title
        ):

            role_id = (
                self.bot.channels_config.get(
                    "palworld_role"
                )
            )

            if role_id:

                content = (
                    f"<@&{role_id}>"
                )

            else:

                print(
                    "📣 Grosse mise à jour détectée "
                    "(aucun rôle @Palworld configuré)."
                )

        # -----------------------------------------------------
        # ENVOI
        # -----------------------------------------------------

        try:

            await channel.send(
                content=content,
                embed=embed,
                view=view
            )

        except Exception as error:

            print(
            logger.error(
                f"Erreur envoi Discord: 

            return False

        # -----------------------------------------------------
        # ENREGISTREMENT
        # -----------------------------------------------------

        self.bot.news_service.mark_as_sent(
            news
        )

        print(
            f"🆕 Actualité envoyée : "
            f"{title}"
        )

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
