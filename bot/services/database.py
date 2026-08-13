import sqlite3
from pathlib import Path


DATABASE_PATH = Path("/app/data/news.db")


class Database:

    def __init__(self):
        DATABASE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            DATABASE_PATH,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row

        self.create_tables()

    def create_tables(self):

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guid TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                published TEXT,
                source TEXT NOT NULL,
                sent_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.connection.commit()

    def news_exists(self, guid: str) -> bool:

        cursor = self.connection.execute(
            "SELECT 1 FROM news WHERE guid = ? LIMIT 1",
            (guid,)
        )

        return cursor.fetchone() is not None

    def save_news(
        self,
        guid: str,
        title: str,
        url: str,
        published: str,
        source: str
    ):

        self.connection.execute("""
            INSERT OR IGNORE INTO news
            (guid, title, url, published, source)
            VALUES (?, ?, ?, ?, ?)
        """, (
            guid,
            title,
            url,
            published,
            source
        ))

        self.connection.commit()
