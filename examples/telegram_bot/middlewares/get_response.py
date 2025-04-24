from typing import Dict, Any

from aiogram import BaseMiddleware

from aiogram.types import (
    ChatMemberUpdated,
    TelegramObject,
    CallbackQuery
)

from aiogram.fsm.context import FSMContext


class ResponseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler,
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        state: FSMContext = data.get("state")

        if isinstance(event.chat_member, ChatMemberUpdated):
            match event.chat_member.new_chat_member.status:
                case "member":
                    await state.clear()
                case "left":
                    await state.clear()

        elif isinstance(event.callback_query, CallbackQuery):
            if not (response := (await state.get_data()).get("response")):
                return await event.callback_query.answer("🤷‍♂️")

            data["response"] = response

        return await handler(event, data)


__all__ = (
    "ResponseMiddleware",
)
