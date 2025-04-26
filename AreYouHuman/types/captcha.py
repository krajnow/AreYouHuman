import math
import random
from io import BytesIO
from pathlib import Path
from urllib.parse import quote, unquote
from typing import List, Tuple, Optional

import numpy
from PIL import Image, ImageEnhance
from PIL.Image import Resampling

from AreYouHuman.exception import MissingDirectoryError
from AreYouHuman.types import Settings, Response


class Captcha:
    """A class for generating captcha images from emojis."""
    def __init__(
        self,
        settings: Optional[Settings] = None
    ) -> None:
        self.settings: Settings = settings or Settings()

        if not (Path() / self.settings.emojis_dir).is_dir():
            raise MissingDirectoryError()

    def generate(self) -> Response:
        """Captcha generation and obtaining data for verification."""
        emojis_list: List[str] = list(
            numpy.random.choice(self.settings.emojis, size=15, replace=False)
        )
        emojis_answer: List[str] = list(
            numpy.random.choice(emojis_list, size=5, replace=False)
        )
        background: Image.Image = self.background()

        emojis_pt: List[str] = [quote(_) for _ in emojis_answer]
        emojis_p: List[Tuple[int, ...]] = []

        w, h = self.settings.sizes
        c_w, c_h = w // 2, h // 2

        for emoji_pt in emojis_pt:
            size: Tuple[int, int] = (random.randint(int(h // 2.5), int(h // 2.2)), ) * 2

            emoji: Image.Image = ImageEnhance.Brightness((
                Image.open(Path() / self.settings.emojis_dir / emoji_pt).convert("RGBA")
                .resize(size, Resampling.LANCZOS)
                .rotate(
                    random.randint(0, 360),
                    expand=True,
                    resample=Resampling.BICUBIC
                )
            )).enhance(random.uniform(0.2, 1.0))

            radius: int = size[0] // 2
            place = False

            max_pr = min(c_w, c_h)
            current_pr = 0

            for _ in range(75):
                current_pr = min(current_pr + 10, max_pr)
                distance = random.uniform(0, current_pr)

                angle = random.uniform(0, 2 * math.pi)
                x, y = int(c_w + distance * math.cos(angle)), int(c_h + distance * math.sin(angle))

                if not (radius <= x <= w - radius and radius <= y <= h - radius):
                    continue

                minimal_distance: float = 0.7 * (radius + max([p_r for _, _, p_r in emojis_p], default=0))

                if not self.checking_for_overlap((x, y), emojis_p, minimal_distance):
                    background.paste(emoji, (x - radius, y - radius), emoji)
                    emojis_p.append((x, y, radius))
                    place = True
                    break

            if not place:
                emojis_answer.remove(unquote(emoji_pt))

        background.save(image := BytesIO(), format="PNG")
        image.seek(0)

        return Response(
            settings=self.settings,
            emojis_answer=emojis_answer,
            emojis_list=emojis_list,
            emojis_user=list(),
            image=image,
        )

    def background(self) -> Image.Image:
        """Creating a gradient background for drawing."""
        j, k = [numpy.array(color) for color in self.settings.gradient]
        width, height = self.settings.sizes

        y, x = numpy.ogrid[:height, :width]
        d = (x / width + y / height) / 2

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
        for x, y, radius in existing:
            distance = math.sqrt((emoji_x - x) ** 2 + (emoji_y - y) ** 2)
            if distance < minimal_distance:
                return True
        return False
