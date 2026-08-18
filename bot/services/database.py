import sqlite3
from pathlib import Path
from typing import List
from config import Config
from models import NewsArticle


class Database:

    def __init__(self, db_path: Path = None):
        """
        Initialize database connection
        
        Args:
            db_path: Path to database file (uses Config.DATABASE_PATH if None)
        """
        self.db_path = db_path or Config.DATABASE_PATH

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            str(self.db_path),
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
                category TEXT DEFAULT 'news',
                summary TEXT,
                image TEXT,
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
            
        Nouvelles colonnes :
            category: Type de news (news, patch_notes, events)
            summary: Résumé de l'article
            image: Image associée à l'article
        """

        columns = self.connection.execute(
            "PRAGMA table_info(news)"
        ).fetchall()

        column_names = {
            column["name"]
            for column in columns
        }

        # Ajouter sent_at si manquante
        if "sent_at" not in column_names:
            self.connection.execute(
                "ALTER TABLE news ADD COLUMN sent_at TEXT"
            )
            self.connection.commit()

        # Ajouter category si manquante
        if "category" not in column_names:
            self.connection.execute(
                "ALTER TABLE news ADD COLUMN category TEXT DEFAULT 'news'"
            )
            self.connection.commit()

        # Ajouter summary si manquante
        if "summary" not in column_names:
            self.connection.execute(
                "ALTER TABLE news ADD COLUMN summary TEXT"
            )
            self.connection.commit()

        # Ajouter image si manquante
        if "image" not in column_names:
            self.connection.execute(
                "ALTER TABLE news ADD COLUMN image TEXT"
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
        source: str,
        category: str = "news",
        summary: str = None,
        image: str = None
    ):
        """
        Save a pending news article
        
        Args:
            guid: Unique article identifier
            title: Article title
            url: Article URL
            published: Publication date
            source: News source (Steam, Pocketpair, etc.)
            category: news, patch_notes, or events
            summary: Article summary/preview text
            image: Image URL
        """
        self.connection.execute(
            """
            INSERT OR IGNORE INTO news
            (
                guid,
                title,
                url,
                published,
                source,
                category,
                summary,
                image,
                sent_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL)
            """,
            (
                guid,
                title,
                url,
                published,
                source,
                category,
                summary,
                image
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

    def get_unsent_news(self) -> List[NewsArticle]:
        """
        Get all unsent news articles
        
        Returns:
            List of NewsArticle dataclasses
        """
        cursor = self.connection.execute(
            """
            SELECT *
            FROM news
            WHERE sent_at IS NULL
            ORDER BY id ASC
            """
        )

        news_list = []
        for row in cursor.fetchall():
            news_list.append(self._row_to_article(row))

        return news_list

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _row_to_article(self, row) -> NewsArticle:
        """
        Convert database row to NewsArticle dataclass
        
        Args:
            row: sqlite3.Row object
            
        Returns:
            NewsArticle dataclass
        """
        return NewsArticle(
            guid=row["guid"],
            title=row["title"],
            url=row["url"],
            published=row.get("published"),
            source=row["source"],
            category=row.get("category", "news"),
            summary=row.get("summary", ""),
            image=row.get("image"),
            sent_at=row.get("sent_at"),
        )
