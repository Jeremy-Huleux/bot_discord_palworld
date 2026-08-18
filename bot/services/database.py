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
        self.migrate_tables()

    def create_tables(self):

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guid TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                published TEXT,
                source TEXT NOT NULL,
                sent_at TEXT
            )
        """)

        self.connection.commit()

    def migrate_tables(self):

        """
        Migration de l'ancienne base.

        Avant :
            sent_at TEXT DEFAULT CURRENT_TIMESTAMP

        Maintenant :
            sent_at NULL = connu mais pas encore envoyé
            sent_at rempli = envoyé
        """

        columns = self.connection.execute(
            "PRAGMA table_info(news)"
        ).fetchall()

        column_names = {
            column["name"]
            for column in columns
        }

        if "sent_at" not in column_names:

            self.connection.execute(
                "ALTER TABLE news ADD COLUMN sent_at TEXT"
            )

            self.connection.commit()

    # ---------------------------------------------------------
    # Vérifie si une news est déjà connue
    # ---------------------------------------------------------

    def news_exists(self, guid: str) -> bool:

        cursor = self.connection.execute(
            """
            SELECT 1
            FROM news
            WHERE guid = ?
            LIMIT 1
            """,
            (guid,)
        )

        return cursor.fetchone() is not None

    # ---------------------------------------------------------
    # Vérifie si une news est connue via son URL
    # ---------------------------------------------------------

    def news_url_exists(self, url: str) -> bool:

        if not url:
            return False

        cursor = self.connection.execute(
            """
            SELECT 1
            FROM news
            WHERE url = ?
            LIMIT 1
            """,
            (url,)
        )

        return cursor.fetchone() is not None

    # ---------------------------------------------------------
    # Sauvegarde une news comme NON envoyée
    # ---------------------------------------------------------

    def save_news_pending(
        self,
        guid: str,
        title: str,
        url: str,
        published: str,
        source: str
    ):

        self.connection.execute(
            """
            INSERT OR IGNORE INTO news
            (
                guid,
                title,
                url,
                published,
                source,
                sent_at
            )
            VALUES (?, ?, ?, ?, ?, NULL)
            """,
            (
                guid,
                title,
                url,
                published,
                source
            )
        )

        self.connection.commit()

    # ---------------------------------------------------------
    # Marque une news comme envoyée
    # ---------------------------------------------------------

    def mark_as_sent(self, guid: str):

        self.connection.execute(
            """
            UPDATE news
            SET sent_at = CURRENT_TIMESTAMP
            WHERE guid = ?
            """,
            (guid,)
        )

        self.connection.commit()

    # ---------------------------------------------------------
    # Récupère les news non envoyées
    # ---------------------------------------------------------

    def get_unsent_news(self):

        cursor = self.connection.execute(
            """
            SELECT *
            FROM news
            WHERE sent_at IS NULL
            ORDER BY id ASC
            """
        )

        return cursor.fetchall()
