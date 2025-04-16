from typing import Optional

from aiogram.filters.callback_data import CallbackData


class CaptchaCallback(CallbackData, prefix="captcha"):
    user_id: int
    action: str
    emoji: Optional[str] = None
