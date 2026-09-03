"""Local catalogs for Palworld items and bosses."""

import unicodedata
import json
from pathlib import Path
from typing import List, Optional

from models import Boss, Item


class CatalogService:
    """Search local item and boss catalogs."""

    def __init__(self, items: Optional[List[Item]] = None, bosses: Optional[List[Boss]] = None):
        self.items = items or self._load_items()
        self.bosses = bosses or self._load_bosses()

    @staticmethod
    def _load_data() -> dict:
        path = Path(__file__).parent.parent / "data" / "catalog.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {}

    @staticmethod
    def _load_items() -> List[Item]:
        data = CatalogService._load_data()
        return [Item(**item) for item in data.get("items", [])] or CatalogService._default_items()

    @staticmethod
    def _load_bosses() -> List[Boss]:
        data = CatalogService._load_data()
        return [Boss(**boss) for boss in data.get("bosses", [])] or CatalogService._default_bosses()

    def search_items(self, query: str) -> List[Item]:
        return self._search(self.items, query)

    def search_bosses(self, query: str = "") -> List[Boss]:
        return self._search(self.bosses, query)

    @classmethod
    def _search(cls, entries, query: str):
        normalized_query = cls._normalize(query)
        if not normalized_query:
            return entries[:10]
        return [
            entry for entry in entries
            if normalized_query in cls._normalize(entry.name)
            or normalized_query in cls._normalize(getattr(entry, "category", ""))
            or normalized_query in cls._normalize(getattr(entry, "location", ""))
        ][:10]

    @staticmethod
    def _normalize(value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value.lower())
        return "".join(char for char in normalized if not unicodedata.combining(char))

    @staticmethod
    def _default_items() -> List[Item]:
        return [
            Item(
                id=1,
                name="Pal Sphere",
                rarity=1,
                category="capture",
                description="Une sphere permettant de capturer les Pals.",
                materials=["Fragment de Paldium", "Bois", "Pierre"],
            ),
            Item(
                id=2,
                name="Mega Sphere",
                rarity=2,
                category="capture",
                description="Une sphere plus efficace pour capturer les Pals.",
                materials=["Fragment de Paldium", "Lingot", "Bois", "Pierre"],
            ),
        ]

    @staticmethod
    def _default_bosses() -> List[Boss]:
        return [
            Boss(
                id=1,
                name="Zoe et Grizzbolt",
                level=20,
                type="Electric",
                location="Tour du Syndicat de Rayne",
                hp=3050,
                rewards=["Badge de succes", "Ancient Technology Points"],
            ),
            Boss(
                id=2,
                name="Lily et Lyleen",
                level=35,
                type="Grass",
                location="Tour de l'Alliance Free Pal",
                hp=6937,
                rewards=["Badge de succes", "Ancient Technology Points"],
            ),
        ]
