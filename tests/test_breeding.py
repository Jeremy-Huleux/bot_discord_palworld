"""Tests for the local breeding calculator."""

from models import Pal
from services.breeding import BreedingService


def test_calculate_returns_closest_breeding_power():
    pals = [
        Pal(id=1, name="A", name_en="A", breeding_power=1000),
        Pal(id=2, name="B", name_en="B", breeding_power=800),
        Pal(id=3, name="C", name_en="C", breeding_power=900),
    ]

    matches = BreedingService(pals).calculate("A", "B")

    assert [pal.name for pal in matches] == ["C"]


def test_calculate_returns_empty_for_unknown_parent():
    pals = [Pal(id=1, name="A", name_en="A", breeding_power=1000)]

    assert BreedingService(pals).calculate("A", "Unknown") == []
