"""Unit tests for the Palworld server monitor."""

import asyncio
from services.server_monitor import ServerMonitorService


def test_server_status_from_rest(monkeypatch):
    """REST server information is mapped to ServerStatus."""
    monitor = ServerMonitorService(api_url="http://example.test:8212")
    monitor.password = "test-password"
    async def get_json(endpoint):
        if endpoint == "players":
            return {"players": [{"name": "Alice"}, {"name": "Bob"}, {"name": "Eve"}]}
        return {"version": "1.0.0"}

    monkeypatch.setattr(monitor, "_get_json", get_json)

    status = asyncio.run(monitor.get_status())

    assert status.is_online
    assert status.player_count == 3
    assert status.max_players == 32
    assert status.version == "1.0.0"
    assert status.uptime >= 0


def test_server_status_offline(monkeypatch):
    """A failed REST query produces an offline status."""
    async def raise_timeout(endpoint):
        raise TimeoutError("server unavailable")

    monitor = ServerMonitorService(api_url="http://example.test:8212")
    monitor.password = "test-password"
    monkeypatch.setattr(monitor, "_get_json", raise_timeout)

    status = asyncio.run(monitor.get_status())

    assert not status.is_online
    assert status.player_count == 0
    assert status.uptime == 0


def test_server_url_is_configured():
    """A configured REST URL is used as the monitoring endpoint."""
    monitor = ServerMonitorService(api_url="http://example.test:9999")

    assert monitor.api_url == "http://example.test:9999"
