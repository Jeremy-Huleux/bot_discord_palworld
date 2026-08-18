"""
Utilities for building Discord UI components (Embeds, Views, Buttons)
"""

import discord
from typing import Optional, List
from models import NewsArticle, Pal, Item, Boss, ServerStatus, Player


class EmbedBuilder:
    """Helper class to build Discord Embeds"""

    @staticmethod
    def news_embed(article: NewsArticle) -> discord.Embed:
        """
        Build a news article embed
        """

        # Category design
        category_design = {
            "patch_notes": {
                "color": discord.Color.green(),
                "emoji": "🔧",
                "label": "MISE À JOUR & CORRECTIF",
            },
            "events": {
                "color": discord.Color.gold(),
                "emoji": "🎁",
                "label": "ÉVÉNEMENT SPÉCIAL",
            },
        }

        design = category_design.get(
            article.category,
            {
                "color": discord.Color.blue(),
                "emoji": "📰",
                "label": "ACTUALITÉ PALWORLD",
            },
        )

        emoji = design["emoji"]
        label = design["label"]
        color = design["color"]

        # Build description
        description = (
            f"**{label}**\n\n{article.summary}"
            if article.summary
            else f"**{label}**\n\nUne nouvelle publication Palworld est disponible."
        )

        # Create embed
        embed = discord.Embed(
            title=f"{emoji} {article.title}",
            description=description,
            url=article.url if article.url else discord.Embed.Empty,
            color=color,
        )

        # Add image if available
        if article.image:
            embed.set_image(url=article.image)

        # Add fields
        embed.add_field(
            name="📅 Date",
            value=article.published or "Non disponible",
            inline=True,
        )

        embed.add_field(
            name="📰 Source",
            value=article.source,
            inline=True,
        )

        # Footer
        embed.set_footer(text="Zaelos Palworld Bot")

        return embed

    @staticmethod
    def pal_embed(pal: Pal) -> discord.Embed:
        """Build a Pal Dex embed (future)"""

        embed = discord.Embed(
            title=f"🐾 {pal.name} ({pal.name_en})",
            description=pal.description or "No description available",
            color=discord.Color.purple(),
        )

        if pal.image:
            embed.set_thumbnail(url=pal.image)

        # Stats
        stats = (
            f"**HP:** {pal.hp}\n"
            f"**ATK:** {pal.attack}\n"
            f"**DEF:** {pal.defense}\n"
            f"**SP.ATK:** {pal.sp_atk}\n"
            f"**SP.DEF:** {pal.sp_def}\n"
            f"**SPD:** {pal.speed}"
        )

        embed.add_field(name="📊 Stats", value=stats, inline=True)

        if pal.type:
            embed.add_field(name="🏷️ Type", value=" / ".join(pal.type), inline=True)

        if pal.partner_skill:
            embed.add_field(
                name="🤝 Partner Skill", value=pal.partner_skill, inline=False
            )

        if pal.drops:
            embed.add_field(name="💧 Drops", value=", ".join(pal.drops), inline=False)

        return embed

    @staticmethod
    def server_status_embed(status: ServerStatus) -> discord.Embed:
        """Build a server status embed (future)"""

        color = discord.Color.green() if status.is_online else discord.Color.red()
        emoji = "🟢" if status.is_online else "🔴"

        embed = discord.Embed(
            title=f"{emoji} Statut du Serveur Palworld",
            color=color,
        )

        state = "EN LIGNE ✅" if status.is_online else "HORS LIGNE ❌"
        embed.add_field(name="État", value=state, inline=False)

        embed.add_field(
            name="👥 Joueurs",
            value=f"{status.player_count} / {status.max_players}",
            inline=True,
        )

        embed.add_field(
            name="⏱️ Réponse", value=f"{status.response_time:.0f}ms", inline=True
        )

        embed.add_field(name="📌 Version", value=status.version or "Unknown", inline=True)

        if status.last_check:
            embed.add_field(name="🕐 Dernier check", value=status.last_check, inline=True)

        return embed


class ViewBuilder:
    """Helper class to build Discord Views (Buttons, Menus)"""

    @staticmethod
    def news_view(article: NewsArticle) -> discord.ui.View:
        """Build a view with a link button for news"""

        view = discord.ui.View(timeout=None)

        if article.url:
            view.add_item(
                discord.ui.Button(
                    label="Lire l'article",
                    url=article.url,
                    emoji="🔗",
                )
            )

        return view

    @staticmethod
    def paginated_view() -> discord.ui.View:
        """Build a view with pagination buttons (future)"""

        view = discord.ui.View()

        @discord.ui.button(label="⬅️ Précédent", style=discord.ButtonStyle.primary)
        async def previous_button(
            interaction: discord.Interaction, button: discord.ui.Button
        ):
            # To be implemented
            await interaction.response.defer()

        @discord.ui.button(label="Suivant ➡️", style=discord.ButtonStyle.primary)
        async def next_button(
            interaction: discord.Interaction, button: discord.ui.Button
        ):
            # To be implemented
            await interaction.response.defer()

        return view


class Formatter:
    """Helper class for text formatting"""

    @staticmethod
    def format_date(date_str: Optional[str]) -> str:
        """
        Format date string
        Supports Pocketpair format (YYYY.MM.DD) and ISO format
        """

        if not date_str:
            return "Non disponible"

        import re
        from datetime import datetime

        # Pocketpair format: YYYY.MM.DD
        if re.match(r"^\d{4}\.\d{2}\.\d{2}$", date_str):
            try:
                date = datetime.strptime(date_str, "%Y.%m.%d")
                return date.strftime("%d/%m/%Y")
            except ValueError:
                return date_str

        # ISO format
        if "T" in date_str:
            try:
                date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                return date.strftime("%d/%m/%Y %H:%M")
            except ValueError:
                return date_str

        return date_str

    @staticmethod
    def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """Truncate text with ellipsis"""
        if len(text) <= max_length:
            return text
        return text[: max_length - len(suffix)] + suffix

    @staticmethod
    def format_uptime(seconds: float) -> str:
        """Format uptime in human-readable format"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)

        parts = []
        if days > 0:
            parts.append(f"{days}j")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")

        return " ".join(parts) or "0m"
