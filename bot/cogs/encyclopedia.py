"""Discord commands for the Pal encyclopedia."""

from discord.ext import commands

from services.pal_dex import PalDexService
from utils import EmbedBuilder


class EncyclopediaCog(commands.Cog):
    """Expose Pal search commands."""

    def __init__(self, bot):
        self.bot = bot
        self.dex = PalDexService()

    @commands.hybrid_command(
        name="pals",
        description="Recherche un Pal dans l'encyclopedie.",
    )
    async def pals(self, ctx: commands.Context, recherche: str = ""):
        """Search and display matching Pals."""
        await ctx.defer()
        matches = self.dex.search(recherche)

        if not matches:
            await ctx.send("Aucun Pal ne correspond a cette recherche.")
            return

        if len(matches) == 1:
            await ctx.send(embed=EmbedBuilder.pal_embed(matches[0]))
            return

        results = "\n".join(
            f"`{pal.id}` **{pal.name}** | {', '.join(pal.type)}"
            for pal in matches
        )
        await ctx.send(f"**Pals trouves**\n{results}")


async def setup(bot):
    """Load the encyclopedia cog."""
    await bot.add_cog(EncyclopediaCog(bot))
