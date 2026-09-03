"""Tests for item and boss catalogs."""

from models import Boss, Item
from services.catalog import CatalogService


def test_search_items_by_name():
    catalog = CatalogService()
    assert catalog.search_items("mega")[0].name == "Mega Sphere"


def test_search_bosses_by_location():
    catalog = CatalogService()
    matches = catalog.search_bosses("Rayne")
    assert [boss.name for boss in matches] == ["Zoe et Grizzbolt"]


def test_catalog_accepts_injected_data():
    item = Item(id=10, name="Test Item")
    boss = Boss(id=10, name="Test Boss", level=1)
    catalog = CatalogService(items=[item], bosses=[boss])

    assert catalog.search_items("test")[0] is item
    assert catalog.search_bosses("test")[0] is boss
