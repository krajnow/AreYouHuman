from emoji_data_python import emoji_data
from emoji_data_python import EmojiChar

from dataclasses import dataclass
from dataclasses import field

from typing import Tuple
from typing import List


@dataclass(frozen=True)
class Settings:
    """
    Captcha generator settings.

    :param emojis: *Optional*. A set of emojis for captcha generation.
    :param sizes: *Optional*. The width and height of the canvas for drawing captcha.
    :param gradient: *Optional*. Color gradient from start to end.
    """

    emojis: List[EmojiChar] = field(default_factory=lambda: DefaultEmojis().emojis)

    sizes: Tuple[int, int] = (400, 300)

    gradient: Tuple[Tuple[int, ...], Tuple[int, ...]] = ((100, 200, 255), (200, 162, 200))


class DefaultEmojis:
    emojis: List[EmojiChar] = emoji_data
