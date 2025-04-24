from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from AreYouHuman.types import CaptchaCallback, Response

from filters import UserCheckFilter


router = Router()


@router.callback_query(
    CaptchaCallback.filter((F.action.in_(["click"]))),
    UserCheckFilter()
)
async def captcha_click(callback: CallbackQuery, callback_data: CaptchaCallback, response: Response) -> Message | None:
    (response.emojis_user.remove if callback_data.emoji in response.emojis_user else response.emojis_user.append)(
        callback_data.emoji
    )
    return await callback.message.edit_reply_markup(reply_markup=response.get_keyboard(callback.from_user.id))
