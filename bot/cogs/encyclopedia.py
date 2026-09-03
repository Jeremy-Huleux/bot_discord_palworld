"""Discord commands for the Pal encyclopedia."""

from discord.ext import commands

from services.pal_dex import PalDexService
from services.breeding import BreedingService
from utils import EmbedBuilder


class EncyclopediaCog(commands.Cog):
    """Expose Pal search commands."""

    def __init__(self, bot):
        self.bot = bot
        self.dex = PalDexService()
        self.breeding_service = BreedingService(self.dex.pals)

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

    @commands.hybrid_command(
        name="breeding",
        description="Calcule les resultats possibles de breeding.",
    )
    async def breeding(
        self,
        ctx: commands.Context,
        parent1: str,
        parent2: str,
    ):
        """Calculate possible offspring for two catalog Pals."""
        await ctx.defer()
        first = self.dex.search(parent1)
        second = self.dex.search(parent2)
        if not first or not second:
            await ctx.send("Parent introuvable dans l'encyclopedie locale.")
            return

        matches = self.breeding_service.calculate(first[0].name, second[0].name)
        if not matches:
            await ctx.send("Aucun resultat de breeding disponible.")
            return

        await ctx.send(
            "**Resultats possibles**\n" + "\n".join(
                f"- **{pal.name}** ({', '.join(pal.type)})"
                for pal in matches
            )
        )


async def setup(bot):
    """Load the encyclopedia cog."""
    await bot.add_cog(EncyclopediaCog(bot))
