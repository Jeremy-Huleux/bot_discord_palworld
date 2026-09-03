"""Database backup service."""

from datetime import datetime, timezone
from pathlib import Path
import shutil


class BackupService:
    """Create timestamped copies of the SQLite database."""

    def __init__(self, database_path: Path, backup_dir: Path = None):
        self.database_path = Path(database_path)
        self.backup_dir = backup_dir or self.database_path.parent / "backups"

    def create_backup(self) -> Path:
        """Copy the database and return the generated backup path."""
        if not self.database_path.exists():
            raise FileNotFoundError(self.database_path)

        self.backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        destination = self.backup_dir / f"news-{timestamp}.db"
        shutil.copy2(self.database_path, destination)
        return destination
