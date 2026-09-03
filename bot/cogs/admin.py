"""Administrative Discord commands."""

from discord.ext import commands

from config import Config
from services.backup import BackupService


class AdminCog(commands.Cog):
    """Protected configuration and backup commands."""

    def __init__(self, bot):
        self.bot = bot
        self.backup = BackupService(Config.DATABASE_PATH)

    @commands.hybrid_group(name="admin", description="Commandes d'administration.")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def admin(self, ctx: commands.Context):
        """Administrative command group."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Utilisez `/admin config` ou `/admin backup`.")

    @admin.command(name="config", description="Affiche la configuration publique.")
    async def config(self, ctx: commands.Context):
        """Display safe configuration details."""
        await ctx.send(f"```text\n{Config.summary().strip()}\n```")

    @admin.command(name="backup", description="Sauvegarde la base des actualités.")
    async def backup_database(self, ctx: commands.Context):
        """Create a timestamped database backup."""
        try:
            backup_path = self.backup.create_backup()
        except FileNotFoundError:
            await ctx.send("Impossible de sauvegarder: base de données absente.")
            return

        await ctx.send(f"Sauvegarde créée: `{backup_path.name}`")

    @config.error
    @backup_database.error
    async def admin_command_error(self, ctx: commands.Context, error):
        """Return a useful response for permission and command errors."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Cette commande est réservée aux administrateurs.")
            return
        raise error


async def setup(bot):
    """Load the administration cog."""
    await bot.add_cog(AdminCog(bot))
