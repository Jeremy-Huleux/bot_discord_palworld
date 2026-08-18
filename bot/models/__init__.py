"""
Data models for Palworld Bot
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class NewsArticle:
    """News article model"""

    guid: str
    title: str
    url: str
    published: Optional[str] = None
    source: str = "Unknown"
    category: str = "news"
    summary: str = ""
    image: Optional[str] = None
    sent_at: Optional[str] = None

    def __post_init__(self):
        """Validation après initialisation"""
        if not self.guid:
            raise ValueError("GUID is required")
        if not self.title:
            raise ValueError("Title is required")

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "guid": self.guid,
            "title": self.title,
            "url": self.url,
            "published": self.published,
            "source": self.source,
            "category": self.category,
            "summary": self.summary,
            "image": self.image,
            "sent_at": self.sent_at,
        }

    def is_sent(self) -> bool:
        """Check if article has been sent to Discord"""
        return self.sent_at is not None

    def mark_as_sent(self, sent_at: Optional[str] = None):
        """Mark article as sent"""
        self.sent_at = sent_at or datetime.now().isoformat()


@dataclass
class Pal:
    """Palworld Pal model (for future Pal Dex)"""

    id: int
    name: str
    name_en: str
    type: List[str] = field(default_factory=list)
    rarity: int = 1
    hp: int = 0
    attack: int = 0
    defense: int = 0
    sp_atk: int = 0
    sp_def: int = 0
    speed: int = 0
    image: Optional[str] = None
    description: str = ""
    drops: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    partner_skill: Optional[str] = None
    breeding_power: int = 0

    def __post_init__(self):
        """Validation"""
        if not self.name:
            raise ValueError("Pal name is required")


@dataclass
class Item:
    """Palworld Item model (for future Items system)"""

    id: int
    name: str
    rarity: int = 1
    category: str = "misc"
    description: str = ""
    image: Optional[str] = None
    recipe: Optional[dict] = None
    materials: List[str] = field(default_factory=list)
    usage: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validation"""
        if not self.name:
            raise ValueError("Item name is required")


@dataclass
class Boss:
    """Palworld Boss model (for future Boss system)"""

    id: int
    name: str
    level: int
    type: Optional[str] = None
    location: str = ""
    hp: int = 0
    image: Optional[str] = None
    rewards: List[str] = field(default_factory=list)
    drops: List[str] = field(default_factory=list)
    description: str = ""

    def __post_init__(self):
        """Validation"""
        if not self.name:
            raise ValueError("Boss name is required")


@dataclass
class ServerStatus:
    """Palworld server status model (for future server monitoring)"""

    is_online: bool = False
    player_count: int = 0
    max_players: int = 0
    uptime: float = 0.0  # In seconds
    version: Optional[str] = None
    last_check: Optional[str] = None
    response_time: float = 0.0  # In milliseconds

    @property
    def player_slots_available(self) -> int:
        """Get available player slots"""
        return max(0, self.max_players - self.player_count)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "is_online": self.is_online,
            "player_count": self.player_count,
            "max_players": self.max_players,
            "uptime": self.uptime,
            "version": self.version,
            "last_check": self.last_check,
            "response_time": self.response_time,
        }


@dataclass
class Player:
    """Player model (for player tracking)"""

    uid: str
    name: str
    level: int = 1
    playtime: float = 0.0  # In hours
    last_seen: Optional[str] = None
    is_online: bool = False
    joined_at: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "uid": self.uid,
            "name": self.name,
            "level": self.level,
            "playtime": self.playtime,
            "last_seen": self.last_seen,
            "is_online": self.is_online,
            "joined_at": self.joined_at,
        }
