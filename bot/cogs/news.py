import discord

from discord.ext import commands, tasks


class NewsCog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.news_check.start()

    def cog_unload(self):

        self.news_check.cancel()

    @tasks.loop(minutes=10)
    async def news_check(self):

        print("📰 Vérification des actualités Palworld...")

        try:

            news_list = await self.bot.news_service.fetch_news()

            if not news_list:

                print("📰 Aucune nouvelle actualité.")

                return

            channel_id = self.bot.news_channel_id

            if not channel_id:

                print(
                    "❌ NEWS_CHANNEL_ID n'est pas configuré."
                )

                return

            channel = self.bot.get_channel(
                int(channel_id)
            )

            if not channel:

                print(
                    f"❌ Salon Discord {channel_id} introuvable."
                )

                return

            # Vérification des permissions
            permissions = channel.permissions_for(
                channel.guild.me
            )

            print(
                f"🔎 Vérification permissions du salon : "
                f"#{channel.name}"
            )

            print(
                f"   Voir le salon       : {permissions.view_channel}"
            )

            print(
                f"   Envoyer messages    : {permissions.send_messages}"
            )

            print(
                f"   Intégrer liens      : {permissions.embed_links}"
            )

            print(
                f"   Lire historique     : {permissions.read_message_history}"
            )

            if not permissions.view_channel:

                print(
                    "❌ Le bot ne peut pas voir ce salon."
                )

                return

            if not permissions.send_messages:

                print(
                    "❌ Le bot ne peut pas envoyer de messages "
                    "dans ce salon."
                )

                return

            if not permissions.embed_links:

                print(
                    "❌ Le bot ne peut pas intégrer les liens "
                    "dans ce salon."
                )

                return

            for news in reversed(news_list):

                embed = discord.Embed(
                    title=f"📰 {news['title']}",
                    url=news["url"],
                    description=(
                        "Une nouvelle actualité Palworld "
                        "vient d'être publiée."
                    ),
                    timestamp=discord.utils.utcnow()
                )

                embed.set_footer(
                    text=f"Source : {news['source']}"
                )

                try:

                    await channel.send(
                        embed=embed
                    )

                    self.bot.news_service.mark_as_sent(
                        news
                    )

                    print(
                        f"🆕 Actualité envoyée : "
                        f"{news['title']}"
                    )

                except discord.Forbidden:

                    print(
                        "❌ Discord refuse l'envoi du message "
                        "dans le salon."
                    )

                    return

        except Exception as error:

            print(
                f"❌ Erreur système News : {error}"
            )

    @news_check.before_loop
    async def before_news_check(self):

        await self.bot.wait_until_ready()

        print(
            "📰 Système automatique News prêt."
        )

    @commands.hybrid_command(
        name="news",
        description="Affiche les dernières actualités Palworld."
    )
    async def news(self, ctx):

        news_list = await self.bot.news_service.fetch_news()

        if not news_list:

            await ctx.send(
                "📰 Aucune nouvelle actualité disponible."
            )

            return

        for news in news_list[:5]:

            embed = discord.Embed(
                title=f"📰 {news['title']}",
                url=news["url"],
                color=discord.Color.blue()
            )

            embed.set_footer(
                text=f"Source : {news['source']}"
            )

            await ctx.send(
                embed=embed
            )

            self.bot.news_service.mark_as_sent(
                news
            )


async def setup(bot):

    await bot.add_cog(
        NewsCog(bot)
    )
