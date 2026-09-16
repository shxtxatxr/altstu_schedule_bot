from datetime import date

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.states import GroupStates
from app.keyboards.groups import groups_keyboard
from app.providers.altstu import search_groups
from app.services.schedule_service import get_group_schedule
from app.formatters.schedule import format_day_schedule

from app.repositories.user_repository import get_user_group
from app.repositories.user_repository import save_user_group

router = Router()


@router.message(F.text == "⚙️ Изменить группу")
async def choose_group(
    message: Message,
    state: FSMContext,
):
    await state.set_state(GroupStates.waiting_for_group)

    await message.answer(
        "Введите название группы или его часть.\n\n"
        "Например:\n"
        "ИВТ\n"
        "ИВТ-6\n"
        "ПИ"
    )


@router.message(GroupStates.waiting_for_group)
async def search_group_handler(
    message: Message,
    state: FSMContext,
):
    await search_and_show_groups(message, state)


@router.message(
    StateFilter(None),
    F.text,
    ~F.text.in_({
        "📅 Сегодня",
        "➡️ Завтра",
        "📋 Неделя",
        "➡️ Следующая неделя",
        "⚙️ Изменить группу",
        "🔄 Обновить расписание",
        "ℹ️ Помощь",
    }),
)
async def search_group_from_text(
    message: Message,
    state: FSMContext,
):
    @router.message(
        StateFilter(None),
        F.text,
        ~F.text.in_({
            "📅 Сегодня",
            "➡️ Завтра",
            "📋 Неделя",
            "➡️ Следующая неделя",
            "⚙️ Изменить группу",
            "🔄 Обновить расписание",
            "ℹ️ Помощь",
        }),
    )
    async def search_group_from_text(
            message: Message,
            state: FSMContext,
    ):
        await search_and_show_groups(
            message,
            state,
        )

    # Если группы нет — считаем сообщение поиском группы
    await search_and_show_groups(
        message,
        state,
    )


async def search_and_show_groups(
    message: Message,
    state: FSMContext,
):
    query = message.text.strip()

    if not query:
        await message.answer(
            "Введите название группы."
        )
        return

    groups = await search_groups(query)

    if not groups:
        await message.answer(
            f"По запросу «{query}» группы не найдены."
        )
        return

    group_options = {
        group["id"]: group["value"]
        for group in groups
    }

    await state.update_data(
        group_options=group_options
    )

    await state.set_state(
        GroupStates.waiting_for_selection
    )

    await message.answer(
        f"Найдено групп: {len(groups)}\n"
        "Выберите нужную:",
        reply_markup=groups_keyboard(groups),
    )


@router.callback_query(
    GroupStates.waiting_for_selection,
    F.data.startswith("group:")
)
async def group_selected(
    callback: CallbackQuery,
    state: FSMContext,
):
    external_id = callback.data.split(":", 1)[1]

    data = await state.get_data()
    group_options = data.get("group_options", {})

    group_name = group_options.get(external_id)

    if not group_name:
        await callback.answer(
            "Результаты поиска устарели. Выполните поиск заново.",
            show_alert=True,
        )

        await state.clear()
        return

    # Сохраняем выбранную группу
    await save_user_group(
        callback.from_user.id,
        external_id,
        group_name,
    )

    # Поиск группы завершён
    await state.clear()

    await callback.answer()

    try:
        # Получаем расписание выбранной группы
        lessons = await get_group_schedule(external_id)

        # Сегодня
        today = date.today()

        # Формируем расписание
        text = format_day_schedule(
            lessons,
            today,
            group_name,
        )

        # Вместо сообщения "группа выбрана"
        # сразу показываем расписание
        await callback.message.edit_text(text)

    except Exception:
        await callback.message.edit_text(
            f"📚 Группа: {group_name}\n\n"
            "Не удалось получить расписание на сегодня."
        )