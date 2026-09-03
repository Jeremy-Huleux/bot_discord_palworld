#!/usr/bin/env python3
"""Validate a normalized Palworld Pal dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

VALID_TYPES = {
    "Normal", "Fire", "Water", "Ice", "Leaf", "Earth", "Electricity",
    "Dark", "Dragon",
}
REQUIRED_FIELDS = {"internal_id", "element_types", "stats", "source"}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    payload = json.loads(path.read_text(encoding="utf-8"))
    pals = payload.get("pals")

    if not isinstance(pals, dict) or not pals:
        return ["dataset pals is empty or invalid"]

    if payload.get("provenance") != "GAME_DATA":
        errors.append("dataset provenance must be GAME_DATA")

    seen_ids: set[str] = set()
    for key, pal in pals.items():
        if not isinstance(pal, dict):
            errors.append(f"{key}: row is not an object")
            continue
        missing = REQUIRED_FIELDS - pal.keys()
        if missing:
            errors.append(f"{key}: missing fields {sorted(missing)}")
        internal_id = pal.get("internal_id")
        if not internal_id:
            errors.append(f"{key}: empty internal_id")
        elif internal_id in seen_ids:
            errors.append(f"{key}: duplicate internal_id {internal_id}")
        else:
            seen_ids.add(internal_id)

        element_types = pal.get("element_types", [])
        if not isinstance(element_types, list) or any(element not in VALID_TYPES for element in element_types):
            errors.append(f"{key}: invalid element_types")
        if pal.get("source", {}).get("provenance") != "GAME_DATA":
            errors.append(f"{key}: missing GAME_DATA row provenance")

    if payload.get("row_count") != len(pals):
        errors.append("row_count does not match pals length")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    args = parser.parse_args()
    errors = validate(args.dataset)
    if errors:
        print("VALIDATION FAILED")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"VALIDATION PASSED: {json.loads(args.dataset.read_text(encoding='utf-8'))['row_count']} pals")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
