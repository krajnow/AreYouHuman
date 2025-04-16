from dataclasses import dataclass
from collections import Counter
from typing import List
from io import BytesIO


@dataclass
class Response:
    emojis_answer: List[str]
    emojis_list: List[str]
    image: BytesIO

    def get_json(self) -> dict:
        return dict(
            emojis_answer=self.emojis_answer,
            emojis_list=self.emojis_list,
            image=self.image
        )

    def checking_similarity(
        self,
        emojis_user: List[str]
    ) -> bool:
        """Checking whether the user's choice matches the answers."""

        return Counter(emojis_user) == Counter(self.emojis_answer)
