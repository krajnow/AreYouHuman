from dataclasses import dataclass, field
from typing import List, Tuple

from emoji_data_python import emoji_data


class DefaultEmojis:
    @classmethod
    def get_all(cls) -> List[str]:
        """Get all available emoji."""
        return [emoji.char for emoji in emoji_data if emoji.char]


@dataclass
class ButtonSettings:
    active: bool
    text: str


@dataclass
class KeyboardSettings:
    confirm: ButtonSettings = field(
        default_factory=lambda: ButtonSettings(active=True, text="✅ Confirm")
    )
    refresh: ButtonSettings = field(
        default_factory=lambda: ButtonSettings(active=True, text="🔄 Refresh")
    )
    row: int = field(
        default_factory=lambda: 5
    )


@dataclass(frozen=True)
class Settings:
    """Configuration settings for captcha generation."""

    gradient: Tuple[Tuple[int, int, int], Tuple[int, int, int]] = (
        (100, 200, 255),
        (200, 162, 200)
    )
    emojis: List[str] = field(
        default_factory=lambda: DefaultEmojis.get_all()
    )
    keyboard: KeyboardSettings = field(
        default_factory=lambda: KeyboardSettings()
    )
    sizes: Tuple[int, int] = (400, 300)
    emojis_dir: str = "emojis"
