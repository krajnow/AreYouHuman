from AreYouHuman.types import CaptchaCallback

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class UserCheckFilter(BaseFilter):
    async def __call__(
        self,
        callback: CallbackQuery,
        callback_data: CaptchaCallback
    ) -> bool:
        return callback.from_user.id == callback_data.user_id


__all__ = (
    "UserCheckFilter",
)
