#!/usr/bin/env python3
"""Probe and optionally extract Palworld data from a local server PAK."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

INCLUDE_PATHS = (
    "Pal/Content/Pal/DataTable/Character",
    "Pal/Content/Pal/DataTable/Item",
    "Pal/Content/Pal/DataTable/PassiveSkill",
    "Pal/Content/Pal/DataTable/PartnerSkill",
    "Pal/Content/Pal/DataTable/Technology",
    "Pal/Content/Pal/DataTable/Text",
    "Pal/Content/Pal/Blueprint/RaidBoss",
    "Pal/Content/L10N/en/Pal/DataTable/Text",
    "Pal/Content/L10N/fr/Pal/DataTable/Text",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_id(manifest: Path | None) -> str | None:
    if not manifest or not manifest.exists():
        return None
    match = re.search(r'"buildid"\s+"([^"]+)"', manifest.read_text())
    return match.group(1) if match else None


def repak_output(repak: Path, command: str, pak: Path) -> str:
    result = subprocess.run(
        [str(repak), command, str(pak)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pak", type=Path, required=True)
    parser.add_argument("--repak", type=Path, required=True)
    parser.add_argument("--steam-manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--extract", action="store_true")
    args = parser.parse_args()

    if not args.pak.is_file():
        parser.error(f"PAK introuvable: {args.pak}")
    if not args.repak.is_file():
        parser.error(f"repak introuvable: {args.repak}")

    info = repak_output(args.repak, "info", args.pak)
    listing = repak_output(args.repak, "list", args.pak)
    build = build_id(args.steam_manifest)
    dataset_dir = args.output / (build or "unknown-build")
    dataset_dir.mkdir(parents=True, exist_ok=True)

    selected = [
        line for line in listing.splitlines()
        if any(line.startswith(prefix) for prefix in INCLUDE_PATHS)
    ]
    manifest = {
        "game": "Palworld",
        "game_build": build,
        "extraction_date": datetime.now(timezone.utc).isoformat(),
        "extractor": "repak",
        "extractor_version": subprocess.run(
            [str(args.repak), "--version"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
        "source_pak": str(args.pak),
        "source_pak_sha256": sha256(args.pak),
        "source_pak_size": args.pak.stat().st_size,
        "pak_info": info.splitlines(),
        "selected_entry_count": len(selected),
        "selected_entries": selected,
        "status": "EXTRACTED" if args.extract else "PROBED",
    }

    if args.extract:
        command = [str(args.repak), "unpack", str(args.pak), "-o", str(dataset_dir / "pak"), "-q"]
        for include_path in INCLUDE_PATHS:
            command.extend(("-i", include_path))
        subprocess.run(command, check=True)

    manifest_path = dataset_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n")
    print(json.dumps({
        "build": build,
        "pak_sha256": manifest["source_pak_sha256"],
        "selected_entries": len(selected),
        "output": str(manifest_path),
        "status": manifest["status"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
