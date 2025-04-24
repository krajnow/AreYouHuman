from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from AreYouHuman.types import CaptchaCallback, Response

from filters import UserCheckFilter


router = Router()


@router.callback_query(
    CaptchaCallback.filter((F.action.in_(["confirm"]))),
    UserCheckFilter()
)
async def captcha_confirm(callback: CallbackQuery, state: FSMContext, response: Response) -> None:
    await callback.message.delete()
    await state.clear()

    if not response.checking_similarity():
        ...  # 🚫 Captcha failed. Add the action taken with the user yourself.
        return

    ...  # ✅ Now you can chat. Add the action taken with the user yourself.
    return
