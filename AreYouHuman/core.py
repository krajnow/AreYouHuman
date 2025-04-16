import random
import numpy
import math

from typing import Tuple
from typing import List
from io import BytesIO
from urllib.parse import unquote
from urllib.parse import quote

from PIL import ImageEnhance
from PIL import Image
from PIL.Image import Resampling

from AreYouHuman.types import Settings
from AreYouHuman.types import Response


class Captcha:
    def __init__(
        self,
        settings: Settings | None = None
    ) -> None:
        self.settings: Settings = settings or Settings()

    def generate(self) -> Response:
        """Captcha generation and obtaining data for verification."""
        emojis_list: List[str] = list(numpy.random.choice(self.settings.emojis, size=15, replace=False))
        emojis_answer: List[str] = list(numpy.random.choice(emojis_list, size=5, replace=False))
        background: Image.Image = self.background()

        emojis_pt: List[str] = [
             quote(_) for _ in emojis_answer
        ]

        emojis_p: List[Tuple[int, ...]] = []

        for emoji_pt in emojis_pt:
            w, h = self.settings.sizes
            size: Tuple[int, int] = (random.randint(int(h // 2.5), int(h // 2.2)), ) * 2

            emoji: Image.Image = ImageEnhance.Brightness((
                Image.open("emojis/" + emoji_pt).convert("RGBA")
                .resize(size, Resampling.LANCZOS)
                .rotate(
                    random.randint(0, 360),
                    expand=True,
                    resample=Resampling.BICUBIC
                )
            )).enhance(random.uniform(0.2, 1.0))

            radius: int = size[0] // 2

            place = False

            for _ in range(50):

                x, y = [random.randint(radius, s - radius) for s in self.settings.sizes]

                minimal_distance: float = 0.5 * (radius + max([p_r for p_x, p_y, p_r in emojis_p], default=0))

                if not self.checking_for_overlap((x, y), emojis_p, minimal_distance):
                    background.paste(emoji, (x - radius, y - radius), emoji)
                    emojis_p.append((x, y, radius))
                    place = True
                    break

            if not place:
                emojis_answer.remove(unquote(emoji_pt))

        image = BytesIO()
        background.save(image, format='png')
        image.seek(0)

        return Response(
            emojis_answer=emojis_answer,
            emojis_list=emojis_list,
            image=image
        )

    def background(self) -> Image.Image:
        """Creating a background for drawing."""

        j, k = [numpy.array(color) for color in self.settings.gradient]
        w, h = self.settings.sizes

        y, x = numpy.ogrid[:h, :w]
        d = (x / w + y / h) / 2

        gradient = (1 - d[..., numpy.newaxis]) * j + d[..., numpy.newaxis] * k

        return Image.fromarray(gradient.astype(numpy.uint8)).convert("RGBA")

    @staticmethod
    def checking_for_overlap(
            emoji_position: Tuple[int, int],
            existing: List[Tuple[int, ...]],
            minimal_distance: float
    ) -> bool:
        """Checking if the emoji overlaps other emojis."""
        emoji_x, emoji_y = emoji_position
        for data in existing:
            x, y, radius = data
            distance = math.sqrt(
                (emoji_x - x) ** 2 + (emoji_y - y) ** 2
            )
            if distance < minimal_distance:
                return True

        return False
