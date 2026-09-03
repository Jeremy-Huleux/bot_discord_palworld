"""Tests for the local Pal encyclopedia."""

from models import Pal
from services.pal_dex import PalDexService


def test_search_by_name():
    dex = PalDexService()

    matches = dex.search("fox")

    assert [pal.name for pal in matches] == ["Foxparks"]


def test_search_by_type():
    dex = PalDexService()

    matches = dex.search("neutral")

    assert {pal.name for pal in matches} == {"Lamball", "Cattiva"}


def test_search_is_case_and_accent_insensitive():
    dex = PalDexService([
        Pal(
            id=99,
            name="Étoile",
            name_en="Star",
            type=["Neutral"],
        )
    ])

    assert dex.search("etoile")[0].name == "Étoile"


def test_get_by_id_returns_none_when_missing():
    dex = PalDexService()

    assert dex.get_by_id(999) is None
