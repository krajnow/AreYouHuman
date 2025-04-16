from typing import List

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from .callback import CaptchaCallback


class Keyboard:
    @staticmethod
    def generate(
        emojis_list: List[str],
        user_id: int
    ) -> InlineKeyboardMarkup:

        builder = InlineKeyboardBuilder()

        for emoji in emojis_list:
            builder.add(
                InlineKeyboardButton(
                    text=emoji,
                    callback_data=CaptchaCallback(
                        user_id=user_id,
                        action="click",
                        emoji=emoji
                    ).pack()
                )
            )

        builder.add(
            InlineKeyboardButton(
                text="🔄 Refresh",
                callback_data=CaptchaCallback(
                    user_id=user_id,
                    action="refresh"
                ).pack()
            )
        )

        builder.adjust(5)

        return builder.as_markup()
