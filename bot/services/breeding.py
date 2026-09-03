"""Breeding calculator for the local Pal catalog."""

from typing import List

from models import Pal


class BreedingService:
    """Calculate likely offspring using breeding power proximity."""

    def __init__(self, pals: List[Pal]):
        self.pals = pals

    def calculate(self, first_name: str, second_name: str) -> List[Pal]:
        """Return catalog Pals closest to the parents' average breeding power."""
        first = self._find(first_name)
        second = self._find(second_name)
        if not first or not second:
            return []

        target = (first.breeding_power + second.breeding_power) / 2
        candidates = [pal for pal in self.pals if pal.id not in {first.id, second.id}]
        if not candidates:
            return []

        closest_distance = min(
            abs(pal.breeding_power - target) for pal in candidates
        )
        return [
            pal for pal in candidates
            if abs(pal.breeding_power - target) == closest_distance
        ][:10]

    def _find(self, name: str) -> Pal | None:
        normalized = name.strip().lower()
        return next(
            (
                pal for pal in self.pals
                if pal.name.lower() == normalized
                or pal.name_en.lower() == normalized
            ),
            None,
        )
