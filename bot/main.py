import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

from services.database import Database
from services.news_service import NewsService
from logger import logger


load_dotenv()


TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")


if not TOKEN:
    logger.error("DISCORD_TOKEN n'est pas défini.")
    raise RuntimeError("DISCORD_TOKEN n'est pas défini.")

if not GUILD_ID:
    logger.error("DISCORD_GUILD_ID n'est pas défini.")
    raise RuntimeError("DISCORD_GUILD_ID n'est pas défini.")


GUILD_ID = int(GUILD_ID)


class PalworldBot(commands.Bot):

    def __init__(self):

        intents = discord.Intents.default()

        super().__init__(
            command_prefix="!",
            intents=intents
        )

        self.database = Database()

        self.news_service = NewsService(
            self.database
        )

        # ==========================================
        # CONFIGURATION DISCORD
        # ==========================================

        self.channels_config = {

            "patch_notes": os.getenv(
                "PATCH_NOTES_CHANNEL_ID"
            ),

            "news": os.getenv(
                "NEWS_CHANNEL_ID"
            ),

            "events": os.getenv(
                "EVENTS_CHANNEL_ID"
            ),

            "palworld_role": os.getenv(
                "PALWORLD_ROLE_ID"
            )
        }


    async def setup_hook(self):

        try:
            await self.load_extension(
                "cogs.news"
            )
            logger.info("✅ Cog 'news' chargé")
        except Exception as error:
            logger.error(f"❌ Erreur chargement cog 'news': {error}")

        guild = discord.Object(
            id=GUILD_ID
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
        logger.info(f"Serveur Discord ID : {GUILD_ID}")
        logger.info("=" * 60)


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


bot.run(TOKEN)
