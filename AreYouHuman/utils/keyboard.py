from __future__ import annotations

from typing import TYPE_CHECKING
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from AreYouHuman.types.callback import CaptchaCallback

if TYPE_CHECKING:
    from AreYouHuman.types.response import Response


def generate(response: Response, user_id: int) -> InlineKeyboardMarkup:
    """Generate an inline keyboard with emoji buttons and refresh option."""
    builder = InlineKeyboardBuilder()

    for emoji in response.emojis_list:
        builder.add(
            InlineKeyboardButton(
                text=f"• {emoji} •" if emoji in response.emojis_user else emoji,
                callback_data=CaptchaCallback(
                    user_id=user_id,
                    action="click",
                    emoji=emoji
                ).pack()
            )
        )

    if response.settings.keyboard.refresh.active:
        builder.add(
            InlineKeyboardButton(
                text=response.settings.keyboard.refresh.text,
                callback_data=CaptchaCallback(
                    user_id=user_id,
                    action="refresh"
                ).pack()
            )
        )
    if response.settings.keyboard.confirm.active:
        builder.add(
            InlineKeyboardButton(
                text=response.settings.keyboard.confirm.text,
                callback_data=CaptchaCallback(
                    user_id=user_id,
                    action="confirm"
                ).pack()
            )
        )

    builder.adjust(response.settings.keyboard.row)

    return builder.as_markup()
