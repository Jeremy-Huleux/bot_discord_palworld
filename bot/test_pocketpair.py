import asyncio

from services.pocketpair import PocketpairService


class TestDatabase:

    def news_exists(self, guid):
        return False


async def main():

    database = TestDatabase()

    service = PocketpairService(
        database=database
    )

    news = await service.fetch_news()

    print()
    print("=" * 70)
    print("POCKETPAIR - RESULTAT DU PARSER")
    print("=" * 70)

    for article in news:

        print()
        print(f"📂 Catégorie : {article['category']}")
        print(f"📅 Date      : {article['published']}")
        print(f"📰 Titre     : {article['title']}")
        print(f"📝 Résumé    : {article['summary'][:200]}")
        print(f"🖼️ Image     : {article['image']}")
        print(f"🔗 URL       : {article['url']}")

    print()
    print("=" * 70)
    print(
        f"{len(news)} articles détectés"
    )
    print("=" * 70)


asyncio.run(main())
