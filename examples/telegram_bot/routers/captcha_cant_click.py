from aiogram import F, Router
from aiogram.types import CallbackQuery

from AreYouHuman.types import CaptchaCallback

from filters import UserCheckFilter


router = Router()


@router.callback_query(
    CaptchaCallback.filter(F.action.in_(["refresh", "confirm", "click"])),
    ~UserCheckFilter()
)
async def cant_press(callback: CallbackQuery):
    return callback.answer("⚠️ You can't press this button.")
