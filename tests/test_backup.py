"""Tests for database backups."""

from pathlib import Path

from services.backup import BackupService


def test_create_backup(tmp_path: Path):
    database = tmp_path / "news.db"
    database.write_bytes(b"sqlite test data")
    backup_dir = tmp_path / "backups"

    backup_path = BackupService(database, backup_dir).create_backup()

    assert backup_path.exists()
    assert backup_path.parent == backup_dir
    assert backup_path.read_bytes() == b"sqlite test data"
    assert backup_path.name.startswith("news-")


def test_backup_requires_database(tmp_path: Path):
    database = tmp_path / "missing.db"

    try:
        BackupService(database).create_backup()
    except FileNotFoundError as error:
        assert error.args == (database,)
    else:
        raise AssertionError("Missing database should fail")
