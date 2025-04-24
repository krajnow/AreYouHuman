from aiogram import F, Router
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import CallbackQuery, ChatMemberUpdated, Message
from aiogram.enums.chat_type import ChatType
from aiogram.fsm.context import FSMContext

from AreYouHuman import Captcha
from AreYouHuman.types import CaptchaCallback, Response

from filters import UserCheckFilter


captcha = Captcha()
router = Router()


@router.callback_query(
    CaptchaCallback.filter(F.action.in_(["refresh"])),
    UserCheckFilter()
)
@router.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
    flags={"chat": True, "chat_options": [], "user": False}
)
async def captcha_generate(event: ChatMemberUpdated | CallbackQuery, state: FSMContext) -> Message:
    response: Response = captcha.generate()
    await state.update_data(response=response)

    if isinstance(event, ChatMemberUpdated):
        ...  # Add the action taken with the user yourself.

    elif isinstance(event, CallbackQuery):
        await event.message.delete()

    return await (
        event.message if isinstance(event, CallbackQuery) else event
    ).answer_photo(
        response.get_image(),
        caption="...",
        reply_markup=response.get_keyboard(event.from_user.id)
    )
