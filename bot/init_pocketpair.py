import asyncio

from services.database import Database
from services.news_service import NewsService


async def main():

    database = Database()

    service = NewsService(
        database
    )

    await service.initialize_pocketpair()


asyncio.run(main())
