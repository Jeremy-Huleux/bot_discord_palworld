import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from services.database import Database
from services.news_service import NewsService

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN n'est pas défini.")
if not GUILD_ID:
    raise RuntimeError("DISCORD_GUILD_ID n'est pas défini.")

GUILD_ID = int(GUILD_ID)

class PalworldBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

        self.database = Database()
        self.news_service = NewsService(self.database)

        # Configuration des salons cibles
        self.channels_config = {
            "patch_notes": os.getenv("PATCH_NOTES_CHANNEL_ID"),
            "news": os.getenv("NEWS_CHANNEL_ID"),
            "events": os.getenv("EVENTS_CHANNEL_ID")
        }

    async def setup_hook(self):
        await self.load_extension("cogs.news")
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print("Commandes Discord synchronisées.")

    async def on_ready(self):
        print("=" * 50)
        print("🤖 Palworld Bot démarré")
        print(f"Connecté en tant que : {self.user}")
        print(f"Serveur Discord ID : {GUILD_ID}")
        print("=" * 50)

bot = PalworldBot()

@bot.tree.command(name="ping", description="Vérifie que le bot fonctionne.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong ! Le bot fonctionne !")

bot.run(TOKEN)
