#!/usr/bin/env python3
"""Normalize Palworld Pal parameters exported from UAssetAPI."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TABLE_NAME = "DT_PalMonsterParameter.json"
WORK_FIELDS = (
    "EmitFlame", "Watering", "Seeding", "GenerateElectricity", "Handcraft",
    "Collection", "Deforest", "Mining", "OilExtraction", "ProductMedicine",
    "Cool", "Transport", "MonsterFarm",
)


def property_map(row: dict[str, Any]) -> dict[str, Any]:
    """Convert UAssetAPI's property list into a name/value mapping."""
    properties = row.get("Value", [])
    if not isinstance(properties, list):
        return {}
    return {
        prop["Name"]: prop.get("Value")
        for prop in properties
        if isinstance(prop, dict) and prop.get("Name")
    }


def enum_value(value: Any) -> Any:
    """Remove Unreal enum namespace while preserving null-like values."""
    if isinstance(value, str) and "::" in value:
        return value.rsplit("::", 1)[-1]
    return value


def normalize_row(row_id: str, row: dict[str, Any], source_asset: str, build: str) -> dict[str, Any] | None:
    props = property_map(row)
    if props.get("IsPal") is not True:
        return None

    elements = [
        enum_value(props.get("ElementType1")),
        enum_value(props.get("ElementType2")),
    ]
    elements = [element for element in elements if element and element != "None"]
    work = {
        field.removeprefix("WorkSuitability_"): props[field]
        for field in WORK_FIELDS
        if field in props
    }

    values = {
        "internal_id": row_id,
        "paldeck_number": props.get("ZukanIndex"),
        "name_key": props.get("Tribe") or row_id,
        "element_types": elements,
        "size": enum_value(props.get("Size")),
        "rarity": props.get("Rarity"),
        "stats": {
            key.lower(): props[key]
            for key in ("HP", "MeleeAttack", "ShotAttack", "Defense", "Support", "Stamina")
            if key in props
        },
        "food_amount": props.get("FoodAmount"),
        "capture_rate_correct": props.get("CaptureRateCorrect"),
        "work_suitability": work,
        "partner_skill_key": props.get("PartnerSkill"),
        "active_skill_keys": [
            props[key] for key in ("Skill1", "Skill2", "Skill3", "Skill4")
            if props.get(key) not in (None, "None")
        ],
        "passive_skill_keys": [
            props[key] for key in ("PassiveSkill1", "PassiveSkill2", "PassiveSkill3", "PassiveSkill4")
            if props.get(key) not in (None, "None")
        ],
        "breeding": {
            "combi_rank": props.get("CombiRank"),
            "duplicate_priority": props.get("CombiDuplicatePriority"),
            "ignore_combi": props.get("IgnoreCombi"),
        },
        "flags": {
            key.removeprefix("Is"): props[key]
            for key in ("IsBoss", "IsTowerBoss", "IsRaidBoss")
            if key in props
        },
        "source": {
            "provenance": "GAME_DATA",
            "game_build": build,
            "source_asset": source_asset,
            "source_row": row_id,
            "extracted_at": datetime.now(timezone.utc).isoformat(),
        },
    }
    return values


def normalize(input_root: Path, output_path: Path, build: str) -> dict[str, Any]:
    matches = list(input_root.rglob(TABLE_NAME))
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {TABLE_NAME}, found {len(matches)}")

    payload = json.loads(matches[0].read_text(encoding="utf-8"))
    source_asset = payload["source_asset"]
    pals = {
        row_id: normalized
        for row_id, row in payload["rows"].items()
        if (normalized := normalize_row(row_id, row, source_asset, build)) is not None
    }
    result = {
        "dataset": "pals",
        "game_build": build,
        "source_asset": source_asset,
        "provenance": "GAME_DATA",
        "row_count": len(pals),
        "pals": pals,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--build", required=True)
    args = parser.parse_args()
    result = normalize(args.input_root, args.output, args.build)
    print(json.dumps({"dataset": result["dataset"], "build": result["game_build"], "pals": result["row_count"], "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
