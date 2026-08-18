import re
import logging
import asyncio
import aiohttp

from bs4 import BeautifulSoup
from urllib.parse import urljoin

logger = logging.getLogger("palworld_bot.pocketpair")


POCKETPAIR_URL = (
    "https://www.pocketpair.jp/en/"
    "game-news/category_game/palworld-en/"
)


class PocketpairService:

    def __init__(self, database):
        self.database = database

    async def extract_article_details(
        self,
        session,
        url,
        raw_title="",
        title="",
        published="",
        category=""
    ):
        try:

            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=20)
            ) as response:

                if response.status != 200:

                    logger.warning(
                        f"Pocketpair article HTTP {response.status}: {url}"
                    )

                    return "", ""

                html = await response.text()

            soup = BeautifulSoup(
                html,
                "html.parser"
            )

            # =================================================
            # IMAGE
            # =================================================

            image_url = ""

            og_image = soup.find(
                "meta",
                property="og:image"
            )

            if og_image:

                image_url = og_image.get(
                    "content",
                    ""
                )

            # Fallback : première image
            if not image_url:

                img = soup.find("img")

                if img:

                    image_url = img.get(
                        "src",
                        ""
                    )

            if image_url:

                image_url = urljoin(
                    url,
                    image_url
                )

            # =================================================
            # CONTENU
            # =================================================

#debut modif

            # =========================================================
            # EXTRACTION DU CONTENU DE L'ARTICLE
            # =========================================================

            content = ""

            selectors = [
                "article",
                ".entry-content",
                ".post-content",
                ".article-content",
                "main"
            ]

            for selector in selectors:

                element = soup.select_one(selector)

                if not element:
                    continue

                # -----------------------------------------------------
                # Supprimer les éléments qui ne font pas partie
                # du contenu de l'article
                # -----------------------------------------------------

                for unwanted in element.select(
                    "nav, header, footer, script, style, "
                    ".breadcrumb, .breadcrumbs, "
                    ".share, .social, .related, "
                    ".comments, .comment, "
                    ".author, .post-meta"
                ):
                    unwanted.decompose()

                # -----------------------------------------------------
                # Récupération du texte complet
                # -----------------------------------------------------

                text = element.get_text(
                    " ",
                    strip=True
                )

                # -----------------------------------------------------
                # Nettoyage
                # -----------------------------------------------------

                text = re.sub(
                    r"\s+",
                    " ",
                    text
                ).strip()

                # Supprimer les URLs
                text = re.sub(
                    r"https?://\S+",
                    "",
                    text
                )

                text = re.sub(
                    r"\s+",
                    " ",
                    text
                ).strip()

                # -----------------------------------------------------
                # Retirer les informations de l'en-tête de l'article
                # -----------------------------------------------------

                # Date
                if published:
                    text = text.replace(
                        published,
                        "",
                        1
                    )

                # Catégorie
                category_texts = [
                    "important notice",
                    "event information",
                    "pitch your game",
                    "update",
                    "news"
                ]

                for category_text in category_texts:

                    text = re.sub(
                        rf"^\s*{re.escape(category_text)}\s*",
                        "",
                        text,
                        flags=re.IGNORECASE
                    )

                # Titre
                if raw_title:

                    cleaned_raw_title = re.sub(
                        r"\s+",
                        " ",
                        raw_title
                    ).strip()

                    if cleaned_raw_title:

                        text = text.replace(
                            cleaned_raw_title,
                            "",
                            1
                        ).strip()

                # -----------------------------------------------------
                # Nettoyage final
                # -----------------------------------------------------

                text = re.sub(
                    r"\s+",
                    " ",
                    text
                ).strip()

                if len(text) > 30:

                    content = text
                    break


            # =========================================================
            # FALLBACK
            # =========================================================

            if not content:

                element = soup.select_one("main")

                if element:

                    content = element.get_text(
                        " ",
                        strip=True
                    )

                    content = re.sub(
                        r"\s+",
                        " ",
                        content
                    ).strip()


            # =========================================================
            # LIMITATION DU RÉSUMÉ
            # =========================================================

            if len(content) > 500:

                content = content[:500].rsplit(
                    " ",
                    1
                )[0] + "..."

#fin modif

            # Nettoyage
            content = re.sub(
                r"\s+",
                " ",
                content
            ).strip()

#debut modif 2

            # =================================================
            # SUPPRESSION DES INFORMATIONS DE HEADER
            # =================================================

            if published := re.search(
                r"\b20\d{2}\.\d{2}\.\d{2}\b",
                content
            ):

                content = content[
                    published.end():
                ].strip()

            # Retirer les catégories affichées avant le contenu
            content = re.sub(
                r"^(News|Update|Important Notice|"
                r"Event Information)\s+",
                "",
                content,
                flags=re.IGNORECASE
            )

            # Retirer le titre s'il est répété au début

            title_text = title

            if title_text and content.lower().startswith(
                title_text.lower()
            ):

                content = content[
                    len(title_text):
                ].strip()

