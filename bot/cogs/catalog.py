"""Discord commands for items and bosses."""

from discord.ext import commands

from services.catalog import CatalogService
from utils import EmbedBuilder


class CatalogCog(commands.Cog):
    """Expose local item and boss searches."""

    def __init__(self, bot):
        self.bot = bot
        self.catalog = CatalogService()

    @commands.hybrid_command(name="items", description="Recherche un objet Palworld.")
    async def items(self, ctx: commands.Context, recherche: str = ""):
        await ctx.defer()
        matches = self.catalog.search_items(recherche)
        if not matches:
            await ctx.send("Aucun objet ne correspond a cette recherche.")
            return
        if len(matches) == 1:
            await ctx.send(embed=EmbedBuilder.item_embed(matches[0]))
            return
        await ctx.send("**Objets trouves**\n" + "\n".join(
            f"`{item.id}` **{item.name}** | {item.category}" for item in matches
        ))

    @commands.hybrid_command(name="boss", description="Liste les boss Palworld.")
    async def boss(self, ctx: commands.Context, recherche: str = ""):
        await ctx.defer()
        matches = self.catalog.search_bosses(recherche)
        if not matches:
            await ctx.send("Aucun boss ne correspond a cette recherche.")
            return
        if len(matches) == 1:
            await ctx.send(embed=EmbedBuilder.boss_embed(matches[0]))
            return
        await ctx.send("**Boss trouves**\n" + "\n".join(
            f"`{boss.id}` **{boss.name}** | niveau {boss.level}" for boss in matches
        ))


async def setup(bot):
    await bot.add_cog(CatalogCog(bot))
