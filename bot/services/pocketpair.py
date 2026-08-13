import aiohttp

from bs4 import BeautifulSoup
from urllib.parse import urljoin


POCKETPAIR_URL = (
    "https://www.pocketpair.jp/en/"
    "game-news/category_game/palworld-en/"
)


class PocketpairService:

    def __init__(self, database):

        self.database = database

    async def fetch_news(self):

        results = []

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(compatible; ZaelosPalworldBot/1.0)"
            )
        }

        try:

            async with aiohttp.ClientSession(
                headers=headers
            ) as session:

                async with session.get(
                    POCKETPAIR_URL,
                    timeout=aiohttp.ClientTimeout(
                        total=20
                    )
                ) as response:

                    if response.status != 200:

                        print(
                            f"❌ Pocketpair HTTP "
                            f"{response.status}"
                        )

                        return results

                    html = await response.text()

            soup = BeautifulSoup(
                html,
                "html.parser"
            )

            # -------------------------------------------------
            # On récupère uniquement les liens d'articles
            # situés dans la liste Palworld.
            # -------------------------------------------------

            articles = []

            for link in soup.find_all(
                "a",
                href=True
            ):

                href = link.get("href", "")

                url = urljoin(
                    POCKETPAIR_URL,
                    href
                )

                # Les vrais articles Pocketpair utilisent
                # /game-news/ dans leur URL.
                if "/game-news/" not in url:

                    continue

                # On ignore la page de catégorie elle-même.
                if "category_game" in url:

                    continue

                title = link.get_text(
                    " ",
                    strip=True
                )

                if not title:

                    continue

                articles.append(
                    {
                        "url": url,
                        "raw_title": title
                    }
                )

            # -------------------------------------------------
            # Nettoyage + extraction des informations
            # -------------------------------------------------

            for article in articles:

                raw_title = article["raw_title"]

                url = article["url"]

                parts = raw_title.split()

                category = None
                date = None

                # Catégories connues
                categories = [
                    "News",
                    "important notice",
                    "update",
                    "Event Information",
                    "Palworld",
                    "Pitch Your Game"
                ]

                # Extraction simple de la date
                for part in parts:

                    if (
                        len(part) == 10
                        and part[4] == "."
                        and part[7] == "."
                    ):

                        date = part

                        break

                # Détection de catégorie
                lowered = raw_title.lower()

                if "important notice" in lowered:

                    category = "important notice"

                elif "event information" in lowered:

                    category = "Event Information"

                elif "pitch your game" in lowered:

                    category = "Pitch Your Game"

                elif "update" in lowered:

                    category = "update"

                elif "news" in lowered:

                    category = "News"

                else:

                    category = "Palworld"

                # -------------------------------------------------
                # Nettoyage du titre
                # -------------------------------------------------

                title = raw_title

                for prefix in [
                    "important notice",
                    "Event Information",
                    "Pitch Your Game",
                    "News",
                    "update",
                    "Palworld"
                ]:

                    if title.lower().startswith(
                        prefix.lower()
                    ):

                        title = title[
                            len(prefix):
                        ].strip()

                if date and date in title:

                    title = title.replace(
                        date,
                        "",
                        1
                    ).strip()

                # -------------------------------------------------
                # On ignore Pitch Your Game
                # -------------------------------------------------

                if category == "Pitch Your Game":

                    continue

                # -------------------------------------------------
                # Identifiant unique
                # -------------------------------------------------

                guid = (
                    f"pocketpair:"
                    f"{url}"
                )

                if self.database.news_exists(
                    guid
                ):

                    continue

                results.append(
                    {
                        "guid": guid,
                        "title": title,
                        "url": url,
                        "published": date or "",
                        "source": "Pocketpair",
                        "category": category
                    }
                )

        except Exception as error:

            print(
                f"❌ Erreur Pocketpair : {error}"
            )

        return results