#fin modif 2

            # Éviter les textes énormes
            if len(content) > 500:

                content = (
                    content[:500]
                    .rsplit(" ", 1)[0]
                    + "..."
                )

            return content, image_url

        except Exception as error:

            logger.error(
                f"Erreur lecture article Pocketpair: {error}"
            )

            return "", ""

    async def fetch_news(self):

        results = []

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(compatible; ZaelosPalworldBot/1.0)"
            )
        }

        try:

            # =================================================
            # UNE SEULE SESSION POUR TOUTE LA REQUÊTE
            # =================================================

            async with aiohttp.ClientSession(
                headers=headers
            ) as session:

                # =============================================
                # PAGE DES NEWS
                # =============================================

                async with session.get(
                    POCKETPAIR_URL,
                    timeout=aiohttp.ClientTimeout(
                        total=20
                    )
                ) as response:

                    if response.status != 200:

                        print(
                        logger.error(
                            f"Pocketpair HTTP 

                        return results

                    html = await response.text()

                soup = BeautifulSoup(
                    html,
                    "html.parser"
                )

                seen_urls = set()

                # =============================================
                # PARCOURS DES ARTICLES
                # =============================================

                for link in soup.find_all(
                    "a",
                    href=True
                ):

                    href = link.get(
                        "href",
                        ""
                    )

                    url = urljoin(
                        POCKETPAIR_URL,
                        href
                    )

                    # -----------------------------------------
                    # URL ARTICLE
                    # -----------------------------------------

                    if "/game-news/" not in url:
                        continue

                    if url.rstrip("/") == (
                        "https://www.pocketpair.jp/en/game-news"
                    ):
                        continue

                    if "category_game" in url:
                        continue

                    if url in seen_urls:
                        continue

                    seen_urls.add(url)

                    # -----------------------------------------
                    # TITRE
                    # -----------------------------------------

                    raw_title = link.get_text(
                        " ",
                        strip=True
                    )

                    if not raw_title:
                        continue

                    if raw_title.lower() in {
                        "game news",
                        "all",
                        "palworld",
                        "palworld: palfarm"
                    }:
                        continue

                    # -----------------------------------------
                    # DATE
                    # -----------------------------------------

                    date_match = re.search(
                        r"\b(20\d{2}\.\d{2}\.\d{2})\b",
                        raw_title
                    )

                    published = ""

                    if date_match:

                        published = (
                            date_match.group(1)
                        )

                    # -----------------------------------------
                    # CATEGORIE
                    # -----------------------------------------

                    category = "Palworld"

                    lowered = raw_title.lower()

                    if "important notice" in lowered:

                        category = "important notice"

                    elif "event information" in lowered:

                        category = "Event Information"

                    elif "pitch your game" in lowered:

                        category = "Pitch Your Game"

                    elif re.search(
                        r"\bupdate\b",
                        lowered
                    ):

                        category = "update"

                    elif re.search(
                        r"\bnews\b",
                        lowered
                    ):

                        category = "News"

                    # -----------------------------------------
                    # NETTOYAGE TITRE
                    # -----------------------------------------

                    title = raw_title

                    prefixes = [
                        "important notice",
                        "event information",
                        "pitch your game",
                        "update",
                        "news",
                        "palworld"
                    ]

                    for prefix in prefixes:

                        title = re.sub(
                            rf"^\s*{re.escape(prefix)}\s*",
                            "",
                            title,
                            flags=re.IGNORECASE
                        )

                    if published:

                        title = title.replace(
                            published,
                            "",
                            1
                        )

                    title = re.sub(
                        r"\s+",
                        " ",
                        title
                    ).strip()

                    title = title.strip(
                        ":-–—| "
                    )

                    if not title:
                        continue

                    # -----------------------------------------
                    # IGNORER PITCH YOUR GAME
                    # -----------------------------------------

                    if category == "Pitch Your Game":
                        continue

                    # -----------------------------------------
                    # GUID
                    # -----------------------------------------

                    guid = (
                        f"pocketpair:{url}"
                    )

                    if self.database.news_exists(
                        guid
                    ):
                        continue

                    # =========================================
                    # ARTICLE
                    # =========================================


                    print(
                    logger.debug(
                        f"Lecture article Pocketpair: 

                    summary, image = (
                        await self.extract_article_details(
                            session,
                            url,
                            raw_title,
                            title,
                            published,
                            category
                        )
                    )

                    results.append(
                        {
                            "guid": guid,
                            "title": title,
                            "summary": summary,
                            "image": image,
                            "url": url,
                            "published": published,
                            "source": "Pocketpair",
                            "category": category
                        }
                    )

                    # Petite pause pour éviter de spammer
                    await asyncio.sleep(0.3)

        except Exception as error:

            print(
            logger.error(
                f"Erreur Pocketpair: 

        return results
