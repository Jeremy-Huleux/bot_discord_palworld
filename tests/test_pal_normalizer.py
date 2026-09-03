"""Tests for normalization of extracted Palworld tables."""

import json

from tools.normalize_pal_data import normalize


def test_normalize_only_game_pal_rows(tmp_path):
    input_root = tmp_path / "input"
    table = input_root / "DT_PalMonsterParameter.json"
    table.parent.mkdir()

    def prop(name, value):
        return {"Name": name, "Value": value}

    payload = {
        "source_asset": "Pal/Content/Pal/DataTable/Character/DT_PalMonsterParameter.uasset",
        "rows": {
            "TestPal": {
                "Value": [
                    prop("IsPal", True),
                    prop("ZukanIndex", 999),
                    prop("Tribe", "EPalTribeID::TestPal"),
                    prop("ElementType1", "EPalElementType::Fire"),
                    prop("ElementType2", "EPalElementType::None"),
                    prop("HP", 100),
                    prop("MeleeAttack", 80),
                    prop("ShotAttack", 90),
                    prop("Defense", 70),
                    prop("Stamina", 100),
                    prop("FoodAmount", 5),
                    prop("CombiRank", 500),
                    prop("IgnoreCombi", False),
                ]
            },
            "NotAPal": {"Value": [prop("IsPal", False)]},
        },
    }
    table.write_text(json.dumps(payload), encoding="utf-8")

    output = tmp_path / "pals.json"
    result = normalize(input_root, output, "test-build")

    assert result["row_count"] == 1
    assert result["pals"]["TestPal"]["element_types"] == ["Fire"]
    assert result["pals"]["TestPal"]["stats"]["hp"] == 100
    assert result["pals"]["TestPal"]["source"]["provenance"] == "GAME_DATA"
