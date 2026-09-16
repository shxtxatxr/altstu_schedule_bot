from aiogram.fsm.state import State, StatesGroup


class GroupStates(StatesGroup):
    waiting_for_group = State()
    waiting_for_selection = State()