"""Discord commands for Palworld server monitoring."""

import discord
from discord.ext import commands

from services.server_monitor import ServerMonitorService
from utils import EmbedBuilder, Formatter


class ServerCog(commands.Cog):
    """Expose Palworld server status and player list commands."""

    def __init__(self, bot):
        self.bot = bot
        self.monitor = ServerMonitorService()

    @commands.hybrid_command(
        name="server",
        description="Affiche le statut du serveur Palworld.",
    )
    async def server(self, ctx: commands.Context):
        """Display server connectivity, players, version and uptime."""
        await ctx.defer()

        if not self.monitor.configured:
            await ctx.send(
                "Le serveur Palworld n'est pas configure. "
                "Definissez PALWORLD_API_URL et PALWORLD_ADMIN_PASSWORD dans .env."
            )
            return

        status = await self.monitor.get_status()
        embed = EmbedBuilder.server_status_embed(status)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="players",
        description="Liste les joueurs connectes au serveur Palworld.",
    )
    async def players(self, ctx: commands.Context):
        """Display currently connected players."""
        await ctx.defer()

        if not self.monitor.configured:
            await ctx.send(
                "Le serveur Palworld n'est pas configure. "
                "Definissez PALWORLD_API_URL et PALWORLD_ADMIN_PASSWORD dans .env."
            )
            return

        try:
            players = await self.monitor.get_players()
        except Exception:
            await ctx.send("Impossible de joindre le serveur Palworld.")
            return

        if not players:
            await ctx.send("Aucun joueur connecte actuellement.")
            return

        description = "\n".join(
            f"{index}. **{player.name}**"
            for index, player in enumerate(players, start=1)
        )
        embed = discord.Embed(
            title=f"Joueurs connectes ({len(players)})",
            description=description,
            color=discord.Color.blue(),
        )
        embed.set_footer(text="Zaelos Palworld Bot")
        await ctx.send(embed=embed)


async def setup(bot):
    """Load the server monitoring cog."""
    await bot.add_cog(ServerCog(bot))
