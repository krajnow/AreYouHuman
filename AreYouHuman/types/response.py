from __future__ import annotations

from dataclasses import dataclass
from collections import Counter
from io import BytesIO
from typing import List, TYPE_CHECKING

from aiogram.types import InlineKeyboardMarkup, BufferedInputFile

from AreYouHuman.utils import keyboard

if TYPE_CHECKING:
    from AreYouHuman.types.settings import Settings


@dataclass
class Response:
    settings: Settings
    emojis_answer: List[str]
    emojis_list: List[str]
    emojis_user: List[str]
    image: BytesIO

    @property
    def json(self) -> dict:
        """Returns object data as a dict for JSON serialization."""
        return dict(
            emojis_answer=self.emojis_answer,
            emojis_list=self.emojis_list,
            emojis_user=self.emojis_user,
            image=self.get_image()
        )

    def get_image(self) -> BufferedInputFile:
        """Convert the stored image BytesIO object into a BufferedInputFile."""
        return BufferedInputFile(file=self.image.getvalue(), filename="image.png")

    def checking_similarity(self) -> bool:
        """Check whether the user's choice matches the answers."""
        return Counter(self.emojis_user) == Counter(self.emojis_answer)

    def get_keyboard(self, user_id: int) -> InlineKeyboardMarkup:
        """Generate an inline keyboard for a bot."""
        return keyboard.generate(self, user_id)
