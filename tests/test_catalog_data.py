"""Tests for the enriched catalog data."""

from services.catalog import CatalogService
from services.pal_dex import PalDexService


def test_enriched_pal_catalog_is_loaded():
    pals = PalDexService().pals
    assert len(pals) >= 25
    assert PalDexService().search("Jetragon")[0].name == "Jetragon"


def test_enriched_item_and_boss_catalogs_are_loaded():
    catalog = CatalogService()
    assert len(catalog.items) >= 10
    assert len(catalog.bosses) >= 8
    assert catalog.search_items("cake")[0].name == "Cake"
    assert catalog.search_bosses("raid")
