"""Local Pal encyclopedia service."""

import unicodedata
import json
from pathlib import Path
from typing import List, Optional

from models import Pal


class PalDexService:
    """Search the local Pal catalog."""

    def __init__(self, pals: Optional[List[Pal]] = None):
        self.pals = pals or self._load_pals()

    @staticmethod
    def _load_pals() -> List[Pal]:
        path = Path(__file__).parent.parent / "data" / "catalog.json"
        if path.exists():
            payload = json.loads(path.read_text(encoding="utf-8"))
            return [Pal(**data) for data in payload.get("pals", [])]
        return PalDexService._default_pals()

    def search(self, query: str) -> List[Pal]:
        """Return Pals whose name or type matches the query."""
        normalized_query = self._normalize(query)
        if not normalized_query:
            return self.pals[:10]

        return [
            pal for pal in self.pals
            if normalized_query in self._normalize(pal.name)
            or normalized_query in self._normalize(pal.name_en)
            or any(normalized_query in self._normalize(pal_type) for pal_type in pal.type)
        ][:10]

    def get_by_id(self, pal_id: int) -> Optional[Pal]:
        """Return a Pal by numeric identifier."""
        return next((pal for pal in self.pals if pal.id == pal_id), None)

    @staticmethod
    def _normalize(value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value.lower())
        return "".join(char for char in normalized if not unicodedata.combining(char))

    @staticmethod
    def _default_pals() -> List[Pal]:
        return [
            Pal(
                id=1,
                name="Lamball",
                name_en="Lamball",
                type=["Neutral"],
                rarity=1,
                hp=70,
                attack=70,
                defense=70,
                description="Un Pal docile qui produit de la laine.",
                partner_skill="Bouclier laineux",
                breeding_power=1000,
            ),
            Pal(
                id=2,
                name="Foxparks",
                name_en="Foxparks",
                type=["Fire"],
                rarity=1,
                hp=70,
                attack=70,
                defense=70,
                description="Un petit Pal de feu capable d'etre porte.",
                partner_skill="Embraseur",
                breeding_power=950,
            ),
            Pal(
                id=3,
                name="Cattiva",
                name_en="Cattiva",
                type=["Neutral"],
                rarity=1,
                hp=70,
                attack=70,
                defense=70,
                description="Un Pal polyvalent qui aide a transporter les objets.",
                partner_skill="Cat Assistance",
                breeding_power=900,
            ),
        ]
