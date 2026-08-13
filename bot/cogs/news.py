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
                print("Aucune nouvelle actualité.")
                return

            for news in reversed(news_list):
                category = news.get("category", "news")
                channel_id_str = self.bot.channels_config.get(category)
                
                # Sécurité : si un salon spécifique n'est pas trouvé, on rabat sur "news"
                if not channel_id_str:
                    channel_id_str = self.bot.channels_config.get("news")
                
                if not channel_id_str:
                    print("⚠️ Aucun salon de destination configuré.")
                    return

                channel = self.bot.get_channel(int(channel_id_str))
                if not channel:
                    print(f"⚠️ Salon Discord {channel_id_str} introuvable.")
                    continue

                # Personnalisation de l'affichage selon la catégorie
                if category == "patch_notes":
                    color = discord.Color.green()
                    emoji = "🔧"
                    label = "Mise à jour & Correctif"
                elif category == "events":
                    color = discord.Color.gold()
                    emoji = "🎁"
                    label = "Événement spécial"
                else:
                    color = discord.Color.blue()
                    emoji = "📰"
                    label = "Actualité"

                embed = discord.Embed(
                    title=f"{emoji} {news['title']}",
                    url=news["url"],
                    description=f"Une nouvelle publication de type **{label}** est disponible !",
                    color=color,
                    timestamp=discord.utils.utcnow()
                )
                embed.set_footer(text=f"Source : {news['source']}")

                await channel.send(embed=embed)
                self.bot.news_service.mark_as_sent(news)
                print(f"🆕 {label} envoyée : {news['title']}")

        except Exception as error:
            print(f"❌ Erreur système News : {error}")

    @news_check.before_loop
    async def before_news_check(self):
        await self.bot.wait_until_ready()
        print("📰 Système automatique News prêt.")

    @commands.hybrid_command(name="news", description="Affiche les dernières actualités Palworld (test visuel).")
    async def news(self, ctx):
        news_list = await self.bot.news_service.fetch_news()
        if not news_list:
            await ctx.send("📰 Aucune nouvelle actualité disponible non-envoyée.")
            return

        for news in news_list[:3]:
            embed = discord.Embed(
                title=f"📰 {news['title']}",
                url=news["url"],
                color=discord.Color.blurple()
            )
            embed.set_footer(text=f"Catégorie détectée : {news.get('category')} | Source : {news['source']}")
            await ctx.send(embed=embed)
            self.bot.news_service.mark_as_sent(news)

async def setup(bot):
    await bot.add_cog(NewsCog(bot))
