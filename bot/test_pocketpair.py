import asyncio

from services.pocketpair import PocketpairService


class TestDatabase:

    def news_exists(self, guid):

        # Pour le test, aucun article n'est considéré
        # comme déjà enregistré.
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
        print(f"🔗 URL       : {article['url']}")

    print()
    print("=" * 70)
    print(
        f"{len(news)} articles détectés"
    )
    print("=" * 70)


asyncio.run(main())
