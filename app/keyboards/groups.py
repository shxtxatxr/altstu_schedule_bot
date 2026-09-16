from aiogram.utils.keyboard import InlineKeyboardBuilder


def groups_keyboard(groups: list[dict]):
    builder = InlineKeyboardBuilder()

    for group in groups:
        builder.button(
            text=group["value"],
            callback_data=f"group:{group['id']}",
        )

    builder.adjust(2)

    return builder.as_markup()