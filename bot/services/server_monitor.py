"""Palworld server monitoring service."""

import time
from datetime import datetime, timezone
from typing import List

import aiohttp

from config import Config
from models import Player, ServerStatus


class ServerMonitorService:
    """Query the Palworld REST API without blocking Discord's event loop."""

    def __init__(self, api_url: str = None, timeout: float = None):
        configured_url = api_url or Config.PALWORLD_API_URL
        if not configured_url and Config.PALWORLD_SERVER_HOST:
            configured_url = (
                f"http://{Config.PALWORLD_SERVER_HOST}:{Config.PALWORLD_API_PORT}"
            )

        self.api_url = (configured_url or "").rstrip("/")
        self.username = Config.PALWORLD_ADMIN_USER
        self.password = Config.PALWORLD_ADMIN_PASSWORD
        self.timeout = timeout or Config.PALWORLD_SERVER_TIMEOUT
        self._online_since: float | None = None
        self._last_status = ServerStatus()

        if self.api_url and "://" not in self.api_url:
            self.api_url = f"http://{self.api_url}"

    @property
    def configured(self) -> bool:
        """Return whether a server endpoint is configured."""
        return bool(self.api_url and self.password)

    async def _get_json(self, endpoint: str) -> dict:
        """Fetch one authenticated REST endpoint."""
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        auth = aiohttp.BasicAuth(self.username, self.password)
        async with aiohttp.ClientSession(timeout=timeout, auth=auth) as session:
            async with session.get(f"{self.api_url}/v1/api/{endpoint}") as response:
                response.raise_for_status()
                return await response.json()

    async def get_status(self) -> ServerStatus:
        """Query server information and return a normalized status."""
        if not self.configured:
            return ServerStatus(last_check=self._timestamp())

        started = time.monotonic()
        try:
            info = await self._get_json("info")
            try:
                players = await self._get_json("players")
                player_count = len(players.get("players", []))
            except Exception:
                player_count = 0
            if self._online_since is None:
                self._online_since = time.monotonic()

            status = ServerStatus(
                is_online=True,
                player_count=player_count,
                max_players=Config.PALWORLD_MAX_PLAYERS,
                uptime=time.monotonic() - self._online_since,
                version=info.get("version"),
                last_check=self._timestamp(),
                response_time=(time.monotonic() - started) * 1000,
            )
        except Exception:
            self._online_since = None
            status = ServerStatus(
                is_online=False,
                last_check=self._timestamp(),
                response_time=(time.monotonic() - started) * 1000,
            )

        self._last_status = status
        return status

    async def get_players(self) -> List[Player]:
        """Query currently connected players."""
        if not self.configured:
            return []

        payload = await self._get_json("players")
        return [
            Player(
                uid=str(player.get("userId", index)),
                name=player.get("name") or "Joueur inconnu",
                level=int(player.get("level", 1)),
                is_online=True,
            )
            for index, player in enumerate(payload.get("players", []), start=1)
        ]

    @staticmethod
    def _timestamp() -> str:
        return datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
