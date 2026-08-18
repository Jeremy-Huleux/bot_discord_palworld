import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import Config
from services.database import Database
from services.news_service import NewsService
from logger import logger


load_dotenv()

# Validate configuration
if not Config.validate():
    logger.error("Configuration validation failed")
    raise RuntimeError("Invalid configuration")


class PalworldBot(commands.Bot):
    """
    Main Discord bot class for Palworld
    Initializes services, loads cogs, and syncs commands
    Uses dependency injection for better testability
    """

    def __init__(self):

        intents = discord.Intents.default()

        super().__init__(
            command_prefix="!",
            intents=intents
        )

        # Initialize services with dependency injection
        self.database = Database()

        self.news_service = NewsService(
            self.database
        )


    async def setup_hook(self):

        try:
            await self.load_extension(
                "cogs.news"
            )
            logger.info("✅ Cog 'news' chargé")
        except Exception as error:
            logger.error(f"❌ Erreur chargement cog 'news': {error}")

        guild = discord.Object(
            id=Config.DISCORD_GUILD_ID
        )

        self.tree.copy_global_to(
            guild=guild
        )

        try:
            await self.tree.sync(
                guild=guild
            )
            logger.info("✅ Commandes Discord synchronisées")
        except Exception as error:
            logger.error(f"❌ Erreur synchronisation commandes: {error}")


    async def on_ready(self):

        logger.info("=" * 60)
        logger.info("🤖 PALWORLD BOT DÉMARRÉ AVEC SUCCÈS")
        logger.info(f"Connecté en tant que : {self.user}")
        logger.info(f"Serveur Discord ID : {Config.DISCORD_GUILD_ID}")
        logger.info("=" * 60)

        # Print configuration summary
        logger.info(Config.summary())


bot = PalworldBot()


@bot.tree.command(
    name="ping",
    description="Vérifie que le bot fonctionne."
)
async def ping(
    interaction: discord.Interaction
):

    await interaction.response.send_message(
        "🏓 Pong ! Le bot fonctionne !"
    )


bot.run(Config.DISCORD_TOKEN)
