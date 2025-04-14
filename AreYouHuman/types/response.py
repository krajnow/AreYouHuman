from dataclasses import dataclass
from typing import List
from io import BytesIO


@dataclass
class Response:
    emojis_answer: List[str]
    emojis_list: List[str]
    image: BytesIO
