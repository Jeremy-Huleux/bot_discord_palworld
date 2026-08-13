import aiohttp
import feedparser

from datetime import datetime, timezone


class NewsService:

    def __init__(self, database):

        self.database = database

        self.feeds = [
            {
                "name": "Steam",
                "url": "https://store.steampowered.com/feeds/news/app/1623730/?l=french"
            }
        ]

    async def fetch_news(self):

        results = []

        async with aiohttp.ClientSession() as session:

            for feed_info in self.feeds:

                try:

                    async with session.get(
                        feed_info["url"],
                        timeout=aiohttp.ClientTimeout(total=15)
                    ) as response:

                        if response.status != 200:
                            print(
                                f"Erreur RSS {feed_info['name']} : "
                                f"{response.status}"
                            )
                            continue

                        content = await response.text()

                    feed = feedparser.parse(content)

                    for entry in feed.entries:

                        guid = entry.get(
                            "id",
                            entry.get("link")
                        )

                        if not guid:
                            continue

                        if self.database.news_exists(guid):
                            continue

                        news = {
                            "guid": guid,
                            "title": entry.get(
                                "title",
                                "Sans titre"
                            ),
                            "url": entry.get(
                                "link",
                                ""
                            ),
                            "published": entry.get(
                                "published",
                                ""
                            ),
                            "source": feed_info["name"]
                        }

                        results.append(news)

                except Exception as error:

                    print(
                        f"Erreur récupération "
                        f"{feed_info['name']} : {error}"
                    )

        return results

    def mark_as_sent(self, news):

        self.database.save_news(
            guid=news["guid"],
            title=news["title"],
            url=news["url"],
            published=news["published"],
            source=news["source"]
        )
