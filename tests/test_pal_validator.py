"""Tests for normalized Pal dataset validation."""

import json

from tools.validate_pal_data import validate


def test_valid_dataset_passes(tmp_path):
    dataset = {
        "provenance": "GAME_DATA",
        "row_count": 1,
        "pals": {
            "TestPal": {
                "internal_id": "TestPal",
                "element_types": ["Fire"],
                "stats": {"hp": 100},
                "source": {"provenance": "GAME_DATA"},
            }
        },
    }
    path = tmp_path / "pals.json"
    path.write_text(json.dumps(dataset), encoding="utf-8")

    assert validate(path) == []


def test_empty_dataset_is_rejected(tmp_path):
    path = tmp_path / "pals.json"
    path.write_text(json.dumps({"pals": {}}), encoding="utf-8")

    assert validate(path)
